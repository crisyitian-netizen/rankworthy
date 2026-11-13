#!/usr/bin/env python3
"""Rankworthy AI-visibility log: record and compare how AI answers mention you.

AI answers vary run to run, so treat results as samples. Keep the same query
set over time; compare only runs that used the same queries.

Usage:
  python3 ai_visibility.py init queries.txt --brand "Acme" > ai_log.csv
      (one query per line; writes an empty log with one row per query x engine)
  python3 ai_visibility.py report ai_log.csv
      (mention/citation rates by run date and engine, gaps, who is cited instead)

Log columns:
  date, engine, query, intent, run, mentioned (y/n), cited (y/n),
  position (1 = first brand named; blank if absent), competitors_named (;),
  cited_domains (;), notes
intent is one of: learn, choose, do, brand (see references/ai-visibility.md).
Python 3.8+ standard library only.
"""
import argparse, csv, sys, datetime
from collections import defaultdict, Counter

COLS = ["date", "engine", "query", "intent", "run", "mentioned", "cited", "position",
        "competitors_named", "cited_domains", "notes"]
ENGINES = ["google_ai_overview", "google_ai_mode", "chatgpt", "perplexity", "gemini", "copilot", "claude"]


def yes(v):
    return str(v).strip().lower() in ("y", "yes", "1", "true", "si", "sí", "是")


def init(qfile, engines):
    w = csv.writer(sys.stdout)
    w.writerow(COLS)
    today = datetime.date.today().isoformat()
    for q in [l.strip() for l in open(qfile, encoding="utf-8") if l.strip()]:
        for e in engines:
            w.writerow([today, e, q, "", "1", "", "", "", "", "", ""])


def report(path):
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8-sig")) if r.get("mentioned", "").strip()]
    if not rows:
        sys.exit("No filled rows (the 'mentioned' column is empty everywhere).")
    by = defaultdict(list)
    for r in rows:
        by[(r["date"], r["engine"])].append(r)
    L = ["# AI visibility report", "", "_Samples, not exact exposure. Compare only runs with the same query set._", "",
         "| Date | Engine | Answers | Mentioned | Cited | Avg position |", "|---|---|---|---|---|---|"]
    for (d, e), rs in sorted(by.items()):
        m = sum(yes(r["mentioned"]) for r in rs); c = sum(yes(r["cited"]) for r in rs)
        pos = [float(r["position"]) for r in rs if r.get("position", "").strip()]
        L.append(f"| {d} | {e} | {len(rs)} | {m} ({m/len(rs):.0%}) | {c} ({c/len(rs):.0%}) | {sum(pos)/len(pos):.1f} |" if pos else
                 f"| {d} | {e} | {len(rs)} | {m} ({m/len(rs):.0%}) | {c} ({c/len(rs):.0%}) | — |")
    dates = sorted({r["date"] for r in rows})
    latest = [r for r in rows if r["date"] == dates[-1]]
    gaps = [r for r in latest if not yes(r["mentioned"]) and r.get("competitors_named", "").strip()]
    L += ["", f"## Gaps on {dates[-1]}: competitors named, you are not"]
    L += [f"- [{r['engine']}] {r['query']} → {r['competitors_named']}" for r in gaps] or ["- none"]
    dom = Counter()
    for r in latest:
        if not yes(r["mentioned"]):
            for x in r.get("cited_domains", "").split(";"):
                if x.strip():
                    dom[x.strip().lower()] += 1
    L += ["", "## Sources AI cites where you are absent (go get listed / mentioned there)"]
    L += [f"- {d}: {n}" for d, n in dom.most_common(15)] or ["- none recorded"]
    intents = defaultdict(lambda: [0, 0])
    for r in latest:
        k = r.get("intent", "").strip() or "unlabelled"
        intents[k][0] += 1; intents[k][1] += yes(r["mentioned"])
    L += ["", "## By intent (latest run)"] + [f"- {k}: mentioned in {v[1]}/{v[0]}" for k, v in sorted(intents.items())]
    if len(dates) > 1:
        prev = {(r["engine"], r["query"]) for r in rows if r["date"] == dates[-2]}
        cur = {(r["engine"], r["query"]) for r in latest}
        same = prev & cur
        note = "same query set" if prev == cur else f"only {len(same)} engine×query pairs overlap — compare those only"
        L += ["", f"## Change vs {dates[-2]} ({note})"]
        pm = {(r["engine"], r["query"]): yes(r["mentioned"]) for r in rows if r["date"] == dates[-2]}
        cm = {(r["engine"], r["query"]): yes(r["mentioned"]) for r in latest}
        won = [k for k in same if cm[k] and not pm[k]]; lost = [k for k in same if pm[k] and not cm[k]]
        L += [f"- Gained: {e} · {q}" for e, q in won] + [f"- Lost: {e} · {q}" for e, q in lost] or ["- no change"]
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init"); i.add_argument("queries"); i.add_argument("--brand", default="")
    i.add_argument("--engines", default="google_ai_overview,chatgpt,perplexity")
    r = sub.add_parser("report"); r.add_argument("log")
    a = ap.parse_args()
    if a.cmd == "init":
        init(a.queries, [e.strip() for e in a.engines.split(",") if e.strip()])
    else:
        report(a.log)
