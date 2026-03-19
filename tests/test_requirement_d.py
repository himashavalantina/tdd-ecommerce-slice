import pytest
from src.product import Product, Catalog
from src.cart import Cart
from src.discount import DiscountEngine # This will cause ImportError (RED)

def test_bulk_discount_applied_at_ten_units():
    catalog = Catalog()
    p1 = Product("PEN", "Blue Pen", 2.0)
    catalog.add_product(p1)
    
    cart = Cart(catalog)
    cart.add_item("PEN", 10) # Total 20.0. 10% discount = 2.0
    
    engine = DiscountEngine()
    discount = engine.calculate_discount(cart)
    assert discount == 2.0

def test_order_discount_applied_at_thousand_total():
    catalog = Catalog()
    p1 = Product("GOLD", "Gold Ring", 1000.0)
    catalog.add_product(p1)
    
    cart = Cart(catalog)
    cart.add_item("GOLD", 1) # Total 1000.0. 5% discount = 50.0
    
    engine = DiscountEngine()
    discount = engine.calculate_discount(cart)
    assert discount == 50.0