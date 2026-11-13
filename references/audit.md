# W1 Audit

Goal: find where the site leaks money and traffic, not list every warning. Output a prioritized task table the owner can act on.

## Steps

1. Run `scripts/site_check.py` on the home page and 3-5 money pages (services, categories, top products, location pages). Without a shell: fetch the pages, robots.txt and sitemap and check the same items.
2. Read Search Console if available (Performance, Pages/Indexing, Core Web Vitals, Generative AI report). Run `scripts/gsc_analyze.py` on the exports.
3. Look at the live search results for 3-5 money keywords in the target country (page types that rank, AI Overview present or not, who is cited).
4. Check the conversion path on a phone: can a buyer act within 5 seconds?
5. Write the task table and the plan.

## Checklist

### 1. Crawl and index
- Search Console verified (Domain property, DNS). Sitemap submitted.
- No accidental `noindex` (meta or X-Robots-Tag), no 5xx, canonical correct, no mass duplicates or parameter URLs. `[Google]`
- Sitemap lists only public, indexable pages with real `lastmod`. Do not fake daily updates. After removing many low-value URLs (e.g. colour variants), fewer indexed pages is expected; watch clicks, not index count.
- Money pages linked from strong pages; important pages within 3 clicks of home.
- Old URLs that still get impressions or links: 301 to the closest page. Spam pages injected by hackers: keep 404/410 and check the Security report. `[Google]`
- Key content present in raw HTML (many AI crawlers do not run JavaScript; Googlebot does). `[Study]`
- Googlebot reads the first 2 MB of HTML; inline base64 images or huge scripts can push content past it. `[Google]`
- Mobile first: most visits are mobile and Google indexes the mobile version. `[Google]`
- Core Web Vitals passing; HTML response fast; images compressed.
- IndexNow set up for Bing and others (Google does not use it); request indexing in Search Console after important changes. `[Practice]`
- Expected lag after changes (Google, 2026): titles/meta ~45-90 min to be picked up; removals/canonical changes 1-3 weeks; site moves 1-3 months; known URLs recrawled ~every 30 days. Canonical fixes can take ~2 weeks to settle. Judge results on that timeline.

### 2. AI crawler access
- Search/answer crawlers decide whether the site can be cited: Googlebot (AI Overviews / AI Mode), Bingbot (Copilot, ChatGPT search depends on Bing's index), OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot. Blocking one removes the site from that engine's answers.
- Training crawlers (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider) do not control search citation; blocking Google-Extended does not affect Google Search or AI Overviews. A site can block training and allow search. `[Google]` / vendor docs.
- Many sites block AI crawlers by accident (old templates, CDN defaults). `[Study]`
- Bing Webmaster Tools verified.
- Google AI features eligibility: page indexed and allowed to show a snippet; no separate AI index. `[Google]`

### 3. On-page
- Unique title and meta description per page; one H1 per page, not duplicated across pages; logical H2/H3.
- Friendly URLs matching the page/category name; depth ≤2 (max 3).
- Transactional content on pages with a CTA; informational content in the blog.
- Image alt text, breadcrumbs, internal links, og:image on key pages.

### 4. Citability (see content.md)
Answer-first sections, self-contained paragraphs, named entities, sourced facts, first-hand data, freshness.

### 5. Authority and E-E-A-T
- Author bylines and author pages (bio, credentials, social profiles), publish and update dates, primary sources, real reviews, About and Contact. `[Google]` Who/How/Why test: who wrote it, how it was made, why it exists.
- Brand search share: in Search Console, brand-term clicks ÷ all clicks. One practitioner benchmark: ~2.4% average, ~10% for strong brands `[Practice]`. Very low means the problem is awareness, not SEO. Very high (most clicks are brand) means existing customers find you but new ones do not; non-brand growth is the job.

### 6. Structured data (see schema.md)

### 7. Experience and conversion (see content.md, UX/CRO)
Practitioner case: a competitor with weaker on-page SEO outranked a store because buying took 1 minute there vs 3 minutes on the store; simplifying checkout recovered rankings `[Practice]`.

## Output

### Task table (sorted by revenue impact, then effort)

| # | URL / area | Issue | Why it matters for revenue | Fix | Owner | Effort | Evidence |
|---|---|---|---|---|---|---|---|

Owner values: "me (with your approval)", "you", "developer". Put items that need the owner (logins, reviews, decisions) in a separate short list.

### Optional score (heuristic for prioritizing, not a prediction)
Citability & AI visibility 25 · Brand authority 20 · Content & E-E-A-T 20 · Technical 15 · Structured data 10 · Platform readiness 10. Say it is a heuristic.

### Plan
30 days: blockers and quick wins. 60 days: content and local. 90 days: off-site and re-test. Name the re-check dates.
