from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from crud import CartCRUD, ProductCRUD
from schemas import CartItem, CartSummary
import uuid

router = APIRouter(prefix="/cart", tags=["Shopping Cart"])

def get_session_id(x_session_id: Optional[str] = Header(None)) -> str:
    """Get or generate session ID for cart operations"""
    if x_session_id:
        return x_session_id
    return str(uuid.uuid4())

@router.post("/add", response_model=CartItem)
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    Add a product to the shopping cart.
    
    - **product_id**: ID of the product to add
    - **quantity**: Quantity to add (default: 1)
    - **X-Session-ID**: Optional session ID header (auto-generated if not provided)
    
    If the product is already in the cart, the quantities will be combined.
    """
    
    # Verify product exists
    product = ProductCRUD.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check stock availability
    if product.stock_quantity < quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient stock. Available: {product.stock_quantity}, Requested: {quantity}"
        )
    
    cart_item = CartCRUD.add_to_cart(db, session_id, product_id, quantity)
    return cart_item

@router.delete("/remove/{product_id}")
async def remove_from_cart(
    product_id: int,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    Remove a product from the shopping cart.
    
    - **product_id**: ID of the product to remove
    - **X-Session-ID**: Session ID header (required for this operation)
    """
    
    success = CartCRUD.remove_from_cart(db, session_id, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    
    return {"message": "Product removed from cart successfully"}

@router.put("/update/{product_id}", response_model=CartItem)
async def update_cart_item(
    product_id: int,
    quantity: int,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    Update the quantity of a product in the cart.
    
    - **product_id**: ID of the product to update
    - **quantity**: New quantity (must be greater than 0)
    - **X-Session-ID**: Session ID header (required for this operation)
    """
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    # Verify product exists and check stock
    product = ProductCRUD.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.stock_quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Available: {product.stock_quantity}, Requested: {quantity}"
        )
    
    cart_item = CartCRUD.update_cart_item_quantity(db, session_id, product_id, quantity)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Product not found in cart")
    
    return cart_item

@router.get("/", response_model=CartSummary)
async def get_cart(
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    Get all items in the shopping cart with totals.
    
    - **X-Session-ID**: Session ID header (required to identify the cart)
    
    Returns cart items, total item count, and total price.
    """
    
    cart_items = CartCRUD.get_cart_items(db, session_id)
    totals = CartCRUD.calculate_cart_total(db, session_id)
    
    return CartSummary(
        items=cart_items,
        total_items=totals["total_items"],
        total_price=totals["total_price"]
    )

@router.get("/total")
async def get_cart_total(
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    Get cart totals (items count and total price).
    
    - **X-Session-ID**: Session ID header (required to identify the cart)
    """
    
    return CartCRUD.calculate_cart_total(db, session_id)

@router.delete("/clear")
async def clear_cart(
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    """
    Clear all items from the shopping cart.
    
    - **X-Session-ID**: Session ID header (required to identify the cart)
    """
    
    success = CartCRUD.clear_cart(db, session_id)
    if success:
        return {"message": "Cart cleared successfully"}
    else:
        return {"message": "Cart was already empty"}
