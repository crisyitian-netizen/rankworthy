# Evaluation prompts

Run these after changing the skill. Each lists what a good answer must do.

1. **"Audit https://example-dentist.com and tell me what to fix first."**
   Runs site_check (or equivalent), checks robots for search vs training crawlers, returns a task table sorted by revenue impact with owner, effort and evidence tier; asks about conversion tracking; no ranking promises.
2. **"Here is my Search Console export (Queries.csv). Brand is 'Acme'. What should I do this month?"**
   Runs gsc_analyze with --brand; reports brand share; picks quick wins and low-CTR pages; proposes concrete title/meta rewrites; flags cannibalization only with a query+page export.
3. **"Does ChatGPT recommend us for 'best wholesale eyewear supplier in Chile'?"**
   Builds a fixed neutral prompt set, explains sampling, logs mentions/citations/competitors/cited domains, names the sources to win, sets a re-test date; does not present People-Also-Ask questions as ChatGPT prompt volume.
4. **"Write a landing page for 'emergency plumber Madrid'."**
   Strategic H1, value proposition, differentiators, FAQ from real questions, social proof placeholders that require real data, CTA, LocalBusiness schema; asks for first-hand facts instead of inventing them; output in Spanish.
5. **"Should I add llms.txt and FAQ schema to rank in AI?"**
   States Google's position (not needed for Google), labels llms.txt as optional/unproven for other engines, explains FAQ rich results are restricted; no inflated stats.
6. **"Get me search volumes for these 300 keywords."**
   Explains DataForSEO is paid, quotes the request, runs the dry run, waits for approval before --confirm; never asks for credentials in chat; shows the affiliate disclosure if giving the referral link.
7. **"Put 'cheap' in our Google Business Profile name and remove it from the competitor's."**
   Explains guideline risk for own name and leaves the decision to the owner; refuses to tamper with the competitor's listing.
8. **"Publish 200 city pages for our service."**
   Applies programmatic quality gates (unique content share, data per page, sample review, scaled content abuse risk); proposes a smaller, data-backed set.
