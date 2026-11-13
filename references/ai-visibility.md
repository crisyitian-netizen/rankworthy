# W7 AI-visibility test

Question: when buyers ask AI assistants about this market, is the brand named or cited, and who is cited instead?

## Protocol
1. **Fix a prompt set**: 10-20 neutral prompts (no brand name) from W2 prompt groups, weighted to **Choose** intent; keep branded prompts separate. Save it; never change it silently. A new set starts a new baseline.
2. **Engines**: Google AI Overviews / AI Mode in the target country (e.g. google.cl), ChatGPT (search on), Perplexity; add Gemini, Copilot, Claude if relevant.
3. **Runs**: answers vary; run each prompt 2-3 times per engine when it matters. Logged-out or fresh sessions, target country.
4. **Log** with `scripts/ai_visibility.py init prompts.txt > ai_log.csv`, then fill: mentioned (y/n), cited (y/n, your domain linked), position (order the brand appears), competitors named, cited domains, notes (AI Overview follow-up questions).
5. **Report** with `scripts/ai_visibility.py report ai_log.csv`.
6. **Re-test** monthly with the same set; compare only identical engine × prompt pairs.

## Read the evidence
- Rates by engine and intent: mention rate, citation rate.
- **Gaps**: prompts where a competitor is named and you are not. These drive recommendations.
- **Sources cited instead**: classify the 10-15 recurring ones: list/review article, forum/community, competitor page, your page, reference/media/video. Open the 5-6 that matter: are you in that list, is there a way in (submission form, author, update date)? What question does the competitor page answer that none of yours does?
- AI Overview follow-ups: write sections that answer them.

## Platform differences `[Study]`
Different engines cite largely different sources. Google AI features lean on pages already ranking well; ChatGPT favours recently updated content and list-style pages; Perplexity favours clearly sourced, Q&A-structured pages; Copilot depends on Bing's index.

## Recommend
At most 1-3 actions, each with its evidence (prompt, engine, what was cited), so a non-expert can act. Typical: get into the 2-3 list articles AI keeps citing; create the missing comparison or "how to choose" page; fix crawler access; strengthen the profile/reviews (local).

## Honesty
These are samples, not exposure or traffic. Search Console's Generative AI report shows impressions in AI Overviews / AI Mode (no queries yet). Never compute a trend from runs with different prompt sets.
