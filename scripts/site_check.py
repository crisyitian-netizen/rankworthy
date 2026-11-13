#!/usr/bin/env python3
"""Rankworthy site check: free, dependency-free SEO + GEO checks for one URL.

Usage:
  python3 site_check.py https://example.com/page [--json] [--timeout 20]

Checks: HTTP status and redirects, response time and size, title and meta
description, robots meta and X-Robots-Tag, canonical, H1/H2, lang, hreflang,
Open Graph, JSON-LD types, visible word count (and a hint when content seems to
need JavaScript), links, images without alt, robots.txt access for search and
AI crawlers, sitemap and llms.txt presence.
Only reads public pages. Python 3.8+ standard library only.
"""
import argparse, json, re, sys, time, gzip
import urllib.request, urllib.error, urllib.robotparser
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; Rankworthy-SiteCheck/1.0; +https://github.com/)"

# Crawlers that decide whether a site can appear/cited in search or AI answers,
# versus crawlers mainly used for model training.
SEARCH_BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User",
               "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
               "Applebot", "DuckAssistBot"]
TRAINING_BOTS = ["GPTBot", "ClaudeBot", "Google-Extended", "Applebot-Extended",
                 "CCBot", "Bytespider", "meta-externalagent"]


def fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        status = resp.status
    except urllib.error.HTTPError as e:
        resp, status = e, e.code
    body = resp.read()
    if resp.headers.get("Content-Encoding", "") == "gzip":
        try:
            body = gzip.decompress(body)
        except OSError:
            pass
    elapsed = time.time() - t0
    return {"status": status, "final_url": resp.geturl() if hasattr(resp, "geturl") else url,
            "headers": dict(resp.headers.items()), "body": body, "seconds": round(elapsed, 2)}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title = "", False
        self.meta, self.links_rel, self.hreflang, self.og = {}, {}, [], {}
        self.h1, self.h2, self.cur_h = [], [], None
        self.lang = None
        self.jsonld, self.in_jsonld, self.buf = [], False, ""
        self.skip = 0
        self.text = []
        self.anchors, self.imgs_no_alt, self.imgs = [], 0, 0
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.lang = a["lang"]
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name.startswith("og:"):
                self.og[name] = a.get("content", "")
            elif name:
                self.meta[name] = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if rel == "alternate" and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], a.get("href", "")))
            elif rel:
                self.links_rel[rel] = a.get("href", "")
        elif tag in ("h1", "h2"):
            self.cur_h, self.buf = tag, ""
        elif tag == "script":
            self.scripts += 1
            if a.get("type", "").lower() == "application/ld+json":
                self.in_jsonld, self.buf = True, ""
            else:
                self.skip += 1
        elif tag in ("style", "noscript", "template"):
            self.skip += 1
        elif tag == "a" and a.get("href"):
            self.anchors.append(a["href"])
        elif tag == "img":
            self.imgs += 1
            if not a.get("alt", "").strip():
                self.imgs_no_alt += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == self.cur_h:
            (self.h1 if tag == "h1" else self.h2).append(re.sub(r"\s+", " ", self.buf).strip())
            self.cur_h = None
        elif tag == "script":
            if self.in_jsonld:
                self.jsonld.append(self.buf)
                self.in_jsonld = False
            elif self.skip:
                self.skip -= 1
        elif tag in ("style", "noscript", "template") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_jsonld or self.cur_h:
            self.buf += data
        if not self.skip and not self.in_jsonld:
            self.text.append(data)


def jsonld_types(blocks):
    types, errors = [], 0

    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t:
                types.extend(t if isinstance(t, list) else [t])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for b in blocks:
        try:
            walk(json.loads(b))
        except ValueError:
            errors += 1
    return sorted(set(map(str, types))), errors


