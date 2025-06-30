from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Product
from api import products_router, cart_router
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Automobile Parts Shopping Cart API",
    description="""
    A comprehensive REST API for an automobile parts e-commerce platform.
    
    ## Features
    
    * **Products**: Browse, search, and filter automobile parts
    * **Shopping Cart**: Add, remove, and manage cart items
    * **Search**: Advanced search with multiple filters
    * **Pagination**: Efficient data loading
    
    ## Quick Start
    
    1. Browse products: `GET /products`
    2. Search products: `GET /products?query=brake`
    3. Add to cart: `POST /cart/add?product_id=1&quantity=2`
    4. View cart: `GET /cart`
    
    ## Session Management
    
    Cart operations use session-based tracking. Include `X-Session-ID` header
    in your requests to maintain cart state across API calls.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@autoparts-api.com",
    }
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products_router)
app.include_router(cart_router)

# Mount static files for frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Automobile Parts Shopping Cart API",
        "version": "1.0.0",
        "documentation": "/docs",
        "frontend": "/frontend/index.html",
        "endpoints": {
            "products": "/products",
            "cart": "/cart",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running properly"}

# Initialize sample data
@app.on_event("startup")
async def startup_event():
    """Initialize database with sample data if empty"""
    db = next(get_db())
    
    # Check if we already have data
    if db.query(Product).count() == 0:
        print("Initializing database with sample automobile parts...")
        
        sample_products = [
            Product(
                name="Brake Pads - Front Set",
                description="High-performance ceramic brake pads for front wheels. Excellent stopping power and reduced brake dust.",
                manufacturer="Bosch",
                part_number="BP001-FRONT",
                price=89.99,
                category="Brakes",
                stock_quantity=50,
                image_url="https://example.com/images/brake-pads-front.jpg"
            ),
            Product(
                name="Motor Oil - Synthetic 5W-30",
                description="Full synthetic motor oil for enhanced engine protection and performance. 5 quart container.",
                manufacturer="Mobil 1",
                part_number="OIL-5W30-5Q",
                price=34.99,
                category="Engine",
                stock_quantity=100,
                image_url="https://example.com/images/motor-oil-5w30.jpg"
            ),
            Product(
                name="Air Filter",
                description="High-flow air filter for improved engine breathing and fuel efficiency.",
                manufacturer="K&N",
                part_number="AF-33-2304",
                price=45.50,
                category="Engine",
                stock_quantity=75,
                image_url="https://example.com/images/air-filter.jpg"
            ),
            Product(
                name="Shock Absorber - Rear",
                description="Gas-charged monotube shock absorber for superior ride comfort and handling.",
                manufacturer="Monroe",
                part_number="SA-REAR-58620",
                price=129.99,
                category="Suspension",
                stock_quantity=30,
                image_url="https://example.com/images/shock-absorber.jpg"
            ),
            Product(
                name="Spark Plugs - Set of 4",
                description="Iridium spark plugs for improved ignition and fuel economy. Set of 4.",
                manufacturer="NGK",
                part_number="SP-IR-4SET",
                price=28.95,
                category="Engine",
                stock_quantity=80,
                image_url="https://example.com/images/spark-plugs.jpg"
            ),
            Product(
                name="Headlight Bulb - H7",
                description="High-intensity halogen headlight bulb with extended life.",
                manufacturer="Philips",
                part_number="HL-H7-PLUS",
                price=18.99,
                category="Electrical",
                stock_quantity=120,
                image_url="https://example.com/images/headlight-bulb.jpg"
            ),
            Product(
                name="Timing Belt",
                description="Durable timing belt for precise engine timing. Fits various models.",
                manufacturer="Gates",
                part_number="TB-123456",
                price=67.50,
                category="Engine",
                stock_quantity=40,
                image_url="https://example.com/images/timing-belt.jpg"
            ),
            Product(
                name="Brake Rotors - Front Pair",
                description="Vented brake rotors for enhanced cooling and braking performance.",
                manufacturer="Brembo",
                part_number="BR-FRONT-PAIR",
                price=189.99,
                category="Brakes",
                stock_quantity=25,
                image_url="https://example.com/images/brake-rotors.jpg"
            ),
            Product(
                name="Cabin Air Filter",
                description="Activated carbon cabin air filter for cleaner interior air.",
                manufacturer="Mann-Filter",
                part_number="CAF-CU2544",
                price=22.75,
                category="Interior",
                stock_quantity=60,
                image_url="https://example.com/images/cabin-filter.jpg"
            ),
            Product(
                name="Battery - 12V 70Ah",
                description="Maintenance-free car battery with excellent cold-cranking performance.",
                manufacturer="Optima",
                part_number="BAT-12V-70AH",
                price=199.99,
                category="Electrical",
                stock_quantity=35,
                image_url="https://example.com/images/car-battery.jpg"
            ),
            Product(
                name="Windshield Wipers - 24 inch",
                description="All-season windshield wipers with superior water repelling technology.",
                manufacturer="Rain-X",
                part_number="WW-24-LATITUDE",
                price=24.99,
                category="Exterior",
                stock_quantity=90,
                image_url="https://example.com/images/windshield-wipers.jpg"
            ),
            Product(
                name="Radiator Coolant - 1 Gallon",
                description="Extended-life antifreeze/coolant for optimal engine temperature control.",
                manufacturer="Prestone",
                part_number="RC-EXTENDED-1GAL",
                price=12.99,
                category="Engine",
                stock_quantity=150,
                image_url="https://example.com/images/radiator-coolant.jpg"
            )
        ]
        
        for product in sample_products:
            db.add(product)
        
        db.commit()
        print(f"Added {len(sample_products)} sample products to the database")
    
    db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
