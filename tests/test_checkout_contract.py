"""Safety regressions for the private, non-transactional checkout quote."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "commerce"))
from checkout_contract import CheckoutUnavailable, load_policy, quote_request, REQUIRED_GATES


class CheckoutContractTests(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy()
        self.request = {"edition_id": "core", "payment_method": "bank_qr"}

    def ready_policy(self):
        p = copy.deepcopy(self.policy)
        p["mode"] = "ready"
        p["merchant_provider"] = "reviewed-provider"
        p["payment_endpoint"] = "https://checkout.example.test/api/orders"
        p["approval_gates"] = dict.fromkeys(REQUIRED_GATES, True)
        p["approved_payment_methods"] = ["bank_qr"]
        p["offers"]["core"]["approved_price_vnd"] = 249000
        p["offers"]["core"]["approved_deposit_vnd"] = 49000
        return p

    def test_repository_checkout_is_disabled(self):
        self.assertEqual(self.policy["mode"], "disabled")
        self.assertTrue(all(value is False for value in self.policy["approval_gates"].values()))
        self.assertEqual(self.policy["approved_payment_methods"], [])
        for edition in self.policy["offers"].values():
            self.assertIsNone(edition["approved_price_vnd"])
            self.assertIsNone(edition["approved_deposit_vnd"])
        with self.assertRaises(CheckoutUnavailable):
            quote_request(self.request, self.policy)

    def test_rejects_client_controlled_amount_urls_and_status(self):
        for injected in ({"amount": 1}, {"return_url": "https://attacker.example"}, {"status": "PAID"}, {"buyer_email": "x@y.test"}):
            with self.subTest(injected=injected), self.assertRaises(CheckoutUnavailable):
                quote_request({**self.request, **injected}, self.ready_policy())

    def test_rejects_missing_or_unapproved_gate(self):
        for gate in REQUIRED_GATES:
            p = self.ready_policy()
            p["approval_gates"][gate] = False
            with self.subTest(gate=gate), self.assertRaises(CheckoutUnavailable):
                quote_request(self.request, p)

    def test_rejects_missing_provider_and_endpoint(self):
        for field in ("merchant_provider", "payment_endpoint"):
            p = self.ready_policy()
            p[field] = None
            with self.subTest(field=field), self.assertRaises(CheckoutUnavailable):
                quote_request(self.request, p)

    def test_rejects_unapproved_method_and_edition(self):
        p = self.ready_policy()
        for request in (
            {"edition_id": "nonexistent", "payment_method": "bank_qr"},
            {"edition_id": "core", "payment_method": "momo"},
        ):
            with self.subTest(request=request), self.assertRaises(CheckoutUnavailable):
                quote_request(request, p)

    def test_rejects_unapproved_or_invalid_prices(self):
        for value in (None, -1, 0, True, "49000", 500000):
            p = self.ready_policy()
            p["offers"]["core"]["approved_deposit_vnd"] = value
            with self.subTest(value=value), self.assertRaises(CheckoutUnavailable):
                quote_request(self.request, p)

    def test_rejects_unapproved_currency(self):
        p = self.ready_policy()
        p["currency"] = "USD"
        with self.assertRaises(CheckoutUnavailable):
            quote_request(self.request, p)

    def test_quote_only_never_reports_a_paid_order(self):
        # Synthetic policy is test-only; this is not permission to transact.
        quote = quote_request(self.request, self.ready_policy())
        self.assertEqual(quote, {
            "edition_id": "core",
            "payment_method": "bank_qr",
            "currency": "VND",
            "total_price_vnd": 249000,
            "refundable_deposit_vnd": 49000,
            "status": "quote_only",
        })
        self.assertNotIn("checkout_url", quote)
        self.assertNotIn("order_code", quote)
        self.assertNotIn("buyer", quote)


if __name__ == "__main__":
    unittest.main()
