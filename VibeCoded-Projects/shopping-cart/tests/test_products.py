import pytest
from tests.conftest import client, sample_product

def test_get_products(client):
    """Test getting products list"""
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data

def test_get_product_detail(client, sample_product):
    """Test getting product details"""
    response = client.get(f"/products/{sample_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_product.id
    assert data["name"] == sample_product.name

def test_get_nonexistent_product(client):
    """Test getting non-existent product"""
    response = client.get("/products/99999")
    assert response.status_code == 404

def test_search_products(client, sample_product):
    """Test product search"""
    response = client.get("/products/?query=brake")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1

def test_filter_by_manufacturer(client, sample_product):
    """Test filtering by manufacturer"""
    response = client.get(f"/products/?manufacturer={sample_product.manufacturer}")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1

def test_price_range_filter(client, sample_product):
    """Test price range filtering"""
    response = client.get("/products/?min_price=10&max_price=100")
    assert response.status_code == 200
    data = response.json()
    assert all(10 <= product["price"] <= 100 for product in data["products"])

def test_pagination(client):
    """Test pagination"""
    response = client.get("/products/?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["products"]) <= 5
