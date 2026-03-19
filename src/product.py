# class Product:
#     def __init__(self, sku, name, price):
#         pass  # Do nothing

# class Catalog:
#     def add_product(self, product):
#         pass  # Do nothing

#     def get_by_sku(self, sku):
#         return "This is wrong"  # Return something incorrect


# class Product:
#     def __init__(self, sku: str, name: str, price: float):
#         self.sku = sku
#         self.name = name
#         self.price = float(price)

# class Catalog:
#     def __init__(self):
#         self._products = {}

#     def add_product(self, product: Product):
#         self._products[product.sku] = product

#     def get_by_sku(self, sku: str):
#         # This will return the Product object or None if not found
#         return self._products.get(sku)

class Product:
    """Immutable value object representing a catalogue product."""

    def __init__(self, sku: str, name: str, price: float):
        # Validation: Refactoring to ensure data integrity
        if not sku or not isinstance(sku, str):
            raise ValueError("SKU must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        if price is None:
            raise ValueError("Price is required.")
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number.")
        if price < 0:
            raise ValueError("Price must be non-negative.")

        self.sku = sku
        self.name = name
        self.price = float(price)

    def __repr__(self):
        return f"Product(sku={self.sku!r}, name={self.name!r}, price={self.price})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.sku == other.sku and self.name == other.name and self.price == other.price


class Catalog:
    """Manages a collection of products; supports add and SKU-based lookup."""

    def __init__(self):
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product instances can be added to the catalog.")
        self._products[product.sku] = product

    def get_by_sku(self, sku: str) -> Product | None:
        return self._products.get(sku)

    def all_products(self) -> list[Product]:
        return list(self._products.values())