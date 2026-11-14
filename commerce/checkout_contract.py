"""Fail-closed, provider-neutral checkout quotation contract.

This module is an internal development artifact, not an HTTP endpoint or a
payment integration. The currently committed checkout policy is disabled.
Real payment status must later come only from verified provider reconciliation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

POLICY_FILE = Path(__file__).with_name("checkout-policy.json")
REQUIRED_GATES = (
    "offer_and_prices_approved",
    "print_and_shipping_confirmed",
    "buyer_notice_and_refund_terms_approved",
    "merchant_and_webhook_verified",
    "transaction_and_refund_tested",
    "founder_paid_release_approved",
)


class CheckoutUnavailable(ValueError):
    """The requested checkout cannot be safely offered."""


def load_policy(path: Path = POLICY_FILE) -> dict[str, Any]:
    """Load server-owned draft data, never a client-supplied policy."""
    return json.loads(path.read_text(encoding="utf-8"))


def quote_request(request: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    """Validate an edition/method and calculate an internal server-side quote.

    The browser may choose only an edition ID and an already-approved method.
    It must never supply amounts, return URLs, order statuses, recipient bank
    details or even an approval flag. This function does not create orders,
    charge cards, or return payment links. No buyer PII is accepted.
    """
    if not isinstance(request, dict) or set(request) != {"edition_id", "payment_method"}:
        raise CheckoutUnavailable("Only edition_id and payment_method are accepted.")
    edition_id = request["edition_id"]
    payment_method = request["payment_method"]
    if not isinstance(edition_id, str) or not isinstance(payment_method, str):
        raise CheckoutUnavailable("Edition and payment method must be IDs.")

    # Fail closed before using the requested fields or any proposed amount.
    if policy.get("mode") != "ready":
        raise CheckoutUnavailable("Checkout is not authorized.")
    gates = policy.get("approval_gates")
    if not isinstance(gates, dict) or not all(gates.get(key) is True for key in REQUIRED_GATES):
        raise CheckoutUnavailable("Commercial and payment validation gates are incomplete.")
    if not policy.get("merchant_provider") or not policy.get("payment_endpoint"):
        raise CheckoutUnavailable("A reviewed server/provider connection is required.")
    if policy.get("currency") != "VND":
        raise CheckoutUnavailable("Unexpected currency.")

    offers = policy.get("offers")
    if not isinstance(offers, dict) or edition_id not in offers:
        raise CheckoutUnavailable("Unknown book edition.")
    allowed_methods = policy.get("approved_payment_methods")
    if not isinstance(allowed_methods, list) or payment_method not in allowed_methods:
        raise CheckoutUnavailable("Payment method has not been verified.")
    selected = offers[edition_id]
    if not isinstance(selected, dict):
        raise CheckoutUnavailable("Missing approved offer.")
    total = selected.get("approved_price_vnd")
    deposit = selected.get("approved_deposit_vnd")
    if type(total) is not int or type(deposit) is not int or not (0 < deposit <= total):
        raise CheckoutUnavailable("Approved price and refundable deposit are required.")

    return {
        "edition_id": edition_id,
        "payment_method": payment_method,
        "currency": "VND",
        "total_price_vnd": total,
        "refundable_deposit_vnd": deposit,
        "status": "quote_only",
    }
