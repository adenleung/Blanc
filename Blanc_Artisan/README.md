# Blanc Artisan — five-page floral storefront

A rebuilt site based on the supplied Blanc_Artisan_Redesign(1).zip. It includes all real local bouquet photographs, 23 source-mapped products, published variant snapshots, five separate main pages, internal product pages, server-backed cart, custom/contact enquiries, order records, delivery/stock reservations, owner workspace and a Stripe Payment Element integration. Ordinary purchases stay inside this new site; there are no links to the old store for checkout.

**Live payments are disabled initially.** Stripe credentials, authoritative prices/stock, delivery capacity and owner-approved policies were not supplied. A public catalogue snapshot is not live inventory. The site does not simulate payment success or order confirmation.

## Pages

- `/` — editorial homepage, bouquet selection, occasions, custom feature, delivery assistance, money bouquets, attributed customer paraphrases, bridal feature and Frequently Asked Questions.
- `/shop` — search by bouquet/flower description, category, starting-price budget and price sorting; visible result count, filters, reset and empty state.
- `/custom-and-weddings` — bespoke/wedding services and a genuine database-backed enquiry form.
- `/about` — factual brand introduction and real photography.
- `/contact` — support, genuine contact submission and Frequently Asked Questions.

Additional functional routes: `/products/[source-slug]`, `/cart`, `/checkout`, `/order-confirmation`, `/admin` and five `/policies/*` pages. These are additional commerce routes, not five more marketing pages.

## Install and preview

Use Node.js 24+ and pnpm 11.25.0. Install pnpm if necessary, then run from the extracted project root:

```sh
pnpm install --frozen-lockfile
pnpm run build
```

Initialise the local D1 database once, applying these migrations in order:

```sh
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0000_silent_ironclad.sql
node --import ./scripts/sites-env.mjs ./node_modules/wrangler/bin/wrangler.js d1 execute DB --local --config dist/server/wrangler.json --persist-to .wrangler/state --file drizzle/0001_brainy_amazoness.sql
pnpm run dev
```

Use the localhost URL printed by the server (normally port 5173 on a personal computer). `pnpm start` previews the built Worker instead. Do not open the HTML as a file: the commerce API needs the Worker and database. Use `.wrangler/state` consistently; do not replay applied migrations. In ChatGPT's managed Sites environment, use the supported `sites-preview` supervisor through the advertised browser skill; do not launch a substitute preview.

The ZIP includes source, public assets, SQL migrations, dependency locks and setup documents. Dependencies/build output are regenerated, so node_modules and secret/runtime files are excluded.

## Runtime configuration

Create an ignored `.dev.vars` for local development; set the corresponding values in the hosting platform's runtime settings for deployment:

- `ADMIN_EMAILS`: comma-separated owner email allowlist. Hosted owner APIs use Sites' trusted `oai-authenticated-user-email` identity header. Never expose admin routes through a proxy that accepts that header from visitors. Local development uses the starter's mock identity; that is not a production login.
- `STRIPE_PUBLISHABLE_KEY`: the matching test or live publishable key.
- `STRIPE_SECRET_KEY`: secret, server-only.
- `STRIPE_WEBHOOK_SECRET`: secret for this endpoint and mode.
- `RESEND_API_KEY`: secret, for actual confirmation email delivery.
- `EMAIL_FROM`: an owner-approved sender at a verified Resend domain.

Do not put secrets in `public/`, Git, browser JavaScript, source JSON or command arguments. Stripe publishable keys are returned to the checkout browser; secret keys are never returned. No keys are bundled.

The current Sites project remains owner-private. The owner allowlist is configured for the existing project. A commercial launch requires an explicit audience/domain decision and a publicly reachable, verified Stripe webhook. Private preview access can prevent Stripe from reaching the webhook; verify delivery before enabling live payments. Ordinary customer access and paid fulfilment must not depend on a preview sign-in.

## Owner approval and catalogue import

The supplied snapshot is preserved in `public/products.json`; source URLs, collected timestamps, raw source text and gallery mappings are retained. `COLLECTION_REPORT.json` documents collection. `public/features.json` records money/bridal photograph sources. Operational source text is archival, not a promise shown to customers.

For automatic owner-authorised WooCommerce import, set `WOO_ORIGIN`, `WOO_CONSUMER_KEY` and `WOO_CONSUMER_SECRET` as local environment variables, using read-only REST credentials. Then run:

