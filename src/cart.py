# class Cart:
#     def __init__(self, catalog):
#         self.catalog = catalog
#         self._items = {}  # Dictionary: {sku: quantity}

#     def add_item(self, sku, quantity):
#         product = self.catalog.get_by_sku(sku)
#         if not product:
#             raise ValueError("Product not found in catalog")
        
#         if sku in self._items:
#             self._items[sku] += quantity
#         else:
#             self._items[sku] = quantity

#     def remove_item(self, sku):
#         if sku in self._items:
#             del self._items[sku]

#     @property
#     def total(self):
#         total_sum = 0.0
#         for sku, quantity in self._items.items():
#             product = self.catalog.get_by_sku(sku)
#             total_sum += product.price * quantity
#         return total_sum


# class LineItem:
#     """Helper class to handle quantity and subtotal logic."""
#     def __init__(self, product, quantity):
#         if quantity <= 0:
#             raise ValueError("Quantity must be greater than zero.")
#         self.product = product
#         self.quantity = quantity

#     @property
#     def subtotal(self):
#         return self.product.price * self.quantity

# class Cart:
#     def __init__(self, catalog):
#         self.catalog = catalog
#         self._items = {}  # Stores LineItem objects

#     def add_item(self, sku, quantity):
#         product = self.catalog.get_by_sku(sku)
#         if not product:
#             raise ValueError("Product not found in catalog")
        
#         if sku in self._items:
#             self._items[sku].quantity += quantity
#         else:
#             self._items[sku] = LineItem(product, quantity)

#     def remove_item(self, sku):
#         if sku not in self._items:
#             raise ValueError("Item not in cart")
#         del self._items[sku]

#     @property
#     def total(self):
#         return sum(item.subtotal for item in self._items.values())
class InventoryGateway:
    """Interface/Base class for inventory checks."""
    def get_available(self, sku: str) -> int:
        return float('inf') # Default to infinite stock if not specified

class Cart:
    def __init__(self, catalog, inventory=None):
        self.catalog = catalog
        # If no inventory is passed, use the Gateway that returns infinite stock
        self.inventory = inventory or InventoryGateway()
        self._items = {}

    def add_item(self, sku, quantity):
        product = self.catalog.get_by_sku(sku)
        if not product:
            raise ValueError("Product not found in catalog")
        
        # Check stock (Much cleaner logic now!)
        current_qty = self._items[sku].quantity if sku in self._items else 0
        if (current_qty + quantity) > self.inventory.get_available(sku):
            raise ValueError("Insufficient inventory")

        if sku in self._items:
            self._items[sku].quantity += quantity
        else:
            self._items[sku] = LineItem(product, quantity)
    
    
class LineItem:
    """Helper class to handle quantity and subtotal logic."""
    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self):
        return self.product.price * self.quantity

class Cart:
    def __init__(self, catalog, inventory=None):
        self.catalog = catalog
        self.inventory = inventory # New dependency
        self._items = {}  # Stores LineItem objects

    def add_item(self, sku, quantity):
        product = self.catalog.get_by_sku(sku)
        if not product:
            raise ValueError("Product not found in catalog")
        
        # --- NEW INVENTORY CHECK (GREEN PHASE) ---
        if self.inventory:
            available = self.inventory.get_available(sku)
            if quantity > available:
                raise ValueError(f"Insufficient inventory. Only {available} available.")
        # ------------------------------------------
        

        if sku in self._items:
            # Check cumulative quantity if adding more of the same item
            new_total_qty = self._items[sku].quantity + quantity
            if self.inventory:
                 available = self.inventory.get_available(sku)
                 if new_total_qty > available:
                     raise ValueError(f"Insufficient inventory. Only {available} available.")
            
            self._items[sku].quantity = new_total_qty
        else:
            self._items[sku] = LineItem(product, quantity)

    def remove_item(self, sku):
        if sku not in self._items:
            raise ValueError("Item not in cart")
        del self._items[sku]

    @property
    def total(self):
        return sum(item.subtotal for item in self._items.values())

