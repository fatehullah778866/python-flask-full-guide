# Project 9: Color Palette Generator 🎨

Welcome to Project 9! This app generates random color palettes with hex codes!

## What is This Project? 🤔

**Color Palette Generator** = An app that creates random color palettes!

**Think of it like:**
- **Color Palette** = Collection of colors that work well together
- **Random Generation** = Creates unexpected color combinations
- **Hex Codes** = Color codes like #FF5733

**Palette = Set of colors for design!**

## What You'll Learn 📚

✅ Random number generation
✅ RGB to hexadecimal conversion
✅ String formatting (f-strings)
✅ Color representation
✅ List generation
✅ Loop operations

## What This App Does 🎯

1. **Generate Random Colors** - Creates random RGB values
2. **Convert to Hex** - Converts RGB to hexadecimal format
3. **Create Palette** - Generates 5 random colors
4. **Display Colors** - Shows colors with hex codes
5. **Copy Hex Codes** - Easy copy to clipboard

**Features:**
- 🎨 5 random colors per palette
- 🔢 Hex color codes displayed
- 📋 Copy individual colors
- 🎲 Generate new palettes
- 🖼️ Visual color display

## Step-by-Step Explanation 📖

### Step 1: Generate Random Color
```python
def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02X}{g:02X}{b:02X}'
```
**What this does:**
- Creates random RGB values (0-255)
- Converts to hex format
- Returns hex color code

**Simple explanation:**
- RGB = Red, Green, Blue values
- Hex = Color code format
- Random = Different each time!

### Step 2: Generate Palette
```python
def generate_palette(num_colors=5):
    palette = []
    for _ in range(num_colors):
        palette.append(generate_random_color())
    return palette
```
**What this does:**
- Creates list of colors
- Generates specified number
- Returns color palette

**Simple explanation:**
- Loop = Repeat multiple times
- Generate = Create random color
- Add to list = Collect colors!

## Key Concepts 🎓

### 1. RGB Color Model

**What is RGB?**
- Red, Green, Blue color model
- Each value: 0-255
- 0 = None, 255 = Full intensity

**Example:**
- RGB(255, 0, 0) = Red
- RGB(0, 255, 0) = Green
- RGB(0, 0, 255) = Blue
- RGB(255, 255, 255) = White

### 2. Hexadecimal Colors

**What is hex?**
- Base-16 number system
- Uses 0-9 and A-F
- Format: #RRGGBB

**Example:**
- #FF0000 = Red
- #00FF00 = Green
- #0000FF = Blue
- #FFFFFF = White

### 3. String Formatting

**f-strings:**
```python
f'#{r:02X}{g:02X}{b:02X}'
```
- f'...' = Formatted string
- :02X = 2 digits, uppercase hex
- Formats numbers as hex

## How to Run 🚀

### Step 1: Install Flask
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
1. See random color palette
2. Click "Generate New Palette" for new colors
3. Click "📋 Copy" to copy hex codes
4. Use colors in your designs!

## Files in This Project 📁

```
09-color-palette-generator/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Color palette display
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try generating multiple palettes
2. ✅ Copy hex codes and use them
3. ✅ Move to Project 10: Word Counter

---

**Ready for the next project? Try Project 10: Word Counter!**

