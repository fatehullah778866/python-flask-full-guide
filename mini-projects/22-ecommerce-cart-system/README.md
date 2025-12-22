# Project 22: E-commerce Cart System 🛒

Welcome to Project 22! This app allows users to add products to a shopping cart!

## What is This Project? 🤔

**E-commerce Cart System** = An app for online shopping!

**Think of it like:**
- **Store** = Product catalog
- **Cart** = Shopping basket
- **Checkout** = Purchase process

**Cart = Where you put items before buying!**

## What You'll Learn 📚

✅ Shopping cart functionality
✅ Session management
✅ Cart operations (add, update, remove)
✅ Product catalog
✅ Quantity management
✅ Total calculation

## What This App Does 🎯

1. **Product Catalog** - Browse available products
2. **Add to Cart** - Add products with quantity
3. **View Cart** - See all items in cart
4. **Update Cart** - Change quantities
5. **Remove Items** - Delete items from cart
6. **Calculate Total** - Sum of all items

**Features:**
- 🛒 Shopping cart
- 📦 Product catalog
- ➕ Add to cart
- ✏️ Update quantities
- 🗑️ Remove items
- 💰 Total calculation

## Step-by-Step Explanation 📖

### Step 1: Initialize Cart
```python
def init_cart():
    if 'cart' not in session:
        session['cart'] = {}
```
**What this does:**
- Creates cart if it doesn't exist
- Stores in session
- Dictionary format: {product_id: quantity}

**Simple explanation:**
- Init = Create
- Cart = Shopping basket!

### Step 2: Add to Cart
```python
if product_id in session['cart']:
    session['cart'][product_id] += quantity
else:
    session['cart'][product_id] = quantity
```
**What this does:**
- Checks if product already in cart
- Adds to existing quantity or creates new entry
- Updates session

**Simple explanation:**
- Check = See if exists
- Add = Increase quantity!

### Step 3: Calculate Total
```python
for product_id, quantity in session['cart'].items():
    product = get_product(product_id)
    total += product['price'] * quantity
```
**What this does:**
- Loops through cart items
- Gets product price
- Multiplies by quantity
- Sums all items

**Simple explanation:**
- Loop = Go through items
- Calculate = Figure out total!

## Key Concepts 🎓

### 1. Shopping Cart

**What is a cart?**
- Temporary storage
- Holds selected items
- Session-based

**Cart Structure:**
- Dictionary format
- {product_id: quantity}
- Example: {1: 2, 3: 1}

### 2. Session Management

**What is session?**
- Stores data between requests
- User-specific
- Temporary storage

**Cart in Session:**
- Stored in session['cart']
- Persists across requests
- User-specific cart

### 3. Cart Operations

**Operations:**
- Add = Add product
- Update = Change quantity
- Remove = Delete item
- Calculate = Sum total

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Browse products
2. Add products to cart
3. View cart
4. Update quantities
5. Remove items!

## Files in This Project 📁

```
22-ecommerce-cart-system/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   ├── index.html      # Product catalog
│   └── cart.html       # Shopping cart
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Test adding products
2. ✅ Test updating quantities
3. ✅ Understand session management
4. ✅ You've completed 22 projects! 🎉

---

**Congratulations! You've completed 22 projects! 🎉**

