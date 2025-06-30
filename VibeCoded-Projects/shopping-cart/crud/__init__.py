from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Product, CartItem
from schemas import ProductCreate, ProductUpdate, CartItemCreate
from typing import Optional, List
import math

class ProductCRUD:
    """CRUD operations for products"""
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_products(
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        query: Optional[str] = None,
        manufacturer: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> tuple[List[Product], int]:
        """Get products with optional filtering and pagination"""
        
        # Build query with filters
        db_query = db.query(Product)
        
        # Text search across name, description, and manufacturer
        if query:
            search_filter = or_(
                Product.name.ilike(f"%{query}%"),
                Product.description.ilike(f"%{query}%"),
                Product.manufacturer.ilike(f"%{query}%"),
                Product.part_number.ilike(f"%{query}%")
            )
            db_query = db_query.filter(search_filter)
        
        # Manufacturer filter
        if manufacturer:
            db_query = db_query.filter(Product.manufacturer.ilike(f"%{manufacturer}%"))
        
        # Category filter
        if category:
            db_query = db_query.filter(Product.category.ilike(f"%{category}%"))
        
        # Price range filter
        if min_price is not None:
            db_query = db_query.filter(Product.price >= min_price)
        if max_price is not None:
            db_query = db_query.filter(Product.price <= max_price)
        
        # Get total count for pagination
        total = db_query.count()
        
        # Apply pagination
        products = db_query.offset(skip).limit(limit).all()
        
        return products, total
    
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        """Create a new product"""
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
        """Update an existing product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            update_data = product.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_product, field, value)
            db.commit()
            db.refresh(db_product)
        return db_product

class CartCRUD:
    """CRUD operations for shopping cart"""
    
    @staticmethod
    def get_cart_items(db: Session, session_id: str) -> List[CartItem]:
        """Get all cart items for a session"""
        return db.query(CartItem).filter(CartItem.session_id == session_id).all()
    
    @staticmethod
    def add_to_cart(db: Session, session_id: str, product_id: int, quantity: int = 1) -> CartItem:
        """Add product to cart or update quantity if already exists"""
        
        # Check if item already in cart
        existing_item = db.query(CartItem).filter(
            and_(CartItem.session_id == session_id, CartItem.product_id == product_id)
        ).first()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += quantity
            db.commit()
            db.refresh(existing_item)
            return existing_item
        else:
            # Create new cart item
            cart_item = CartItem(
                session_id=session_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            return cart_item
    
    @staticmethod
    def remove_from_cart(db: Session, session_id: str, product_id: int) -> bool:
        """Remove product from cart"""
        cart_item = db.query(CartItem).filter(
            and_(CartItem.session_id == session_id, CartItem.product_id == product_id)
        ).first()
        
        if cart_item:
            db.delete(cart_item)
            db.commit()
            return True
        return False
    
    @staticmethod
    def update_cart_item_quantity(db: Session, session_id: str, product_id: int, quantity: int) -> Optional[CartItem]:
        """Update cart item quantity"""
        cart_item = db.query(CartItem).filter(
            and_(CartItem.session_id == session_id, CartItem.product_id == product_id)
        ).first()
        
        if cart_item:
            cart_item.quantity = quantity
            db.commit()
            db.refresh(cart_item)
            return cart_item
        return None
    
    @staticmethod
    def clear_cart(db: Session, session_id: str) -> bool:
        """Clear all items from cart"""
        deleted_count = db.query(CartItem).filter(CartItem.session_id == session_id).delete()
        db.commit()
        return deleted_count > 0
    
    @staticmethod
    def calculate_cart_total(db: Session, session_id: str) -> dict:
        """Calculate cart totals"""
        cart_items = CartCRUD.get_cart_items(db, session_id)
        
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        
        return {
            "total_items": total_items,
            "total_price": round(total_price, 2),
            "items_count": len(cart_items)
        }
