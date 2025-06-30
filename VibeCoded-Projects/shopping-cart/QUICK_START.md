# 🚀 Quick Start Guide

## Step 1: Start the Server

Choose one of these methods to start your server:

### Method A: Double-click the batch file
1. Navigate to your project folder
2. Double-click `start.bat`
3. Wait for "Uvicorn running on http://127.0.0.1:8000"

### Method B: Use PowerShell
```powershell
cd "c:\Users\Hema963RNP2\Downloads\Project Folders\shopping-cart"
.\start.bat
```

### Method C: Manual start (if batch file doesn't work)
```powershell
cd "c:\Users\Hema963RNP2\Downloads\Project Folders\shopping-cart"
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Step 2: Access Your Application

Once you see "Uvicorn running on http://127.0.0.1:8000", open these URLs:

### 🛒 **Shopping Cart (Frontend)**
**URL**: http://127.0.0.1:8000/frontend/index.html

This is your main shopping interface with:
- Product browsing and search
- Shopping cart functionality
- Beautiful, responsive design

### 📚 **API Documentation**
**URL**: http://127.0.0.1:8000/docs

Interactive API documentation where you can:
- Test all API endpoints
- See request/response examples
- Try different parameters

### 🔍 **API Root**
**URL**: http://127.0.0.1:8000/

Basic API information and links to other endpoints.

## Step 3: Test the Shopping Cart

1. **Browse Products**: Visit the frontend URL and scroll through the products
2. **Search**: Try searching for "brake" or "oil"
3. **Add to Cart**: Click "Add to Cart" on any product
4. **View Cart**: Scroll down to see your cart update
5. **Test API**: Visit the `/docs` URL and try the API endpoints

## Common Issues & Solutions

### ❌ "This site can't be reached"
- **Problem**: Server isn't running
- **Solution**: Make sure you started the server and see "Uvicorn running" in your terminal

### ❌ "Connection refused"
- **Problem**: Wrong URL or port
- **Solution**: Use `127.0.0.1:8000` instead of `localhost:8000`

### ❌ Server won't start
- **Problem**: Dependencies or Python environment issue
- **Solution**: Run `.\start.bat` which includes diagnostic checks

### ❌ "Module not found" errors
- **Problem**: Virtual environment or dependencies
- **Solution**: 
  ```powershell
  .\.venv\Scripts\pip.exe install -r requirements.txt
  ```

## Success Indicators

✅ **Server Started Successfully** when you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

✅ **Frontend Working** when you see:
- Product grid with automobile parts
- Search bar and filters
- Shopping cart at the bottom

✅ **API Working** when you visit `/docs` and see:
- Interactive Swagger documentation
- List of all endpoints (Products, Shopping Cart)
- Ability to test endpoints

## What's Included

Your shopping cart system includes:

🔧 **12 Automobile Parts** (Brake pads, Motor oil, Air filter, etc.)
🛒 **Full Shopping Cart** (Add, remove, update quantities)
🔍 **Advanced Search** (By name, manufacturer, category, price)
📱 **Responsive Design** (Works on mobile and desktop)
📚 **Auto Documentation** (Complete API docs)
🧪 **Test Suite** (Comprehensive testing)

## Need Help?

1. Check the terminal for error messages
2. Verify URLs use `127.0.0.1:8000` not `localhost:8000`
3. Make sure the server is running (look for "Uvicorn running")
4. Try running `.\start.bat` again
5. Check `GETTING_STARTED.md` for detailed troubleshooting

Happy shopping! 🚗✨
