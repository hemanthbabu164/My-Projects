# Automobile Parts Shopping Cart API

A FastAPI-based REST API for an automobile parts e-commerce platform with shopping cart functionality.

## Features

- **Product Management**: Browse, search, and view automobile parts
- **Shopping Cart**: Add/remove items, calculate totals
- **Search & Filters**: Search by name, manufacturer, price range
- **Pagination**: Efficient product listing
- **Auto Documentation**: Built-in Swagger UI

## Quick Start

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Server**:
```bash
uvicorn main:app --reload
```

3. **Access the API**:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Products
- `GET /products` - List products (with pagination)
- `GET /products/{product_id}` - Get product details
- `GET /products/search` - Search products

### Shopping Cart
- `POST /cart/add` - Add product to cart
- `DELETE /cart/remove/{product_id}` - Remove product from cart
- `GET /cart` - Get cart contents
- `GET /cart/total` - Get cart total

## Testing

Run tests with:
```bash
pytest
```

Test the API manually using:
- Built-in Swagger UI at `/docs`
- Postman collection (import the OpenAPI spec)
- Any HTTP client

## Project Structure

```
shopping-cart/
├── main.py              # FastAPI app entry point
├── models/              # Database models
├── schemas/             # Pydantic schemas
├── crud/                # Database operations
├── api/                 # API routes
├── database.py          # Database connection
├── requirements.txt     # Dependencies
└── tests/              # Test files
```
