from sqlalchemy import MetaData, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime

metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Create User Model
class Users(Base, UserMixin):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    type = Column(String(25), default="Customer", nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow, nullable=False)

    orders = relationship('Orders', back_populates='users')

    def __init__(self, username, password, email, type):
        self.username = username
        self.password = password
        self.email = email
        self.type = type

    def get_id(self):
        return self.user_id

class Products(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    image = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    type = Column(String, nullable=False)

    order_items = relationship('OrderItems', back_populates='products')

class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.utcnow, nullable=False)
    fk_user_id = Column(Integer, ForeignKey('users.user_id'))

    users = relationship('Users', back_populates='orders')
    items = relationship('OrderItems', back_populates='orders')

class OrderItems(Base):
    __tablename__ = "orderitems"
    item_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    fk_order_id = Column(Integer, ForeignKey('orders.order_id'))
    fk_product_id = Column(Integer, ForeignKey('products.product_id'))

    orders = relationship('Orders', back_populates='items')
    products = relationship('Products', back_populates='order_items')