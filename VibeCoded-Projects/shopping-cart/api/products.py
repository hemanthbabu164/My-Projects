from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from crud import ProductCRUD
from schemas import Product, ProductListResponse, ProductSearchParams
import math

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    query: Optional[str] = Query(None, description="Search in name, description, manufacturer, part number"),
    manufacturer: Optional[str] = Query(None, description="Filter by manufacturer"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of automobile parts with optional filtering.
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (1-100)
    - **query**: Search text (searches in name, description, manufacturer, part number)
    - **manufacturer**: Filter by manufacturer name
    - **category**: Filter by category (Engine, Brakes, Suspension, etc.)
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    """
    
    skip = (page - 1) * page_size
    
    products, total = ProductCRUD.get_products(
        db=db,
        skip=skip,
        limit=page_size,
        query=query,
        manufacturer=manufacturer,
        category=category,
        min_price=min_price,
        max_price=max_price
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific automobile part.
    
    - **product_id**: The ID of the product to retrieve
    """
    product = ProductCRUD.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/search/", response_model=ProductListResponse)
async def search_products(
    search_params: ProductSearchParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Advanced search for automobile parts with multiple filters.
    
    This endpoint provides the same functionality as GET /products but with 
    a more structured parameter approach.
    """
    
    skip = (search_params.page - 1) * search_params.page_size
    
    products, total = ProductCRUD.get_products(
        db=db,
        skip=skip,
        limit=search_params.page_size,
        query=search_params.query,
        manufacturer=search_params.manufacturer,
        category=search_params.category,
        min_price=search_params.min_price,
        max_price=search_params.max_price
    )
    
    total_pages = math.ceil(total / search_params.page_size) if total > 0 else 0
    
    return ProductListResponse(
        products=products,
        total=total,
        page=search_params.page,
        page_size=search_params.page_size,
        total_pages=total_pages
    )
