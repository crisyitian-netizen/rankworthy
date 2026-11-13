# Rankworthy

**SEO & GEO agent skill for Claude.** Gets your site ranked in Google and named in ChatGPT, Google AI Overviews and Perplexity, and measures whether it brought customers.

[Español](README.es.md) · [中文](README.zh.md)

## Why another SEO skill

Most SEO skills score your site. Rankworthy is built around the owner's questions: *what should I fix first, will it bring customers, did it work?*

- **Business results first.** Every finding names the leads, calls or orders it affects. If conversions are not tracked, that is fix #1.
- **Safe on live sites.** Backup → approval → change → log → scheduled re-check. Private data (e.g. wholesale prices) never leaks into pages, schema or llms.txt.
- **Evidence-labelled.** Each recommendation is tagged `[Google]`, `[Study]`, `[Practice]` or `[Unproven]`. No invented stats, no "llms.txt will save you".
- **Zero setup, free data first.** Works in a normal Claude chat. Uses Search Console, GA4, PageSpeed and the live web. Paid data is optional and every spend is quoted first.
- **Local and multilingual.** Deep Google Business Profile and reviews workflow; works in any language, with Spanish and Chinese docs.
- **Before/after loop.** Baselines, a fixed AI-prompt set and a change log, so you can tell what worked.

## What it does

| Workflow | You get |
|---|---|
| Audit | Task table ranked by revenue impact, with owner and effort |
| Keywords & prompts | Keyword-to-page map, quick wins, cannibalization, AI prompt groups |
| Content | Publish-ready pages and articles with answer-first blocks and CTAs |
| Schema | Valid JSON-LD for your page types |
| Local SEO | Business Profile fixes vs top competitors, review kit, NAP record |
| Off-site | Where AI cites others but not you, and how to get there |
| AI visibility | Fixed prompt set, sampled log, gaps, re-test plan |
| Reporting | Owner-friendly report vs baseline, change-log verdicts |

## Tools (Python 3, standard library only)

```bash
python3 scripts/site_check.py https://example.com            # SEO + AI-crawler check of a page
python3 scripts/gsc_analyze.py Queries.csv --brand "acme"     # Search Console export analysis
python3 scripts/ai_visibility.py init prompts.txt > log.csv  # AI visibility test log
python3 scripts/ai_visibility.py report log.csv
python3 scripts/dataforseo.py volume "keyword" --location 2840 --lang en   # optional, paid, dry run by default
```

## Install / where it works

Rankworthy is a standard [Agent Skill](https://agentskills.io) (`SKILL.md` + `references/` + `scripts/`), so it is not tied to one app.

| Where | How | Notes |
|---|---|---|
| Claude Code | copy the folder to `~/.claude/skills/rankworthy/` (or `.claude/skills/` in a project) | Full power: scripts run locally and can fetch any site |
| Claude apps (web, desktop, mobile) | zip the folder and upload it under Settings → Capabilities → Skills | Needs code execution on; the sandbox may block fetching some sites, so paste HTML or upload GSC exports instead |
| Claude API / Agent SDK | upload as a custom skill via the Skills API | Same as above |
| Codex, Cursor, Gemini CLI, Copilot, OpenCode and other agents that read `SKILL.md` | put the folder in their skills directory | Instructions work everywhere; scripts need Python 3 |

No API keys are needed to start. Paid data is opt-in.

Then ask: *"Audit example.com and tell me what to fix first"*, *"Does ChatGPT recommend us for 'best X in Madrid'?"*, *"Rewrite this landing page"*.

For long-term work, fill in `references/project-profile-template.md` for your site.

## Paid data (optional)

Rankworthy can pull search volume, SERPs, Google Maps grids and backlinks from [DataForSEO](DATAFORSEO_REFERRAL_LINK) (pay as you go, no subscription). *Affiliate disclosure: the author may earn a commission if you sign up through this link; your price is the same. You can also sign up directly at dataforseo.com.*

## Credits

Methods draw on Google Search Central, practitioner courses and several open-source projects (claude-seo, open-seo, seomachine, geo-seo-claude and others). See `references/sources.md`. No code was copied.

## License

MIT
