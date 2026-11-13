#!/usr/bin/env python3
"""Rankworthy Search Console analysis (free, no API key).

Reads a Search Console performance export (CSV) and finds the work that pays:
brand vs non-brand clicks, quick wins (positions ~8-20 with impressions),
low CTR for the position, and keyword cannibalization (one query split across
several pages; needs a query+page export).

Usage:
  python3 gsc_analyze.py Queries.csv --brand "acme,acme shop"
  python3 gsc_analyze.py query_page.csv --brand acme --min-impr 20

Accepts the Search Console UI export (Queries.csv / Pages.csv, any UI language
it recognises: English, Spanish, Chinese, Portuguese, French) or an API/Looker
export with columns query, page, clicks, impressions, ctr, position.
Python 3.8+ standard library only.
"""
import argparse, csv, io, sys
from collections import defaultdict

ALIASES = {
    "query": ["top queries", "query", "queries", "consultas principales", "consulta", "consultas",
              "热门查询", "查询", "principais consultas", "requêtes les plus fréquentes", "requête"],
    "page": ["top pages", "page", "pages", "landing page", "url", "páginas principales", "página",
             "热门网页", "网页", "principais páginas", "pages les plus populaires"],
    "clicks": ["clicks", "clics", "点击次数", "点击", "cliques"],
    "impressions": ["impressions", "impresiones", "展示次数", "展示", "impressões"],
    "ctr": ["ctr", "点击率"],
    "position": ["position", "posición", "排名", "posição", "average position", "posición media"],
}
# Rough organic CTR expectations by rounded position (only used to flag outliers).
EXPECTED_CTR = {1: .27, 2: .15, 3: .10, 4: .07, 5: .05, 6: .04, 7: .03, 8: .025, 9: .02, 10: .018}


def num(v):
    v = (v or "").strip().replace("%", "").replace(" ", "")
    if v.count(",") == 1 and v.count(".") == 0:
        v = v.replace(",", ".")
    v = v.replace(",", "")
    try:
        return float(v)
    except ValueError:
        return 0.0


def load(path):
    raw = open(path, "rb").read().decode("utf-8-sig", "replace")
    dialect = csv.Sniffer().sniff(raw.splitlines()[0], delimiters=",;\t")
    rows = list(csv.reader(io.StringIO(raw), dialect))
    head = [h.strip().lower() for h in rows[0]]
    cols = {}
    for key, names in ALIASES.items():
        for i, h in enumerate(head):
            if h in names and key not in cols:
                cols[key] = i
    if "query" not in cols and "page" not in cols:
        sys.exit(f"Could not find a query or page column in {path}. Headers: {rows[0]}")
    for need in ("clicks", "impressions", "position"):
        if need not in cols:
            sys.exit(f"Missing column '{need}' in {path}. Headers: {rows[0]}")
    data = []
    for r in rows[1:]:
        if not r or len(r) < len(head):
            continue
        d = {k: r[i].strip() for k, i in cols.items() if k in ("query", "page")}
        d.update({k: num(r[cols[k]]) for k in ("clicks", "impressions", "position")})
        # Recompute CTR from clicks/impressions: avoids "0.5%" vs "0.005" ambiguity across exports.
        d["ctr"] = d["clicks"] / d["impressions"] if d["impressions"] else 0.0
        data.append(d)
    return data, cols


def is_brand(q, brands):
    q = (q or "").lower()
    return any(b and b in q for b in brands)


