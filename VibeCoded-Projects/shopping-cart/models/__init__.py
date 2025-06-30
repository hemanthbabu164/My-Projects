from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Product(Base):
    """Automobile parts product model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True, nullable=False)
    description = Column(Text)
    manufacturer = Column(String(100), index=True)
    part_number = Column(String(50), unique=True, index=True)
    price = Column(Float, nullable=False)
    category = Column(String(100), index=True)  # e.g., "Engine", "Brakes", "Suspension"
    stock_quantity = Column(Integer, default=0)
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="product")

class CartItem(Base):
    """Shopping cart item model"""
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True)  # For guest users
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # Fixed: Added ForeignKey
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with product
    product = relationship("Product", back_populates="cart_items")
