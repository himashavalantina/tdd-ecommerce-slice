import pytest
from src.product import Product, Catalog
# The next line will cause an ImportError (RED phase)
from src.cart import Cart 

def test_add_item_and_calculate_total():
    catalog = Catalog()
    p1 = Product("LAPTOP", "Gaming Laptop", 1000.0)
    p2 = Product("MOUSE", "Wireless Mouse", 50.0)
    catalog.add_product(p1)
    catalog.add_product(p2)
    
    cart = Cart(catalog)
    cart.add_item("LAPTOP", 1) # $1000
    cart.add_item("MOUSE", 2)  # $50 * 2 = $100
    
    assert cart.total == 1100.0

def test_add_unknown_sku_raises_error():
    catalog = Catalog()
    cart = Cart(catalog)
    with pytest.raises(ValueError, match="Product not found"):
        cart.add_item("GHOST-SKU", 1)

def test_remove_item():
    catalog = Catalog()
    p1 = Product("A1", "Item 1", 10.0)
    catalog.add_product(p1)
    
    cart = Cart(catalog)
    cart.add_item("A1", 1)
    cart.remove_item("A1")
    
    assert cart.total == 0.0