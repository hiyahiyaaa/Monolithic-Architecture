from products import dao
from functools import lru_cache

class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])

# Using LRU Cache for listing products if they don't change frequently
@lru_cache(maxsize=128)
def list_products() -> list[Product]:
    products = dao.list_products()
    return [Product.load(product) for product in products]

def get_product(product_id: int) -> Product:
    return Product.load(dao.get_product(product_id))

def add_product(product: dict):
    # You can implement a bulk insert here if needed for better performance
    dao.add_product(product)

def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)


