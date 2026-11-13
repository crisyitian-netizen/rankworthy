# W2 Keywords, prompts and site structure

Goal: a keyword-to-page map that tells the owner which pages to build, merge or improve, in order of revenue.

## 1. Real demand, not guesses
- AI-suggested keywords have no volume behind them. Use AI to brainstorm seeds and modifiers, then validate in a tool: Search Console (free, your real queries), Google Ads Keyword Planner, Ahrefs free keyword generator, Google Trends (direction of demand), or `scripts/dataforseo.py volume/ideas` (paid, approved). Set the right country and language.
- Without tool data, label numbers as estimates.

## 2. Intent first, transactional first
- Transactional → service / product / category pages. Commercial investigation ("best X", "X vs Y", "X price", "X alternatives", "X for <audience>") → comparison, list and pricing pages. Informational → blog/guides.
- 100 visits for "buy laptop online" beat 1,000 for "laptop". Prioritize terms close to money.
- Start with long-tail terms you can win, then climb to head terms.

## 3. Read the SERP before choosing the page type
Search the keyword in the target country. Record the page types in the top 10 (product, category, long article, list, tool, video) and SERP features (AI Overview, featured snippet, People Also Ask, video, map pack, ads). If the top 10 are all category pages, a blog post will not break in. Use People Also Ask and related searches for H2s and FAQs. `[Practice]`

AI filter: if an AI Overview fully answers the query, expect few clicks; aim to be named in the answer instead.

## 4. Query fan-out and prompts
- AI engines split one prompt into many sub-queries. List the sub-questions a buyer's prompt implies and cover them across the page's sections and FAQ. Do not create one page per sub-query (Google calls that ineffective). `[Google]`
- Prompts are longer than keywords. Mine sales calls, support emails, chats, reviews and Reddit threads for the customer's own words.
- AI Overview follow-ups: search the core queries in the target country's Google, note the follow-up questions the AI Overview suggests, and answer them on the relevant page.

### Prompt groups (for W7)
Collect 2-4 head terms (category, problem solved, use case). Group related questions by intent:
- **Learn** (what is, how does it work)
- **Choose** (best, compare, alternatives, recommendation for a situation) — usually matters most for revenue
- **Do** (how to)
- **Brand** (names you or a competitor; measures reputation, not discovery — keep separate)
Questions from "People also ask" are not logged AI prompts; nobody knows how often a question is asked in ChatGPT. Do not present them as real prompt volume.

## 5. Keyword-to-page map
- The unit is the page. Same intent and overlapping SERPs → same page. Different intent, buying stage or SERP format → separate pages. Similar wording does not mean the same cluster; when unsure, compare the two SERPs.
- For each cluster: existing URL / new page / not now. Priority by revenue fit, then volume, then difficulty.
- Group clusters into **verticals**: one hub page per vertical, sub-pages along the dimensions users search (size, material, use, location, audience). URL slug matches the page name.
- **Internal links feed the hub**: long-tail sub-pages link to the hard head page with descriptive anchors. Manage as a table: source URL / target URL / anchor.

| Cluster | Main keyword | Intent | Volume (source) | SERP page type | Target page | Action | Priority |
|---|---|---|---|---|---|---|---|

## 6. Quick wins and cannibalization (Search Console)
- `scripts/gsc_analyze.py`: non-brand queries at positions ~8-20 with impressions; low CTR for position; impressions with zero clicks. Update the ranking page before writing new ones.
- Cannibalization: with a query+page export, one query spread across several pages → merge or make one page primary and link to it.
- Wording mismatch: if buyers search a different word than the site uses (e.g. "lentes" vs "armazones"), check that SERP's page types and decide whether to adapt an existing page or build one.

## 7. Traffic math
Traffic ceiling ≈ search volume covered × CTR. When pages already rank top for their terms, growth needs more pages that cover more real demand (service pages + topic clusters), not more tweaks.

## 8. International
Do not translate keywords; research each market. Add hreflang (see audit/schema notes) and check indexing per language.

### hreflang rules `[Google]`
Self-referencing tag matching the canonical; every version links back to every other (A→B and B→A) or the set is ignored; language ISO 639-1 (`es`, `en`, `ja`, not `jp`), optional region ISO 3166-1 (`es-CL`, `pt-BR`); a country code alone is invalid; add `x-default` when there is a selector or fallback page.

## 9. Competitor analysis
Confirm the competitor really competes in search (appears repeatedly for your target terms). Look at their top pages and terms, link sources and formats. Conclude in four buckets: learn from, avoid, counter-position against, outrank.
