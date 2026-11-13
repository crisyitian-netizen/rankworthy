# W8 Measurement and reporting

## What to measure
- **Money first**: GA4 key events for form submits, WhatsApp/phone clicks, sign-ups/account requests, orders. Report "leads / sign-ups / orders from organic search this period". If not tracked, set it up before anything else.
- **Search Console**: clicks, impressions, average position (28 days), money-keyword positions, indexed pages, brand vs non-brand clicks (`gsc_analyze.py --brand`). Generative AI report: impressions in AI Overviews / AI Mode.
- **GA4 AI referrals**: sessions and conversions from chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com, claude.ai.
- **Local**: profile calls, direction requests, website clicks (UTM), review count and pace.
- **AI visibility**: the fixed prompt set (W7).

## Baselines
Record every metric with date and definition (e.g. 28-day clicks). Missing data is "not recorded", never estimated. If a test set changes, say "not comparable".

## Change log (run alongside every change)
| Date | Change | Why | Baseline | Re-check date | Result | Verdict (keep / revert / iterate) |
|---|---|---|---|---|---|---|
Pilots that are stopped or pages taken down are logged too, with the reason.

## Cadence
| Frequency | Work |
|---|---|
| Daily / on publish | IndexNow ping, 404 and health checks |
| Weekly | Search Console report (clicks, impressions, indexing, conversions); queries with impressions but no clicks go to the content queue; one Business Profile post |
| Monthly | Keep a buffer of scheduled articles and refresh a few old ones; re-test money keywords and the AI prompt set; request new reviews |
| Quarterly | Full audit (W1) and off-site inventory (W6) |

## Report template (for the owner, in their language)
1. **Bottom line**: 3-4 sentences with the business result and the next priority.
2. **Numbers vs baseline** (table with dates and definitions).
3. **What was done** (by area).
4. **Tried and stopped** (with reason).
5. **Open issues** (table: issue, evidence, who does it).
6. **Next steps** with dates; no ranking promises; content changes typically show in 2-8 weeks.
7. **Rules followed** (backups, approvals, private data).
