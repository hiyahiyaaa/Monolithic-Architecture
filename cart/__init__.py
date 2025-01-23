import json
from typing import List
from products import Product
from cart import dao


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> List[Product]:
    # Fetch cart details from the database
    cart_details = dao.get_cart(username)
    
    if not cart_details:
        return []
    
    # Use a set for unique item IDs, to minimize unnecessary product lookups
    item_ids = set()
    
    for cart_detail in cart_details:
        try:
            evaluated_contents = json.loads(cart_detail['contents'])
            item_ids.update(evaluated_contents)  # Adding only unique items
        except (ValueError, KeyError):
            continue  # Ignore invalid content format or missing keys

    # If there are item IDs to fetch, get all the products at once to minimize DB calls
    if item_ids:
        products_batch = products.get_products_by_ids(list(item_ids))  # Assuming a batch method exists
        return products_batch

    return []


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)

