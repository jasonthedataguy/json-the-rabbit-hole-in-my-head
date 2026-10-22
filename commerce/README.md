# Commerce setup

The public `#marketplace` and `#checkout/<edition>` pages are **previews**. No money or buyer data is collected. Edition and paper-goods prices are labeled estimates from the October 2026 strategy PDF, which explicitly says they are unverified hypotheses. The digital manuscripts remain free.

Copy `secrets.template.txt` to `commerce/.env.local` and fill it privately. `.env.local` is gitignored. This template is a collection point for configuration, **not** a live processor. GitHub Pages is static: it cannot safely keep these secrets, create verified order references, receive signed payment notifications, or issue refunds. Never copy filled values into `shared/web/` or `dist/`.

Before enabling preorder, settle the exact edition contents and final price, printer proof and lead time, shipping regions and full cost, refundable deposit amount, buyer notice, refund route, privacy notice, tax treatment, support contact, and payment reconciliation. A buyer must see the total and terms before paying. Store deposits as liabilities until fulfillment. A card/wallet checkout needs an approved merchant connection and server-side payment integration; a personal wallet QR does not prove that an order was paid. A bank QR needs an order-specific reference and reconciliation. A verified personal payOS account may be a route for domestic bank QR; separate merchant onboarding may be necessary for cards, MoMo, ZaloPay and VNPay.

The planned checkout contract is: the client sends only an edition ID and chosen payment method to a server-side endpoint; that endpoint uses canonical approved prices, creates a unique order, provides a hosted checkout/QR, verifies signed provider notifications, stores minimal consented buyer/order data, and reports a paid status only after reconciliation. No client-supplied price or return URL may be trusted. Secrets must be injected into that server's environment. The live offer and checkout stay off until the founder approves the exact buyer-facing page and an end-to-end test has passed for every displayed method.

Sources: *json_product_strategy_solo_ai_restructured_2026.pdf* (pages 9, 16, 21–28, 37, 41–43); [payOS account and API setup](https://payos.vn/docs/api/); [payOS personal account verification](https://payos.vn/docs/huong-dan-su-dung/xac-thuc-to-chuc/); [ZaloPay gateway methods](https://docs.zalopay.vn/docs/guides/payment-acceptance/payment-gateway/intro/).

## Development increment — 23 October 2026 (private branch only)

- `commerce/checkout-policy.json` is an **unapproved, disabled** server-owned policy. The amounts are planning estimates only; approved prices and deposits are `null`. All payment methods and commercial approval gates are disabled.
- `commerce/checkout_contract.py` is a pure, provider-neutral **quote validator**, not a deployed backend or order creator. It accepts only `edition_id` and `payment_method`, and rejects client-side price, payment state, return URL and PII. Even a validated internal quote has `quote_only` status — never `PAID`.
- `tests/test_checkout_contract.py` enforces fail-closed defaults, independent gates, provider configuration, positive amount rules and no payment link or customer storage.
- The static reader checkout offers a transparent edition preview, unresolved costs and a readiness checklist. It offers **no form, payment button, QR code, order reservation, subscription or consent capture**. The checklist is explanatory, not an authorization mechanism.

### Backend sequence, once commercial decisions exist

1. Approve exact physical offer/print specifications, retail and deposit price, expected shipping/taxes and delivery, refund/cancellation language, privacy notice, support and payment methods. Record exact founder authorization and evidence in the controlling commercial run/Jira tickets JSON-32 and JSON-57. Do not change release flags by inference.
2. Choose and verify a PSP and founder-owned merchant identity. GitHub Pages remains static. Choose a separate authenticated HTTPS backend and persistent order store, with secrets in the backend runtime only. Set up restricted operator roles and audit trails.
3. Create **one durable order ID** server-side and use only approved catalog amounts/currency. The browser posts an edition ID and method, with CSRF/abuse controls. Avoid trusting buyer-supplied totals, status, URLs or order codes. Consent and required fulfillment fields must be obtained under a reviewed privacy policy.
4. Create provider-hosted checkout with expiry and a unique reconciliation reference. Return only an approved provider URL; never expose API credentials or mark an unpaid order paid from a browser redirect.
5. Verify webhook authenticity against the PSP's **actual current signature algorithm**, guard retries/replays and compare order identity, amount, currency and provider transaction. Persist idempotent transitions and reconcile against provider transaction status. Browser return/cancel query parameters are *not* payment proof.
6. Build customer support, cancellation/refund, error and timeout handling, refund-liability accounting, retention/deletion and access logs. Test abandoned, double-sent, partial/mismatched, duplicate-notification and refund cases **without moving real funds unless specifically authorized**.
7. After technical QA and a real founder G4 release decision, enable only the methods that actually passed provider onboarding and the documented end-to-end tests. Public book and social posting remain independently gated.

**Provider fact check (23 Oct 2026):** payOS documents that it has no separate sandbox/test environment. Its trial payment flows use the production API and real accounts; therefore do not run even a small-value payOS payment without explicit authorization. See [environment documentation](https://payos.vn/docs/moi-truong-test/), [API](https://payos.vn/docs/api/), and [return URL behavior](https://payos.vn/docs/du-lieu-tra-ve/return-url/). Provider selection is **not** finalized; card/wallet capabilities remain unverified.

Review-only URL routes are `#marketplace` and `#checkout/core`, `#checkout/illustrated`, `#checkout/collector`. This increment is not a public payment or production checkout release.
