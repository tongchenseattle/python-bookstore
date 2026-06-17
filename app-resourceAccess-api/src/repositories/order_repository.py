import uuid

from sqlalchemy.orm import Session

from src.models.order import Cart, CartItem, PseudoOrder


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_cart_item(self, cart_id: uuid.UUID, item: CartItem) -> CartItem:
        item.cart_id = cart_id
        self.db.add(item)
        self.db.flush()
        return item

    def create_pseudo_order(self, order: PseudoOrder) -> PseudoOrder:
        self.db.add(order)
        self.db.flush()
        return order

    def get_cart(self, cart_id: uuid.UUID) -> Cart | None:
        return self.db.get(Cart, cart_id)
