# Rebuild verification — 7 October 2026

This report supersedes the previous static-shortlist verification.

## Actual checks

- Supplied project and catalogue inspected; real photographs/source mappings preserved. Existing image contact-sheet inspection informed the hero, money and bridal selections.
- 14 Node tests passed against SQLite with a D1-style transactional adapter: local catalogue/gallery assets and all 23 product routes, five main routes, exact option/variant pricing, invalid quantities/options, stock gating, Singapore cutoff/blackout/lead-time rules, signed webhook body/timestamp validation, cart persistence, owner access enforcement, stored enquiries, disabled unconfigured payment, server totals, retry idempotency, stock/capacity rollback, price-change review, concurrent paid-event deduplication, unpaid/amount-mismatch rejection and expiry release.
- 7 jsdom tests passed: shop filters/empty/reset, exact product option price and cart/message persistence, database failure without fake added success, mobile drawer aria synchronisation, real enquiry API submission and optional WhatsApp, disabled unconfigured checkout, gallery controls and modal labels. Dialog/browser APIs are stubbed; this is DOM logic testing, not browser rendering.
- Production framework build and JavaScript syntax checks passed. TypeScript `tsc --noEmit` passed.
- Existing contrast calculation: near-black on ivory 16.10:1; muted copy 6.03:1; botanical copy/focus 6.02:1. Browser/third-party payment element contrast was not measured.

## Not tested / remaining launch work

No advertised browser-rendering capability was available in this managed runtime. No substitute browser or preview server was launched. No screenshots at 360, 390, 768 or 1440px were produced. Actual font appearance, layout/crop/overflow, real keyboard focus/trap, touch, screen-reader behaviour and browser console/network QA remain unverified. No Lighthouse/Core Web Vitals/performance claims.

Stripe calls in automated tests are controlled mocks, not transactions with a merchant account. Stripe credentials, approved delivery/stock/policies and email credentials were not supplied. Live payments remain disabled. Real Stripe/3-D Secure/webhook/refund and email-arrival testing is required. The WooCommerce importer is implemented but has not run against owner credentials. D1-style SQLite tests do not replace production D1 race/integration testing.

Owner setup, public webhook reachability and production cutover must be completed before commercial orders are accepted. See README for supported behaviour and integration limits.
