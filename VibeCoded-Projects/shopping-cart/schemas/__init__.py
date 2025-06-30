from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    part_number: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    category: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    part_number: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Cart Schemas
class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)

class CartItemCreate(CartItemBase):
    session_id: str

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)

class CartItem(CartItemBase):
    id: int
    session_id: str
    created_at: datetime
    product: Product
    
    class Config:
        from_attributes = True

class CartSummary(BaseModel):
    items: List[CartItem]
    total_items: int
    total_price: float

# Search and Filter Schemas
class ProductSearchParams(BaseModel):
    query: Optional[str] = None
    manufacturer: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

class ProductListResponse(BaseModel):
    products: List[Product]
    total: int
    page: int
    page_size: int
    total_pages: int
