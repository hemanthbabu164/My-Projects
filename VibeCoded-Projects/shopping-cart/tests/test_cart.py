import pytest
from tests.conftest import client, sample_product
import uuid

def test_add_to_cart(client, sample_product):
    """Test adding product to cart"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    response = client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=2",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == sample_product.id
    assert data["quantity"] == 2

def test_add_nonexistent_product_to_cart(client):
    """Test adding non-existent product to cart"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    response = client.post(
        "/cart/add?product_id=99999&quantity=1",
        headers=headers
    )
    assert response.status_code == 404

def test_add_more_than_stock(client, sample_product):
    """Test adding more items than available in stock"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    response = client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=999",
        headers=headers
    )
    assert response.status_code == 400

def test_get_cart(client, sample_product):
    """Test getting cart contents"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    # Add item to cart first
    client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=1",
        headers=headers
    )
    
    # Get cart contents
    response = client.get("/cart/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total_items" in data
    assert "total_price" in data
    assert data["total_items"] == 1

def test_update_cart_item(client, sample_product):
    """Test updating cart item quantity"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    # Add item to cart first
    client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=1",
        headers=headers
    )
    
    # Update quantity
    response = client.put(
        f"/cart/update/{sample_product.id}?quantity=3",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 3

def test_remove_from_cart(client, sample_product):
    """Test removing product from cart"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    # Add item to cart first
    client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=1",
        headers=headers
    )
    
    # Remove item from cart
    response = client.delete(
        f"/cart/remove/{sample_product.id}",
        headers=headers
    )
    assert response.status_code == 200

def test_get_cart_total(client, sample_product):
    """Test getting cart totals"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    # Add item to cart first
    client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=2",
        headers=headers
    )
    
    # Get cart total
    response = client.get("/cart/total", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_items"] == 2
    assert data["total_price"] == sample_product.price * 2

def test_clear_cart(client, sample_product):
    """Test clearing cart"""
    session_id = str(uuid.uuid4())
    headers = {"X-Session-ID": session_id}
    
    # Add item to cart first
    client.post(
        f"/cart/add?product_id={sample_product.id}&quantity=1",
        headers=headers
    )
    
    # Clear cart
    response = client.delete("/cart/clear", headers=headers)
    assert response.status_code == 200
    
    # Verify cart is empty
    response = client.get("/cart/", headers=headers)
    data = response.json()
    assert data["total_items"] == 0
