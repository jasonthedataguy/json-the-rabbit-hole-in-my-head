# PAYOS-02 — Merchant onboarding and eligibility checklist

**Status:** In progress, account and channel not yet verified. This is a safe onboarding guide, not an account-registration action or permission for a transaction. See [JSON-125](https://jason-agentic-workspace.atlassian.net/browse/JSON-125), [JSON-57](https://jason-agentic-workspace.atlassian.net/browse/JSON-57), and [accepted PAYOS-01 ADR](PAYOS_ARCHITECTURE.md).

## First founder check

Confirm whether a payOS account already exists. If yes, privately check verification status, connected bank, payment-channel name, receiving-bank ownership and current active tariff. If no, begin with the official registration portal:

1. Open **https://my.payos.vn/** in a private, trusted browser and register using a founder-controlled email. Verify the email and enable available account protection.
2. Follow payOS's **organization verification** workflow. payOS documents both registered businesses and individuals/households. Enter CCCD/business documents **only into the payOS-controlled onboarding flow**.
3. Add an approved settlement bank account that matches the verified person/entity. Do not paste account numbers, national-ID images, OTPs or bank-login data into GitHub, Jira or ChatGPT.
4. Check **Kênh thanh toán** (payment channels). Create or use a payment channel only through the founder account; confirm it supports payOS-hosted bank-QR merchant APIs and webhooks. Review the exact terms and prospective fees before committing any paid plan.
5. **Do not copy Client ID, API Key or Checksum Key into chat, source code or Jira.** At the backend-deployment stage they will be set as Cloudflare Worker Secrets in the founder-controlled Cloudflare environment. No secrets are required to build/mock-test the API.
6. Do not generate or pay a real payment link during onboarding. Real-money QA requires separate scoped founder approval at PAYOS-12.

## Public, non-sensitive evidence to capture in JSON-125

- [ ] Account present? yes/no; owner verified? yes/no/pending (never store identity document/number)
- [ ] Entity type: individual/household/business, if appropriate for the approved merchant arrangement
- [ ] Bank connected? yes/no/pending; permitted bank/channel type (bank account digits and personal details omitted)
- [ ] Merchant payment channel created/verified? yes/no/pending, with hosted QR + API + webhook supported
- [ ] Actual plan/fee/transaction quota and VAT confirmed from dashboard, provider quote, or current bank/channel plan (attach redacted terms only)
- [ ] Refund workflow, cancellation semantics, settlement/receipt availability, and support contact confirmed
- [ ] Founder confirms any future paid provisioning separately; no charges authorized now
- [ ] Ready for **mock integration only** (no credentials in CI and no real requests)

## Provider-specific points that must be confirmed

- payOS's technical [environment guidance](https://payos.vn/docs/moi-truong-test/) currently says there is **no separate sandbox** and that integration tests may use production APIs/real bank transfers. Other marketing pages may use the term `sandbox`; do not rely on it until payOS support confirms exact isolated credentials and behavior. Fake-provider tests are our default.
- payOS describes both [account registration](https://payos.vn/docs/huong-dan-su-dung/tao-tai-khoan-payos/) and [person/business verification](https://payos.vn/docs/huong-dan-su-dung/xac-thuc-to-chuc/) before [creating API-enabled payment channels](https://payos.vn/docs/api/).
- Bank matching and connection rules depend on institution; see [payOS bank connection guidance](https://payos.vn/docs/huong-dan-su-dung/ket-noi-tai-khoan-ngan-hang/).
- Published [2026 KienlongBank free-tier promotion](https://payos.vn/cong-thanh-toan-mien-phi-payos-2026/) is conditional on its qualifying bank and plan, **not** a guaranteed free rate for .json. Confirm live dashboard tariff, taxes, annual quota, webhook/API availability, and migration path before choosing a package.
- Distinguish cancelling an **unpaid payment request** from refunding an **actual settled bank transfer**. Verify the latter operationally with payOS and the receiving bank. No automated payout/refund activation in this phase.

## Result required to close PAYOS-02

Provider/merchant eligibility and plan documented with current first-party evidence, founder ownership verified without exposing account secrets, bank/receiving account arrangement verified, exact terms known, and no unintended real payment/test transaction. PAYOS-03 (buyer terms and approved catalog) and PAYOS-04 (mock backend) can be developed independently, but live integration cannot begin before these gates.
