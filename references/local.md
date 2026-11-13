# W5 Local SEO and Google Business Profile

Local SEO = Google Maps / local pack + local organic pages. They work together. Ranking factors: **relevance** (categories, description, site content), **distance** (not controllable), **prominence** (review count and rating, citations, site authority). `[Google]` Local usually moves faster than national SEO because you compete with a handful of nearby businesses. Target "service + city", not national head terms.

## 1. Diagnose vs the top competitors
- Find the listing; run the main 1-3 customer keywords (not the brand name) near the business.
- Rank grid: 3×3 is usually enough; 5×5 only for wide service areas (paid via `dataforseo.py maps` with coordinates, or a grid tool the user has). Separate "ranks only at the storefront" (prominence problem) from "ranks across the area" (basics fine).
- Compare with the top 2-3: primary category, extra categories, review count, recency of last reviews, average rating, owner reply rate, photo count, hours completeness, claimed status, website link. The biggest gaps are the priorities.
- The listing's website link should go to that location's page on the site (with UTM), not a homepage or old domain. Chains: one profile and one page per location.

## 2. Business Profile fixes
- **Primary category** is the strongest field; pick the one that brings revenue. Add every truly relevant secondary category (choose only from Google's list of ~3,800).
- Description written for people, naturally including core services, including ones not covered by name or categories.
- Service area only where you really operate ("pain test": would someone really hire you there?). Fill services and products.
- Verified phone, website with https, chat/WhatsApp, social links, hours. **Set holiday/special hours**; wrong hours create bad reviews.
- **Change name and categories rarely**: edits can trigger re-review. Hours and posts are fine to change.
- Name: keyword-stuffed names often rank better, and competitors may strip yours (one practitioner dropped from #1 to #11 when a competitor's suggested edit removed the keyword) `[Practice]`. It breaks Google's naming rules and risks suspension. Explain the risk; the owner decides. Never edit or report competitors' listings.
- Posts and photos weekly: not a direct ranking lever, but they lift conversion and show the business is active. `[Practice]`
- Q&A: seed and answer real questions.
- UTM on the website link (`utm_source=gmb&utm_medium=organic`) and track calls, direction requests and leads in GA4 / the profile insights.

## 3. Review system
- Unhappy customers review on their own; happy ones need asking. Ask at the moment of peak satisfaction, automate where possible, use the profile's "ask for reviews" link or QR code.
- **Steady pace beats a big old pile**; many reviews at a slightly lower rating often beat a few perfect ones. `[Practice]`
- Reviews mentioning the service or product help (Google quotes review text in results). You may ask customers to mention what they bought; never write or fake reviews, never offer incentives that break Google's rules.
- Reply to every review within 24 hours, negative ones faster; write for future readers.
- Kit to hand the owner: short request message in the customers' language, direct review link, QR, reply templates for 5/3/1-star reviews.

## 4. NAP and citations
- One master record: name, address, phone, website, written identically everywhere (abbreviations, http vs https, "Av." vs "Avenida").
- Use the same record in local and industry directories and social profiles; merge duplicate listings (e.g. user-created TripAdvisor pages).
- One brand name across site, profile and directories also helps AI engines treat them as the same entity.

## 5. Location pages
One page per real served city/area: local keyword, local cases and reviews, LocalBusiness schema, embedded map, link to and from the profile. No mass-generated pages that only swap the city name.
