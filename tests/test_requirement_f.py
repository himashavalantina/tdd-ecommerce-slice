import pytest
from unittest.mock import MagicMock
from src.checkout import CheckoutService
from src.product import Product, Catalog
from src.cart import Cart
from src.discount import DiscountEngine

class FakeOrderRepository:
    def __init__(self):
        self.orders = []
    def save(self, order):
        self.orders.append(order)

def test_successful_checkout_saves_order_to_repository():
    # Setup
    catalog = Catalog()
    catalog.add_product(Product("P1", "Item", 100.0))
    
    mock_inv = MagicMock()
    mock_inv.get_available.return_value = 10
    
    mock_payment = MagicMock()
    mock_payment.charge.return_value = True
    
    repo = FakeOrderRepository() # Our "Database"
    
    cart = Cart(catalog, inventory=mock_inv)
    cart.add_item("P1", 1)
    
    # The CheckoutService now needs the repo
    service = CheckoutService(
        inventory=mock_inv, 
        discount_engine=DiscountEngine(), 
        payment_gateway=mock_payment,
        repository=repo
    )
    
    service.perform_checkout(cart, "token_123")
    
    # Assert
    assert len(repo.orders) == 1
    assert repo.orders[0].total == 100.0