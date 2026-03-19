import pytest

from src.product import Product, Catalog

def test_create_product_and_find_by_sku():
    catalog = Catalog()
    product = Product(sku="SHIRT-01", name="Cool Shirt", price=25.0)
    catalog.add_product(product)
    
    found = catalog.get_by_sku("SHIRT-01")
    assert found.name == "Cool Shirt"

def test_missing_sku_returns_none():
    catalog = Catalog()
    assert catalog.get_by_sku("NON-EXISTENT") is None