#!/usr/bin/env python3
"""Rankworthy optional DataForSEO client with spending guardrails.

Paid data (pay as you go). Every call:
  1. prints what it will request and a rough cost note, and
  2. only runs with --confirm (the agent must ask the user first), and
  3. logs the actual cost reported by DataForSEO to ~/.rankworthy/spend.csv,
  4. refuses to run if today's logged spend would exceed --daily-budget.

Credentials: set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD yourself (API Access
page in your DataForSEO dashboard). Never paste them into a chat.

Usage:
  python3 dataforseo.py volume "kw one" "kw two" --location 2152 --lang es --confirm
  python3 dataforseo.py ideas "seed keyword" --location 2840 --lang en --limit 100 --confirm
  python3 dataforseo.py serp "keyword" --location 2152 --lang es --confirm
  python3 dataforseo.py maps "keyword" --coordinate "-33.44,-70.65,14z" --lang es --confirm
  python3 dataforseo.py ranked example.com --location 2152 --lang es --limit 100 --confirm
  python3 dataforseo.py backlinks example.com --confirm
  python3 dataforseo.py spend          # today's and this month's logged spend

Location codes: e.g. 2840 United States, 2724 Spain, 2484 Mexico, 2152 Chile,
2032 Argentina, 2170 Colombia, 2604 Peru, 2156 China. Check the official list.
Prices change; see https://dataforseo.com/pricing. Python 3.8+ stdlib only.
"""
import argparse, base64, csv, datetime, json, os, sys, urllib.request, urllib.error
from pathlib import Path

API = "https://api.dataforseo.com"
LOG = Path.home() / ".rankworthy" / "spend.csv"
ENDPOINTS = {
    "volume": ("/v3/keywords_data/google_ads/search_volume/live", "one task, up to 1000 keywords; usually cents"),
    "ideas": ("/v3/dataforseo_labs/google/keyword_ideas/live", "one task; usually cents"),
    "serp": ("/v3/serp/google/organic/live/advanced", "about $0.002 per live SERP"),
    "maps": ("/v3/serp/google/maps/live/advanced", "about $0.002 per live Maps SERP"),
    "ranked": ("/v3/dataforseo_labs/google/ranked_keywords/live", "one task; usually cents"),
    "backlinks": ("/v3/backlinks/summary/live", "Backlinks API may need its own subscription; check pricing"),
}


def spent(since):
    if not LOG.exists():
        return 0.0
    tot = 0.0
    for r in csv.reader(open(LOG)):
        try:
            if r[0][:len(since)] == since:
                tot += float(r[2])
        except (IndexError, ValueError):
            pass
    return tot


def log_cost(cmd, cost):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", newline="") as f:
        csv.writer(f).writerow([datetime.datetime.now().isoformat(timespec="seconds"), cmd, f"{cost:.4f}"])


def build(a):
    loc = {"location_code": a.location} if a.location else {}
    lang = {"language_code": a.lang} if a.lang else {}
    if a.cmd == "volume":
        return [dict(keywords=a.items, **loc, **lang)]
    if a.cmd == "ideas":
        return [dict(keywords=a.items, limit=a.limit, **loc, **lang)]
    if a.cmd == "serp":
        return [dict(keyword=k, depth=a.limit if a.limit <= 100 else 100, **loc, **lang) for k in a.items]
    if a.cmd == "maps":
        base = dict(**lang)
        if a.coordinate:
            base["location_coordinate"] = a.coordinate
        else:
            base.update(loc)
        return [dict(keyword=k, **base) for k in a.items]
    if a.cmd == "ranked":
        return [dict(target=a.items[0], limit=a.limit, **loc, **lang)]
    if a.cmd == "backlinks":
        return [dict(target=a.items[0], internal_list_limit=10)]
    raise SystemExit("unknown command")


def call(path, payload):
    login, pw = os.environ.get("DATAFORSEO_LOGIN"), os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not pw:
        sys.exit("Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD environment variables first.")
    tok = base64.b64encode(f"{login}:{pw}".encode()).decode()
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(), method="POST",
                                 headers={"Authorization": "Basic " + tok, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read()[:300]!r}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error ({e.reason}). If running in a sandbox, api.dataforseo.com may need to be allowed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=list(ENDPOINTS) + ["spend"])
    ap.add_argument("items", nargs="*")
    ap.add_argument("--location", type=int, default=None)
    ap.add_argument("--lang", default=None)
    ap.add_argument("--coordinate", default=None, help='maps only: "lat,lng,zoom", e.g. "-33.44,-70.65,14z"')
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--daily-budget", type=float, default=5.0, help="USD; refuse when today's logged spend reaches it")
    ap.add_argument("--confirm", action="store_true", help="actually call the paid API")
    ap.add_argument("--out", default=None, help="save raw JSON response to this file")
    a = ap.parse_args()
    today, month = datetime.date.today().isoformat(), datetime.date.today().isoformat()[:7]
    if a.cmd == "spend":
        print(f"Logged spend today: ${spent(today):.4f} · this month: ${spent(month):.4f} ({LOG})")
        sys.exit(0)
    if not a.items:
        sys.exit("Give at least one keyword or domain.")
    path, note = ENDPOINTS[a.cmd]
    payload = build(a)
    print(f"Request: POST {path} · {len(payload)} task(s) · cost note: {note}")
    print(f"Logged spend today: ${spent(today):.4f} / daily budget ${a.daily_budget:.2f}")
    if spent(today) >= a.daily_budget:
        sys.exit("Daily budget reached. Raise --daily-budget only if the user agrees.")
    if not a.confirm:
        print("Dry run. Ask the user to approve this spend, then re-run with --confirm.")
        sys.exit(0)
    res = call(path, payload)
    cost = float(res.get("cost") or 0)
    log_cost(a.cmd, cost)
    print(f"Status: {res.get('status_code')} {res.get('status_message')} · actual cost ${cost:.4f}")
    if a.out:
        Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(f"Saved raw response to {a.out}")
    else:
        for t in res.get("tasks", [])[:5]:
            items = ((t.get("result") or [{}])[0] or {}).get("items") or t.get("result") or []
            print(f"- task {t.get('status_code')} {t.get('status_message')}: {len(items)} item(s)")
            for it in items[:20]:
                keep = {k: it.get(k) for k in ("keyword", "search_volume", "competition", "cpc", "rank_absolute",
                                               "type", "title", "url", "domain", "rating", "rank_group") if it.get(k) is not None}
                if "keyword_data" in it:
                    kd = it["keyword_data"]; keep.update(keyword=kd.get("keyword"), search_volume=(kd.get("keyword_info") or {}).get("search_volume"))
                print("  ", json.dumps(keep, ensure_ascii=False)[:220])
