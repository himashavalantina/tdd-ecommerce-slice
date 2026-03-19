import pytest
from unittest.mock import MagicMock
from src.product import Product, Catalog
from src.cart import Cart

def test_add_item_fails_when_inventory_insufficient():
    # Setup Catalog & Product
    catalog = Catalog()
    product = Product("BIKE-01", "Mountain Bike", 500.0)
    catalog.add_product(product)
    
    # Setup Mock Inventory Service
    # We pretend the service says there are only 3 bikes available
    mock_inventory = MagicMock()
    mock_inventory.get_available.return_value = 3
    
    # Setup Cart with the mock inventory
    cart = Cart(catalog, inventory_service=mock_inventory)
    
    # Action & Assert
    # Trying to add 5 should fail because 5 > 3
    with pytest.raises(ValueError, match="Insufficient inventory"):
        cart.add_item("BIKE-01", 5)

def test_add_item_succeeds_when_inventory_sufficient():
    catalog = Catalog()
    product = Product("B1", "Book", 10.0)
    catalog.add_product(product)
    
    mock_inventory = MagicMock()
    mock_inventory.get_available.return_value = 10
    
    cart = Cart(catalog, inventory_service=mock_inventory)
    cart.add_item("B1", 2) # 2 <= 10, should pass
    
    assert cart.total == 20.0