def robots_report(base, timeout):
    url = urljoin(base, "/robots.txt")
    out = {"url": url, "found": False, "sitemaps": [], "search_bots": {}, "training_bots": {}}
    try:
        r = fetch(url, timeout)
    except Exception as e:  # network error
        out["error"] = str(e)
        return out
    if r["status"] != 200:
        out["status"] = r["status"]
        return out
    text = r["body"].decode("utf-8", "replace")
    out["found"] = True
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    path = urljoin(base, "/")
    for bot in SEARCH_BOTS:
        out["search_bots"][bot] = rp.can_fetch(bot, path)
    for bot in TRAINING_BOTS:
        out["training_bots"][bot] = rp.can_fetch(bot, path)
    out["sitemaps"] = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", text)
    return out


def count_sitemap(url, timeout):
    try:
        r = fetch(url, timeout)
    except Exception as e:
        return {"url": url, "error": str(e)}
    if r["status"] != 200:
        return {"url": url, "status": r["status"]}
    body = r["body"].decode("utf-8", "replace")
    return {"url": url, "status": 200,
            "type": "index" if "<sitemapindex" in body else "urlset",
            "entries": len(re.findall(r"<loc>", body)),
            "has_lastmod": "<lastmod>" in body}


def check(url, timeout=20):
    r = fetch(url, timeout)
    html = r["body"].decode("utf-8", "replace")
    p = PageParser()
    p.feed(html)
    text = re.sub(r"\s+", " ", " ".join(p.text)).strip()
    words = len(text.split())
    host = urlparse(r["final_url"]).netloc
    internal = sum(1 for h in p.anchors if urlparse(urljoin(r["final_url"], h)).netloc == host)
    types, jsonld_err = jsonld_types(p.jsonld)
    base = f"{urlparse(r['final_url']).scheme}://{host}"
    robots = robots_report(base, timeout)
    sitemaps = [count_sitemap(s, timeout) for s in (robots.get("sitemaps") or [urljoin(base, "/sitemap.xml")])[:3]]
    llms = None
    try:
        lr = fetch(urljoin(base, "/llms.txt"), timeout)
        llms = lr["status"] == 200 and len(lr["body"]) > 20
    except Exception:
        llms = None
    x_robots = r["headers"].get("X-Robots-Tag", "")
    meta_robots = p.meta.get("robots", "")
    res = {
        "url": url, "final_url": r["final_url"], "status": r["status"], "seconds": r["seconds"],
        "html_kb": round(len(r["body"]) / 1024, 1),
        "title": p.title.strip(), "title_len": len(p.title.strip()),
        "meta_description": p.meta.get("description", ""), "meta_description_len": len(p.meta.get("description", "")),
        "meta_robots": meta_robots, "x_robots_tag": x_robots,
        "noindex": "noindex" in (meta_robots + x_robots).lower(),
        "canonical": p.links_rel.get("canonical", ""),
        "lang": p.lang, "hreflang": p.hreflang,
        "h1": p.h1, "h2_count": len(p.h2), "h2_sample": p.h2[:8],
        "og": {k: v for k, v in p.og.items() if k in ("og:title", "og:description", "og:image", "og:type")},
        "jsonld_types": types, "jsonld_parse_errors": jsonld_err,
        "visible_words": words, "scripts": p.scripts,
        "js_dependent_hint": words < 150 and p.scripts > 5,
        "links_internal": internal, "links_total": len(p.anchors),
        "images": p.imgs, "images_without_alt": p.imgs_no_alt,
        "robots_txt": robots, "sitemaps": sitemaps, "llms_txt_present": llms,
    }
    res["issues"] = issues(res)
    return res


