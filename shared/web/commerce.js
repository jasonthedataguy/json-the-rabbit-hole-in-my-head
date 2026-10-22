// Public offer preview. These figures are hypotheses from the October 2026
// strategy deck, not approved prices or an invitation to transfer money.
// Payment credentials and bank details must never be copied into shared/web/.
export const commerce = {
  status: 'preview',
  checkoutEndpoint: '',
  currency: 'VND',
  offers: [
    {id:'core', name:'Core book', estimate:249000, description:'The complete illustrated memoir in a trade physical edition. Final trim, paper and binding await a printer proof.'},
    {id:'illustrated', name:'Illustrated book', estimate:429000, description:'A richer physical edition with five act-opening portal spreads and removable inserts. Specifications await a printer proof.'},
    {id:'collector', name:'Collector edition', estimate:799000, description:'A proposed numbered sleeve or box with selected art extras. The final contents and production quantity are unconfirmed.'}
  ],
  samples: [
    {name:'Sticker sheet', estimate:39000},
    {name:'Bookmark set', estimate:49000},
    {name:'Postcard pack', estimate:89000},
    {name:'A4 chapter poster', estimate:129000}
  ],
  // A visual checklist only: the server-owned policy in commerce/checkout-policy.json
  // is authoritative if a real backend is ever deployed.
  readiness: [
    {id:'offer_and_prices_approved', name:'Edition contents and final price', detail:'Approve physical specifications, stock assumptions and buyer-facing prices.', complete:false},
    {id:'print_and_shipping_confirmed', name:'Production and fulfillment', detail:'Confirm printer proof, delivery regions, shipping costs and timing.', complete:false},
    {id:'buyer_notice_and_refund_terms_approved', name:'Refund and privacy terms', detail:'Publish verified deposit, cancellation, privacy and support terms.', complete:false},
    {id:'merchant_and_webhook_verified', name:'Provider and reconciliation', detail:'Verify a merchant account, hosted checkout and signed server notifications.', complete:false},
    {id:'transaction_and_refund_tested', name:'End-to-end payment and refund QA', detail:'Test failures, duplicate callbacks, reconciliation and a real refund.', complete:false},
    {id:'founder_paid_release_approved', name:'Founder commercial release', detail:'Approve exact offer, payment methods and publication scope.', complete:false}
  ],
  paymentMethods: [
    {name:'Visa / Mastercard', detail:'Hosted card checkout requires a verified payment-provider connection.'},
    {name:'Domestic bank transfer and bank QR', detail:'A unique order reference and confirmed recipient account are required.'},
    {name:'MoMo', detail:'Payment link or merchant integration must be tested.'},
    {name:'ZaloPay', detail:'Payment link or merchant integration must be tested.'},
    {name:'VNPay', detail:'Payment link or merchant integration must be tested.'}
  ]
};
