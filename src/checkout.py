# class CheckoutService:
#     def __init__(self, inventory, discount_engine, payment_gateway):
#         self.inventory = inventory
#         self.discount_engine = discount_engine
#         self.payment_gateway = payment_gateway

#     def perform_checkout(self, cart, payment_token):
#         # 1. Final Inventory Check
#         for sku, item in cart._items.items():
#             if item.quantity > self.inventory.get_available(sku):
#                 raise ValueError(f"Stock changed for {sku}")

#         # 2. Calculate Final Price
#         final_amount = self.discount_engine.get_final_total(cart)

#         # 3. Charge Payment
#         success = self.payment_gateway.charge(final_amount, payment_token)
        
#         if not success:
#             raise ValueError("Payment failed")
            
#         return "SUCCESS"

# class CheckoutService:
#     def __init__(self, inventory, discount_engine, payment_gateway):
#         self.inventory = inventory
#         self.discount_engine = discount_engine
#         self.payment_gateway = payment_gateway

#     def perform_checkout(self, cart, payment_token):
#         self._validate_stock(cart)
#         amount = self.discount_engine.get_final_total(cart)
#         self._process_payment(amount, payment_token)
#         return "SUCCESS"

#     def _validate_stock(self, cart):
#         for sku, item in cart._items.items():
#             if item.quantity > self.inventory.get_available(sku):
#                 raise ValueError("Insufficient stock")

#     def _process_payment(self, amount, token):
#         if not self.payment_gateway.charge(amount, token):
#             raise ValueError("Payment failed")

from src.order import Order

class CheckoutService:
    def __init__(self, inventory, discount_engine, payment_gateway, repository=None):
        self.inventory = inventory
        self.discount_engine = discount_engine
        self.payment_gateway = payment_gateway
        self.repository = repository # New dependency

    def perform_checkout(self, cart, payment_token):
        # 1. Validation & Price
        for sku, item in cart._items.items():
            if item.quantity > self.inventory.get_available(sku):
                raise ValueError("Insufficient stock")
        
        amount = self.discount_engine.get_final_total(cart)

        # 2. Payment
        if not self.payment_gateway.charge(amount, payment_token):
            raise ValueError("Payment failed")

        # 3. Persistence (Green Phase)
        if self.repository:
            new_order = Order(items=list(cart._items.values()), total=amount)
            self.repository.save(new_order)
            
        return "SUCCESS"