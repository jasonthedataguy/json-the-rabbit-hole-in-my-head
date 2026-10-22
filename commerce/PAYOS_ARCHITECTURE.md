# PAYOS-01 — Proposed private checkout architecture (ADR draft)

- **Status:** proposed for founder review; no infrastructure created, no provider connected
- **Date:** 2026-10-23
- **Jira:** [JSON-123](https://jason-agentic-workspace.atlassian.net/browse/JSON-123), [PAYOS-01 / JSON-124](https://jason-agentic-workspace.atlassian.net/browse/JSON-124)
- **Baseline:** [draft checkout PR #2](https://github.com/jasonthedataguy/json-the-rabbit-hole-in-my-head/pull/2)
- **Phase 1:** payOS hosted domestic bank-QR payment for approved physical-book editions only; no cards/wallets assumed

## Decision proposal

**Keep the GitHub Pages reader static and isolated from all checkout secrets.** Add a minimal server-side HTTPS order service on **Cloudflare Workers + D1** as the leading low-cost candidate, subject to account/contract/cost/security review before provisioning. Use plain HTTPS requests to payOS merchant APIs with documented HMAC signing and avoid assuming a particular Node SDK works in Workers. A provider adapter can be swapped without altering the reader or canonical order records.

Rationale: existing public book routes and illustration assets remain untouched; Worker Secrets provide non-public credential bindings; D1 provides durable relational orders, transaction uniqueness constraints, audit ledger and idempotent webhook transitions. Worker/D1 free quotas may suit a small pilot, but quotas/overages, availability, data residency, privacy and dispute handling must be checked before adoption. No paid hosting/domain/account is authorized by this document.

Alternatives requiring assessment if Cloudflare is unsuitable: independently hosted Python FastAPI + PostgreSQL, or other HTTPS functions with a transactional store and separately managed secrets. **Do not deploy the legacy `checkout_contract.py` as an HTTP server without designing auth, durable storage and request controls.** It is a pure reference validator, not production infrastructure.

## Trust and data flow

```text
Visitor ── HTTPS ──> existing GitHub Pages static reader
                           │
                           └── choose edition/method ──> PRIVATE HTTPS Worker
                                                          │ exact-origin CORS
                                                          │ canonical approved catalog
                                                          │ disabled until approvals
                                                          v
                                                     D1 order ledger
                                                          │ durable orderCode
                                                          │ idempotent create
                                                          v
                                              payOS merchant payment request API
                                                          │ signed, server-only
                                                          └── hosted payOS URL
                                                             └── customer's bank app
                                                    (no raw account/QR construction by us)

payOS signed webhook ──> Worker webhook endpoint ──> signature verification
                                                       + orderCode/link/amount/currency
                                                       + idempotent D1 state transition
                                                       + provider reconciliation
                                                       + restricted operator review

payOS browser redirect ──> book return/cancel screen ──> Worker order-status endpoint
                                                                  └── sanitized status only
```

No local browser amount, price, order status, bank account, redirect URL, API signature or checksum is authoritative. A return URL showing `status=PAID` **never** makes an order PAID. Provider reconciliation with a verified webhook and durable payment status is the source of payment truth.

## API sketch (not yet implemented)

| Method | Proposed route | Public contract | Notes |
|---|---|---|---|
| POST | `/v1/checkout-sessions` | Strict `{edition_id,payment_method}` plus only separately approved fulfillment fields/consent | Server calculates final total, deposit, shipping/tax and validates release gates; rate-limited, abuse/CSRF guarded |
| GET | `/v1/orders/{public_token}` | `pending/paid/cancelled/expired/review_required`, no banking or private buyer fields | Opaque unpredictable token, no sequential enumeration; no-store headers |
| POST | `/v1/webhooks/payos` | Official provider webhook body | Verify payOS documented HMAC scheme before mutation; do not authorize via browser Origin alone |
| POST | `/v1/cancel-requests` | Opaque token + approved cancellation/auth proof | Cancelling an unpaid payment link is **not** refunding a paid order |
| Private | admin/reconciliation operations | Restricted owner-only access and audit | No public admin API or automatic payouts |

**Checkout recipient secrets:** `PAYOS_CLIENT_ID`, `PAYOS_API_KEY`, `PAYOS_CHECKSUM_KEY` are encrypted Worker Secrets in a founder-controlled Cloudflare account. Use `wrangler secret` / dashboard; exclude `.dev.vars*` and `.env*` from version control. Never store values in Jira, PR comments, GitHub Pages, screenshots or chat.

**Callback URL design:** configure absolute allowlisted HTTPS base URLs on the backend, currently based on `https://jasonthedataguy.github.io/json-the-rabbit-hole-in-my-head/`; do not accept return/cancel URLs from the client. payOS appends query data before SPA routing. The reader will safely route on a stable root-path query indicator to a pending/confirmation view, with canonical status fetched from the backend; never put an authentication token in UTM/referrers. Revisit exact callback URL behavior in mocked and authorized end-to-end QA before activating.

## Durable order ledger (migration in PAYOS-05)

- `orders`: internal UUID/ULID, unique positive provider `orderCode` (integer constraints verified against payOS API), random separate public status token hash, SKU/catalog revision snapshot, amount/currency, shipping/tax/deposit split, settlement/refund liability, created/updated/expiry, state, gateway link ID
- `payment_events`: immutable event ID/provider reference, linkage to order, verified signature result, normalized event type, arrival time, unique deduplication key, redacted payload fingerprint; never persist raw bank credentials
- `refunds`: refund request, method, authorized operator, gross/net/fees, bank verification reference, timestamps, status and evidence pointer (redacted); no auto payout
- `audit_events`: actor/source/action, before/after state, time and limited structured reason, retention schedule

Transitions must be conditional/idempotent in the database; never turn PAID back to PENDING on out-of-order callbacks; mismatches and double payment go to manual review, not fulfillment. A payment link expiration is distinct from a completed bank transfer/refund.

## Threat model and controls

| Threat | Minimum control |
|---|---|
| Tampered price/edition/method | Server-owned approved catalog; strict request schema; no arbitrary client amounts |
| Public API abuse or invoice spam | Request validation, rate limiting/abuse checks, origin-aware CORS + appropriate CSRF defense, idempotency keys and limit retries |
| Forged webhook or wrong-amount payment | Official payOS signature verification using the **payment-request webhook algorithm**, constant-time comparison, amount/currency/link match, read-back/reconciliation as needed |
| Duplicate or reordered webhook | Unique provider references + atomic state transitions + replay-safe processing |
| Untrusted browser return | Server status lookup only; query params never payment proof |
| Secret/bank/PII disclosure | Encrypted Worker Secrets, least privilege, minimal retention, redacted logs, restrictive status API and restricted admin |
| Canceled/expired but later settled | Manual reconciliation; no unverified automatic fulfillment or refund |
| Free-plan quota exhaustion/outage | Fail closed: do not confirm payment without verified durable order state; alert and queue reconciliation |
| Unapproved commercial release | Independent founder G4 decision; existing `checkout-policy.json` defaults disabled and payment methods empty |

## Testing and rollout sequence

1. **PAYOS-01** ADR/source audit. Record exact infrastructure decision and founder cost/identity choices.
2. **PAYOS-02 / JSON-57** verify payOS eligibility, bank-QR channel, fees, secret custody without sharing credentials.
3. **PAYOS-03** approve actual product/deposit/terms from printer and policy; estimates not chargeable.
4. **PAYOS-04..10** implement backend, durable orders, hosted-link adapter, signed webhook, reader return/status, operations and refunds **in private mock mode**.
5. **PAYOS-11** run mock provider E2E, adversarial callbacks, CI/unit/security, manual mobile browser tests and rollback plan.
6. **PAYOS-12** request separate founder approval for live payOS transaction with specified amount/recipient and refund; payOS has no separate sandbox. Only after evidence and distinct founder G4 approval may paid checkout ever be publicly enabled.

CI on book PRs runs tests/build/link validation without deploying GitHub Pages; no production backend credentials in CI. Rollback: set server and reader `checkout_enabled=false`, disable new sessions, keep webhook receiving existing settled events, preserve ledger and manual reconciliation; never delete pending customer orders.

## Open decisions before PAYOS-01 can be considered approved

- [ ] Confirm founder controls (or will create) a Cloudflare account; authorize any infrastructure provisioning separately.
- [ ] Confirm Cloudflare Workers+D1 is acceptable under the real pilot limits/cost, data-handling requirements and uptime needs; otherwise record selected alternative.
- [ ] Confirm the canonical deployed public reader origin; a future `jsonrabbithole` domain requires separate purchase/DNS approval and later callback updates.
- [ ] Confirm payOS account/channel, settlement eligibility and fee/refund operations (PAYOS-02; may remain pending while mock coding proceeds).
- [ ] Approve implementation scope and evidence needed to close architecture task. Founder G4 **not** implied.

## References checked 23 October 2026

- payOS API: https://payos.vn/docs/api/
- payOS webhook: https://payos.vn/docs/du-lieu-tra-ve/webhook/
- payOS signature guidance: https://payos.vn/docs/tich-hop-webhook/kiem-tra-du-lieu-voi-signature/
- payOS return URL: https://payos.vn/docs/du-lieu-tra-ve/return-url/
- payOS test environment warning: https://payos.vn/docs/moi-truong-test/
- Workers runtime limits: https://developers.cloudflare.com/workers/platform/limits/
- Workers Secrets: https://developers.cloudflare.com/workers/configuration/secrets/
- D1 pricing/quotas: https://developers.cloudflare.com/d1/platform/pricing/
