import pytest
from unittest.mock import MagicMock
from src.checkout import CheckoutService
from src.product import Product, Catalog
from src.cart import Cart
from src.discount import DiscountEngine

def test_successful_checkout_charges_payment_gateway():
    # Setup dependencies
    catalog = Catalog()
    p1 = Product("P1", "Item", 100.0)
    catalog.add_product(p1)
    
    # Mock Inventory: Always says 10 are available
    mock_inv = MagicMock()
    mock_inv.get_available.return_value = 10
    
    # Mock Payment Gateway: Returns True for success
    mock_payment = MagicMock()
    mock_payment.charge.return_value = True
    
    cart = Cart(catalog, inventory=mock_inv)
    cart.add_item("P1", 1)
    
    # Checkout logic
    engine = DiscountEngine() # No discounts for now
    service = CheckoutService(inventory=mock_inv, discount_engine=engine, payment_gateway=mock_payment)
    
    result = service.perform_checkout(cart, payment_token="valid_token")
    
    assert result == "SUCCESS"
    mock_payment.charge.assert_called_with(100.0, "valid_token")

def test_checkout_fails_when_payment_is_declined():
    mock_payment = MagicMock()
    mock_payment.charge.return_value = False # Decline!
    
    # Setup other mocks...
    service = CheckoutService(MagicMock(), MagicMock(), mock_payment)
    
    with pytest.raises(ValueError, match="Payment failed"):
        service.perform_checkout(MagicMock(), "bad_token")