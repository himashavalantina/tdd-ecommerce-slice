# class DiscountEngine:
#     def calculate_discount(self, cart):
#         total_discount = 0.0
        
#         # Rule 1: Bulk Discount (10% off if qty >= 10)
#         for item in cart._items.values():
#             if item.quantity >= 10:
#                 total_discount += item.subtotal * 0.10
        
#         # Rule 2: Order Discount (5% off if total >= 1000)
#         # Note: We apply this on the subtotal before bulk discounts for now
#         if cart.total >= 1000:
#             total_discount += cart.total * 0.05
            
#         return total_discount

#     def get_final_total(self, cart):
#         return cart.total - self.calculate_discount(cart)

class DiscountRule:
    """Base class for all discount strategies."""
    def apply(self, cart) -> float:
        return 0.0

class BulkDiscountRule(DiscountRule):
    def apply(self, cart):
        discount = 0.0
        for item in cart._items.values():
            if item.quantity >= 10:
                discount += item.subtotal * 0.10
        return discount

class OrderDiscountRule(DiscountRule):
    def apply(self, cart):
        if cart.total >= 1000:
            return cart.total * 0.05
        return 0.0

class DiscountEngine:
    def __init__(self, rules=None):
        # We can now plug in any rules we want!
        self.rules = rules or [BulkDiscountRule(), OrderDiscountRule()]

    def calculate_discount(self, cart):
        return sum(rule.apply(cart) for rule in self.rules)

    def get_final_total(self, cart):
        return cart.total - self.calculate_discount(cart)