def issues(r):
    out = []
    add = lambda sev, msg: out.append({"severity": sev, "issue": msg})
    if r["status"] != 200:
        add("critical", f"HTTP status {r['status']}")
    if r["noindex"]:
        add("critical", "Page is noindex (meta robots or X-Robots-Tag)")
    rb = r["robots_txt"]
    if rb.get("found"):
        blocked = [b for b, ok in rb["search_bots"].items() if not ok]
        if "Googlebot" in blocked or "Bingbot" in blocked:
            add("critical", f"robots.txt blocks search crawlers: {', '.join(blocked)}")
        elif blocked:
            add("high", f"robots.txt blocks AI search/answer crawlers (site cannot be cited there): {', '.join(blocked)}")
    if not r["title"]:
        add("high", "Missing <title>")
    elif r["title_len"] > 65:
        add("low", f"Title is long ({r['title_len']} chars); may be truncated")
    if not r["meta_description"]:
        add("medium", "Missing meta description")
    if len(r["h1"]) == 0:
        add("high", "No H1")
    elif len(r["h1"]) > 1:
        add("medium", f"{len(r['h1'])} H1 tags")
    if not r["canonical"]:
        add("medium", "No canonical link")
    if r["js_dependent_hint"]:
        add("high", "Very little text in raw HTML; main content may need JavaScript (many AI crawlers do not run JS)")
    if not r["jsonld_types"]:
        add("medium", "No JSON-LD structured data")
    if r["jsonld_parse_errors"]:
        add("high", f"{r['jsonld_parse_errors']} JSON-LD block(s) do not parse")
    if not r["og"].get("og:image"):
        add("low", "No og:image (no share preview)")
    if r["images"] and r["images_without_alt"]:
        add("low", f"{r['images_without_alt']}/{r['images']} images without alt text")
    if r["seconds"] > 2.5:
        add("medium", f"Slow HTML response ({r['seconds']} s)")
    if not any(s.get("status") == 200 for s in r["sitemaps"]):
        add("medium", "No reachable XML sitemap")
    return out


def to_markdown(r):
    L = [f"# Site check: {r['final_url']}", "",
         f"- Status {r['status']} · {r['seconds']} s · {r['html_kb']} KB HTML · {r['visible_words']} visible words",
         f"- Title ({r['title_len']}): {r['title'] or '—'}",
         f"- Description ({r['meta_description_len']}): {r['meta_description'] or '—'}",
         f"- H1: {' | '.join(r['h1']) or '—'} · H2 count: {r['h2_count']}",
         f"- Canonical: {r['canonical'] or '—'} · lang: {r['lang'] or '—'} · hreflang: {len(r['hreflang'])}",
         f"- JSON-LD: {', '.join(r['jsonld_types']) or '—'}",
         f"- og:image: {'yes' if r['og'].get('og:image') else 'no'} · llms.txt: {r['llms_txt_present']}", ""]
    rb = r["robots_txt"]
    if rb.get("found"):
        L.append("## Crawler access (robots.txt, homepage)")
        L.append("Search / answer crawlers: " + ", ".join(f"{b} {'✓' if ok else '✗'}" for b, ok in rb["search_bots"].items()))
        L.append("Training crawlers: " + ", ".join(f"{b} {'✓' if ok else '✗'}" for b, ok in rb["training_bots"].items()))
        L.append("")
    else:
        L += ["## Crawler access", "robots.txt not found or not reachable", ""]
    L.append("## Sitemaps")
    for s in r["sitemaps"]:
        L.append(f"- {s.get('url')}: " + (f"{s.get('type')} with {s.get('entries')} entries, lastmod {'yes' if s.get('has_lastmod') else 'no'}" if s.get("status") == 200 else f"not available ({s.get('status') or s.get('error')})"))
    L += ["", "## Issues"]
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    for i in sorted(r["issues"], key=lambda x: order[x["severity"]]) or [{"severity": "ok", "issue": "No issues found by the automatic checks"}]:
        L.append(f"- **{i['severity']}** — {i['issue']}")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    ap.add_argument("--timeout", type=int, default=20)
    a = ap.parse_args()
    try:
        res = check(a.url, a.timeout)
    except Exception as e:
        sys.exit(f"Could not fetch {a.url}: {e}")
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else to_markdown(res))