```sh
pnpm run catalogue:import
```

The importer paginates products and variations, downloads HTTPS JPG/PNG/WebP images locally, maps existing source URLs to stable storefront IDs, preserves authoritative variation IDs/prices/options and imports numeric stock only when WooCommerce actually manages it. It writes `data/owner-import.json` and `data/import-report.json`. It never activates stock, guesses a price from a range or uploads anything. Review unsupported/plugin add-ons and missing quantity warnings. Composite/plugin-priced products require a dedicated integration rather than a guessed price. New imported photographs require owner image review.

Without credentials, use `data/owner-setup-template.json` as a starting point. Owner access is needed for complete private variants, inventory, add-on plugin data and continuing synchronisation. The public snapshot includes only accessible published combinations; unavailable combinations remain unpurchasable.

In `/admin`, open Delivery & catalogue and paste the completed JSON. Required fields:

- Delivery `cutoff` as owner-approved Singapore `HH:MM`; `baseFee` and surcharge `amount` in integer SGD cents. Zero is accepted only when explicitly approved. `excludedPrefixes`, `surcharges` and `blackoutDates` are centrally stored.
- Five full policy texts in `delivery.policies` (`delivery`, `substitution`, `refunds`, `privacy`, `terms`). Set `policiesApproved` only after owner approval. Actual policy text is published on the policy routes. Placeholder text does not enable payment.
- Each product's complete current options/variant prices, `leadDays` integer and `sameDay` boolean. `inStock:false` and `enabled:false` prevent ordering. Do not rearrange variant arrays while reservations exist: inventory IDs are mapped to the imported variant index.
- `inventory`: objects with `id` such as `2:0` (product 2, variation index 0) or `18:simple`, and a verified `available` integer. This is total available stock including current reservations; `reserved` is system-managed. Unmanaged Woo stock needs owner-approved capacity. Stock cannot be reduced below reservations.
- `slots`: unique `id`, ISO `date`, customer-readable `label`, integer `capacity`. Capacity is measured in **bouquets**, not orders. `used` is system-managed. Existing capacity cannot be reduced below committed/reserved bouquets. Set capacity to zero to close an unused slot; blackouts override eligibility. Holiday-specific slots/blackouts are entered explicitly.

The source contained incompatible delivery windows/cutoffs, free-delivery claims and S$10 surcharges/exclusions. No schedule or fee was chosen arbitrarily. All live rules come from this single approved configuration.

**This release uses D1 as its operational order/stock authority after import. It does not continuously sync WooCommerce orders or shared flower inventory.** Keep the old checkout disabled at cutover, or implement a shared inventory integration before accepting concurrent orders. A periodic import must not overwrite reservations or reset committed stock. Do not publish stale catalogue stock as live inventory.

## Cart and payment behaviour

Cart data persists in D1 using a secure HTTP-only cart cookie. Each line keeps the exact bouquet, variant, option choices, quantity and gift message. Quantity changes, removals and message edits persist across pages. Prices are resolved on the server. The checkout revalidates against approved catalogue data and requires customer review if a saved price changed.

First release: one delivery address, recipient and slot for the whole order; separate gift messages per bouquet. Use separate orders for different recipients/dates. No customer account is required.

Checkout collects buyer email/phone separately from recipient name/phone, Singapore address and six-digit postal code, unit, instructions and eligible slot. It displays subtotal, confirmed delivery fee and final total before payment. This release treats owner catalogue prices as tax-inclusive; GST registration/invoice rules must be confirmed before launch. It does not calculate an invented tax or discount.

Stripe **Payment Element with Checkout Sessions (`ui_mode: elements`)** provides an embedded ordinary card payment flow. Current official documentation was checked on 7 October 2026. Cards are the initial enabled payment type; bank authentication may open an authorisation step. Other methods require account eligibility, explicit enablement and tests. No guarantee is made that every payment stays on-page. Official references:

- https://docs.stripe.com/payments/accept-a-payment?payment-ui=elements&api-integration=checkout
- https://docs.stripe.com/api/checkout/sessions/create
- https://docs.stripe.com/webhooks

The server reserves all inventory and delivery capacity in one D1 transaction before creating the Session. Incomplete reservations roll back. Stable order/session idempotency handles retry of an open attempt without duplicate charges. Card failures can retry the same open Session. Verified expiry releases holds; a new attempt can then be created. A new cart revision permits a genuine later purchase rather than reusing a paid order.

