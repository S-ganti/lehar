# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: static HTML, CSS and vanilla JS with no build step, deployed on GitHub Pages; data files are JSON fetched same-origin. Chosen because the product is a single interactive page, the incumbent prototype is already built this way, and it needs no server or keys. Repository: separate from Risk Radar (Risk Radar stays an internal tool for consulting use).

## Users

Primary: salaried Indians earning roughly ₹15 LPA and above who invest mostly through mutual funds plus a handful of direct stocks. They follow personal-finance creators (CA Rachana Ranade, Akshat Shrivastava, Sharan Hegde and similar), want to make their own calls, and do not have time to research what a news event or a commodity move means for what they own. They check their portfolio on a phone in spare moments and on a laptop when they sit down to think.

Secondary: finfluencers and advisors who show a portfolio to an audience or a client, often by screen-sharing, so the views must read clearly when projected or recorded.

## Product Purpose

Lehar shows a person what their portfolio is actually exposed to. It opens their mutual funds into the companies they hold, adds their direct stocks, and maps every company to the things that move its costs or revenue: crude oil, the rupee, metals, gas, edible oils, interest rates and more. When something moves, they see which of their holdings it reaches and by how much of their money.

Success: a user leaves knowing what they really own (including overlap they did not know about), which factors their money is most exposed to, and what a given move would touch, and they come back when the news moves.

## Positioning

Portfolio apps link headlines to holdings. Lehar shows the causal chain with numbers: the move, the companies that carry it in their cost base or revenue, how much of the user's money sits in them, through funds as well as directly. The look-through runs on each fund's own monthly disclosure and the exposures on annual-report cost structures.

## Operating Context

Users bring: a list of holdings (broker CSV, CAMS statement, or typed values). They return when crude, the rupee or a policy change is in the news. Creators use it on screen while explaining a market move.

## Capabilities and Constraints

- Universe: Nifty 500 stocks (Nifty 200 flagged); 5 mutual funds today (Parag Parikh Flexi Cap; HDFC Nifty 50 Index, Large Cap, Mid Cap, Flexi Cap), from 30 Sep 2026 disclosures. More funds need per-AMC parsing.
- Exposure basis per company is always visible: "company estimate" (cost-base shares from the annual report, 73 companies) or "industry template" (typical for the AMFI industry; a direction and level, not a measured share).
- Market moves come from a daily data file; every move shows its window and as-of date; stale series are marked.
- What-if shows cost or revenue arithmetic only (share x move), never a share-price forecast.
- Regulatory line (SEBI): information and consolidation of public data only. No buy, sell or hold views, no price targets, no model portfolios, no "this stock will fall". The what-if on named stocks is a grey zone pending a legal opinion. Not positioned as education (that would require 30-day-old price data).
- No live stock prices: values are what the user enters. Holdings stay in the user's browser.
- Undecided: pricing (research suggests the tool band, about ₹2,500–5,000 a year), account system, which funds to add next, final name.

## Brand Commitments

Name: Lehar (working name, chosen as "wave / ripple"; may change). Must read as a separate consumer product, not as Risk Radar or a consulting tool.

## Evidence on Hand

- Real data: NSE Nifty 200/500 constituent lists; AMFI industry per ISIN; five funds' 30 Sep 2026 monthly portfolios (parsed totals match each fund's published subtotals); Risk Radar's curated cost-base map for 73 companies; daily market moves in data/latest.json.
- Market research: ../risk-radar/PMF-RESEARCH.md (price bands paid by this segment; Reddit complaint that paid communities only consolidate public information).
- Absent, must not be fabricated: users, testimonials, press, download counts, pricing, partnerships, accuracy or return claims.

## Product Principles

1. Personal before general: every view is about the user's own money, never generic market commentary.
2. Show the basis: every number says where it comes from and whether it is measured or a template.
3. Facts, not calls: explain exposure; never tell anyone what to buy or sell.
4. Honest about freshness: dates and staleness are part of the interface, not footnotes.
5. Clear enough to screen-share: a view should survive being projected in a creator's video.

## Accessibility & Inclusion

Users are not finance professionals: plain language over jargon, Indian number formats (lakh, crore), works on a phone. Colour is never the only carrier of meaning (cost / revenue / both also labelled in text).
