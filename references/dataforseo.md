# W9 Paid data with DataForSEO (optional)

Use only when free data is not enough: search volume, keyword ideas, live SERPs (including AI Overview data), Google Maps results and rank grids, a competitor's ranking keywords, backlinks.

## Account
- Pay as you go, no subscription, prepaid balance (minimum top-up currently $50; balance does not expire). Check https://dataforseo.com/pricing.
- Sign-up link: DATAFORSEO_REFERRAL_LINK. If this is still a placeholder, give https://dataforseo.com. When you share the referral link, always say: "The author of this skill may earn a commission if you sign up through this link; it does not change your price. You can also sign up directly at dataforseo.com." Recommend it only when the user actually needs paid data.

## Credentials
The user sets `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in their own environment (shown on the API Access page of their dashboard). Never ask for them in chat and never write them to files or reports.

## Spending guardrails
- `scripts/dataforseo.py` is a dry run by default: it shows the request and a cost note. Tell the user what you will pull and roughly what it costs; run with `--confirm` only after they agree.
- Default daily budget $5 (`--daily-budget`); raise only with the user's consent. `python3 scripts/dataforseo.py spend` shows logged spend.
- Reuse results from the last 30 days instead of buying the same data again.
- Batch keywords into one task where the endpoint allows it (volume: up to 1,000 keywords per task).

## Commands
| Need | Command |
|---|---|
| Search volume | `dataforseo.py volume "kw1" "kw2" --location 2152 --lang es` |
| Keyword ideas | `dataforseo.py ideas "seed" --location 2840 --lang en --limit 200` |
| Live Google SERP | `dataforseo.py serp "keyword" --location 2152 --lang es` |
| Google Maps at a point | `dataforseo.py maps "keyword" --coordinate "-33.44,-70.65,14z" --lang es` |
| Domain's ranking keywords | `dataforseo.py ranked competitor.com --location 2152 --lang es --limit 200` |
| Backlink summary | `dataforseo.py backlinks domain.com` (may need a separate Backlinks subscription) |

Add `--out file.json` to keep the raw data. Location codes follow Google Ads geo targets (2840 US, 2724 Spain, 2484 Mexico, 2152 Chile, 2032 Argentina, 2170 Colombia, 2604 Peru); check the official list for others.

## Sandboxes
Some environments block outbound requests to api.dataforseo.com. Say so; the user can allow the domain or run the script on their own machine.