Only verified paid status, matching currency/amount/order metadata, queues fulfilment. Browser success alone is insufficient. Raw-body signed webhooks verify timestamp/HMAC, record processed events and apply stock/payment effects once even under concurrent duplicate events. The protected confirmation route also verifies the Session server-side. Unpaid attempts remain pending. A late payment after holds were released is marked `review_required` instead of promising capacity.

Configure `/api/webhook` for `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.expired`, `refund.created`, `refund.updated` and `refund.failed`. Reconcile pending orders in the owner workspace if a webhook is delayed. Never release an unknown provider attempt simply because its API call timed out. For a rare Session-create timeout before its reference was saved, find the Session in Stripe using the order metadata and securely POST its reference to `/api/admin/attach-session`; the backend checks it before attaching/reconciling. This requires owner access and cannot be done by customers.

Full refunds are available in the owner dashboard using Stripe idempotency; pending/succeeded/failed refund events are reflected separately from fulfilment. Refunds do not automatically restock perishable bouquets or reopen delivery capacity. Partial refunds and disputes require Stripe Dashboard handling; partial refund events are recorded, but a dedicated partial-refund editor and dispute workflow are not included.

## Enquiries, dashboard and emails

Custom/contact forms genuinely write to the owner enquiry inbox and return a saved reference. They do not claim a florist has read or replied. WhatsApp uses the sourced +65 8580 9956 number as optional support, with customer-entered text prefilled; no message sends automatically. Weddings/custom products are consultation-first, not a fabricated priced checkout.

`/admin` shows paid and pending orders, selected options, quantities, gift messages, recipient/delivery details, a delivery-date filter, fulfilment updates, full refunds, enquiries and configuration editing. Payment status is distinct from queued/preparing/dispatched/delivered/delivery_failed/cancelled/review_required.

Paid orders create a confirmation email outbox entry. With a verified Resend sender configured, the backend attempts delivery; failed attempts remain queued. The owner can resend queued confirmations with the dashboard button. Messages contain order reference, items/options/messages, recipient/address, date/slot, total and support number. No email is claimed sent before the provider accepts it. Automated scheduled retries and fulfilment-update emails are later additions; owner monitoring is required initially.

## Verification and commercial launch checklist

See `VERIFICATION.md` for actual results and remaining checks. Run:

```sh
pnpm test
pnpm exec tsc --noEmit
pnpm run build
```

Optional DOM interaction suite:

```sh
cd qa
npm ci
cd ..
pnpm run test:dom
```

Before commercial launch, render at 360, 390, 768 and 1440px and check hero/gallery crops, actual fonts, two-column mobile grids, no horizontal overflow, cart/filters/empty states, footer, forms and checkout. Test real keyboard focus/escape/dialog trapping, accessible labels/errors, reduced motion, all assets and browser console. Test Stripe's successful, declined, 3-D Secure, pending, duplicate webhook, expiry and refund paths with owner test keys; verify actual email arrival and private/public endpoint behaviour. No browser screenshots or Lighthouse claims are included.

## Remaining owner decisions / integrations

1. Complete authoritative variants, prices, inventory and product-specific same-day/lead-time approvals; confirm whether money bouquets remain consultation-only.
2. One approved cutoff, fees, exclusions/surcharges, slots/capacity, holidays, failed-delivery policy and custom/bridal notice.
3. Final policies, tax treatment, business/legal details, approved support details and enquiry monitoring.
4. Stripe account/mode, verified webhook, production domain/public audience and live-payment acceptance testing.
5. Verified email sender and scheduled retry/notification policy.
6. Inventory cutover or continuing WooCommerce/shared-capacity synchronisation.
7. Owner-reviewed occasion assignments and any review publication permissions. No review counts, ratings, awards or guarantees are invented.
8. Public location/appointment rules before adding Google Maps. No private studio/residential address is exposed.
9. Real browser/mobile accessibility and visual sign-off.

The integrated catalogue/backend, transaction routes, Stripe, owner dashboard, email service and ongoing operations are additional e-commerce scope beyond a five-page S$999 starting business website package. No new price or delivery date is implied by this rebuild. Wishlist, accounts, discounts, abandoned-cart marketing, multilingual shopping and automated fulfilment emails are not required for the first release.
