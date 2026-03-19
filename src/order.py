# from datetime import datetime

# class Order:
#     def __init__(self, items, total):
#         self.items = items # List of LineItems
#         self.total = total
#         self.timestamp = datetime.now()

from datetime import datetime

class Order:
    def __init__(self, items, total):
        self.items = items
        self.total = total
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"<Order total={self.total} items={len(self.items)} at {self.timestamp}>"