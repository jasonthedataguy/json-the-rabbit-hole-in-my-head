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
  paymentMethods: [
    {name:'Visa / Mastercard', detail:'Hosted card checkout requires a verified payment-provider connection.'},
    {name:'Domestic bank transfer and bank QR', detail:'A unique order reference and confirmed recipient account are required.'},
    {name:'MoMo', detail:'Payment link or merchant integration must be tested.'},
    {name:'ZaloPay', detail:'Payment link or merchant integration must be tested.'},
    {name:'VNPay', detail:'Payment link or merchant integration must be tested.'}
  ]
};
