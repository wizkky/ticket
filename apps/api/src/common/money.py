"""Chilean peso precision without changing the precision of historical currencies."""

from decimal import ROUND_HALF_UP, Decimal


def valid_currency_precision(value: Decimal | None, currency: str) -> bool:
    """CLP has no fractional pesos. Other currencies retain their existing rules."""
    return value is None or currency.upper() != "CLP" or value == value.to_integral_value()


def round_currency_amount(value: Decimal, currency: str) -> Decimal:
    """Round a computed CLP price to the nearest peso, with halves rounded up."""
    if currency.upper() == "CLP":
        return value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return value.quantize(Decimal("0.01"))
