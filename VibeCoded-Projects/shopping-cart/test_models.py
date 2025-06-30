#!/usr/bin/env python3
"""
Test script to verify the SQLAlchemy models are working correctly
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models():
    """Test the SQLAlchemy models and relationships"""
    print("🧪 Testing SQLAlchemy Models...")
    
    try:
        # Import models
        from models import Base, Product, CartItem
        from database import engine
        
        print("✅ Models imported successfully")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test the relationship
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create a test product
        test_product = Product(
            name="Test Brake Pads",
            part_number="TEST-001",
            price=50.00,
            stock_quantity=10
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        print(f"✅ Test product created with ID: {test_product.id}")
        
        # Create a test cart item
        test_cart_item = CartItem(
            session_id="test-session",
            product_id=test_product.id,
            quantity=2
        )
        db.add(test_cart_item)
        db.commit()
        db.refresh(test_cart_item)
        print(f"✅ Test cart item created with ID: {test_cart_item.id}")
        
        # Test the relationship
        cart_item_with_product = db.query(CartItem).filter(CartItem.id == test_cart_item.id).first()
        if cart_item_with_product and cart_item_with_product.product:
            print(f"✅ Relationship working: Cart item links to product '{cart_item_with_product.product.name}'")
        else:
            print("❌ Relationship not working")
            return False
        
        # Test reverse relationship
        product_with_cart_items = db.query(Product).filter(Product.id == test_product.id).first()
        if product_with_cart_items and len(product_with_cart_items.cart_items) > 0:
            print(f"✅ Reverse relationship working: Product has {len(product_with_cart_items.cart_items)} cart items")
        else:
            print("❌ Reverse relationship not working")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_app():
    """Test if the main FastAPI app can be imported"""
    print("\n🚀 Testing FastAPI Application...")
    
    try:
        import main
        app = main.app
        print("✅ FastAPI app created successfully")
        print(f"   App title: {app.title}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 SQLAlchemy Relationship Fix - Testing")
    print("=" * 50)
    
    success = True
    
    if not test_models():
        success = False
    
    if not test_main_app():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ SQLAlchemy relationships are working correctly")
        print("✅ FastAPI app can be imported without errors")
        print("\n🚀 You can now start the server with: .\\start.bat")
    else:
        print("❌ TESTS FAILED - Check the errors above")
    
    sys.exit(0 if success else 1)