def analyze(data, brands, min_impr):
    has_q = "query" in data[0] if data else False
    has_p = "page" in data[0] if data else False
    out = {"rows": len(data)}
    tot_c = sum(d["clicks"] for d in data)
    tot_i = sum(d["impressions"] for d in data)
    out["clicks"], out["impressions"] = int(tot_c), int(tot_i)
    if has_q:
        agg = defaultdict(lambda: {"clicks": 0, "impressions": 0, "pos_w": 0})
        for d in data:
            a = agg[d["query"]]
            a["clicks"] += d["clicks"]; a["impressions"] += d["impressions"]; a["pos_w"] += d["position"] * d["impressions"]
        q = [{"query": k, "clicks": v["clicks"], "impressions": v["impressions"],
              "position": v["pos_w"] / v["impressions"] if v["impressions"] else 0,
              "ctr": v["clicks"] / v["impressions"] if v["impressions"] else 0} for k, v in agg.items()]
        if brands:
            bc = sum(x["clicks"] for x in q if is_brand(x["query"], brands))
            out["brand_click_share"] = round(bc / tot_c, 3) if tot_c else None
            out["nonbrand_clicks"] = int(tot_c - bc)
        nb = [x for x in q if not is_brand(x["query"], brands)]
        out["quick_wins"] = sorted([x for x in nb if 7.5 <= x["position"] <= 20.5 and x["impressions"] >= min_impr],
                                   key=lambda x: -x["impressions"])[:25]
        low = []
        for x in nb:
            p = round(x["position"])
            if 1 <= p <= 10 and x["impressions"] >= min_impr and x["ctr"] < EXPECTED_CTR[p] * 0.5:
                low.append(dict(x, expected_ctr=EXPECTED_CTR[p]))
        out["low_ctr"] = sorted(low, key=lambda x: -x["impressions"])[:25]
        out["zero_click_queries"] = sorted([x for x in nb if x["clicks"] == 0 and x["impressions"] >= min_impr],
                                           key=lambda x: -x["impressions"])[:25]
    if has_q and has_p:
        by_q = defaultdict(list)
        for d in data:
            by_q[d["query"]].append(d)
        cann = []
        for qq, rows in by_q.items():
            ti = sum(r["impressions"] for r in rows)
            pages = [r for r in rows if ti and r["impressions"] / ti >= 0.1]
            if len(pages) >= 2 and ti >= min_impr:
                cann.append({"query": qq, "impressions": ti,
                             "pages": [(r["page"], int(r["impressions"]), round(r["position"], 1)) for r in sorted(pages, key=lambda r: -r["impressions"])]})
        out["cannibalization"] = sorted(cann, key=lambda x: -x["impressions"])[:25]
    if has_p and not has_q:
        out["pages_low_ctr"] = sorted([d for d in data if d["impressions"] >= min_impr and d["ctr"] < 0.02],
                                      key=lambda x: -x["impressions"])[:25]
    return out


def md(o, brands):
    f = lambda x: f"{x['query']} — {int(x['impressions'])} impr, {int(x['clicks'])} clicks, pos {x['position']:.1f}, CTR {x['ctr']*100:.1f}%"
    L = ["# Search Console analysis", "", f"- Rows: {o['rows']} · Clicks: {o['clicks']} · Impressions: {o['impressions']}"]
    if "brand_click_share" in o and o["brand_click_share"] is not None:
        L.append(f"- Brand share of clicks: {o['brand_click_share']*100:.0f}% (non-brand clicks: {o['nonbrand_clicks']}). Non-brand clicks are the new customers SEO brings.")
    elif not brands:
        L.append("- Tip: pass --brand to split brand and non-brand queries.")
    for key, title, note in [
        ("quick_wins", "Quick wins (non-brand, position ~8–20)", "Improve the ranking page: answer-first section, better title, internal links from strong pages."),
        ("low_ctr", "Low CTR for the position (non-brand)", "Rewrite title and meta description; check the result type the SERP shows."),
        ("zero_click_queries", "Impressions but zero clicks (non-brand)", "Check intent match; consider a section or page that answers this query.")]:
        if key in o:
            L += ["", f"## {title}", f"_{note}_"] + ([f"- {f(x)}" for x in o[key]] or ["- none"])
    if "cannibalization" in o:
        L += ["", "## Possible cannibalization (one query, several pages)", "_Merge, or make one page clearly primary and link to it._"]
        for c in o["cannibalization"] or []:
            L.append(f"- **{c['query']}** ({int(c['impressions'])} impr): " + "; ".join(f"{p} ({i} impr, pos {pos})" for p, i, pos in c["pages"]))
        if not o["cannibalization"]:
            L.append("- none found")
    if "pages_low_ctr" in o:
        L += ["", "## Pages with impressions but CTR under 2%"] + [f"- {d['page']} — {int(d['impressions'])} impr, CTR {d['ctr']*100:.1f}%, pos {d['position']:.1f}" for d in o["pages_low_ctr"]]
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--brand", default="", help="comma-separated brand terms, e.g. 'acme,acme shop'")
    ap.add_argument("--min-impr", type=float, default=20)
    a = ap.parse_args()
    brands = [b.strip().lower() for b in a.brand.split(",") if b.strip()]
    data, _ = load(a.csv)
    if not data:
        sys.exit("No rows found.")
    print(md(analyze(data, brands, a.min_impr), brands))
