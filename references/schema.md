# W4 Structured data

Goal: valid JSON-LD that states who you are, what you sell, where, and what the page answers.

## Rules
- JSON-LD in the `<head>` or body; mark up only what is visible on the page. Ratings must come from real reviews. `[Google]`
- Private data stays out: if prices are not public (wholesale), omit `offers.price`.
- Validate with https://validator.schema.org and Google's Rich Results Test. `scripts/site_check.py` lists detected types and parse errors.
- Expectation: Google says structured data is not required for its AI features, but it helps understanding and can earn rich results (stars lift CTR). FAQ rich results are now heavily restricted in Google; FAQPage still documents Q&A structure. `[Google]`
- llms.txt: Google says it has no effect on Google Search or AI features; no other AI vendor has officially confirmed using it. Cheap optional extra, never a priority or a promise. `[Google]` / `[Unproven]`

## Pick by page type
| Page | Types |
|---|---|
| Home | Organization (or LocalBusiness subtype), WebSite |
| Local business / store | LocalBusiness subtype (Store, WholesaleStore, Dentist…), with address, geo, openingHours, telephone, sameAs |
| Service page | Service (provider → Organization), BreadcrumbList |
| Category | CollectionPage + BreadcrumbList |
| Product | Product with brand, image, sku (if public), offers (if public), aggregateRating (if real) |
| Article / blog | Article or BlogPosting with author (Person, with url), datePublished, dateModified |
| Author page | Person with jobTitle, sameAs |
| FAQ section | FAQPage (questions visible on page) |

## Templates (fill only real values)

```json
{"@context":"https://schema.org","@type":"Organization","name":"","url":"","logo":"","sameAs":[""],
 "contactPoint":{"@type":"ContactPoint","telephone":"","contactType":"sales","areaServed":"","availableLanguage":[""]}}
```

```json
{"@context":"https://schema.org","@type":"LocalBusiness","name":"","url":"","image":"","telephone":"",
 "address":{"@type":"PostalAddress","streetAddress":"","addressLocality":"","addressRegion":"","postalCode":"","addressCountry":""},
 "geo":{"@type":"GeoCoordinates","latitude":0,"longitude":0},
 "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"}],
 "sameAs":[""]}
```

```json
{"@context":"https://schema.org","@type":"Product","name":"","image":[""],"description":"","brand":{"@type":"Brand","name":""},
 "offers":{"@type":"Offer","priceCurrency":"","price":"","availability":"https://schema.org/InStock","url":""}}
```

```json
{"@context":"https://schema.org","@type":"BlogPosting","headline":"","datePublished":"","dateModified":"",
 "author":{"@type":"Person","name":"","url":""},"publisher":{"@type":"Organization","name":"","logo":{"@type":"ImageObject","url":""}}}
```

```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":"","acceptedAnswer":{"@type":"Answer","text":""}}]}
```

```json
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Home","item":""},{"@type":"ListItem","position":2,"name":"","item":""}]}
```

WordPress: Rank Math or Yoast can generate most of these; check the output, then add what is missing.
