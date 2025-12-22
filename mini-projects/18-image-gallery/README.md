# Project 18: Image Gallery 🖼️

Welcome to Project 18! This app displays images in a gallery format!

## What is This Project? 🤔

**Image Gallery** = An app that displays images in a grid!

**Think of it like:**
- **Gallery** = Collection of images
- **Grid Layout** = Images arranged in rows and columns
- **Display** = Show images beautifully

**Gallery = Visual display of images!**

## What You'll Learn 📚

✅ Image serving
✅ File listing
✅ Grid layouts
✅ Image display
✅ File extension checking
✅ Static file handling

## What This App Does 🎯

1. **List Images** - Finds all images in folder
2. **Display Gallery** - Shows images in grid
3. **Serve Images** - Sends images to browser
4. **Click to View** - Click image to see full size

**Features:**
- 🖼️ Image gallery display
- 📁 Automatic image detection
- 🔍 File extension validation
- 📐 Responsive grid layout
- 🔗 Click to view full size

## Step-by-Step Explanation 📖

### Step 1: Get Images
```python
def get_images():
    images = []
    for filename in os.listdir(IMAGE_FOLDER):
        if extension in ALLOWED_EXTENSIONS:
            images.append(filename)
    return images
```
**What this does:**
- Lists files in images folder
- Checks file extensions
- Adds images to list

**Simple explanation:**
- List = Find files
- Check = Validate
- Add = Include!

### Step 2: Serve Images
```python
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)
```
**What this does:**
- Creates route for each image
- Sends image file to browser
- Browser displays image

**Simple explanation:**
- Route = URL path
- Serve = Send file
- Display = Show image!

## Key Concepts 🎓

### 1. Static Files

**What are static files?**
- Files that don't change
- Images, CSS, JavaScript
- Served directly to browser

**Flask Static:**
- static/ folder
- Automatically served
- Access via url_for()

### 2. Image Serving

**How to serve images:**
- Store in static folder
- Use send_from_directory()
- Create route for images

**Security:**
- Validate file extensions
- Check file exists
- Prevent path traversal

### 3. Grid Layout

**What is grid layout?**
- CSS Grid system
- Responsive design
- Auto-adjusts columns

**CSS Grid:**
```css
grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
```

## How to Run 🚀

### Step 1: Install Flask
```bash
pip install -r requirements.txt
```

### Step 2: Add Images
Add some images to `static/images/` folder:
- PNG, JPG, JPEG, GIF, WEBP formats

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Add images to static/images/ folder
2. Refresh page
3. See images in gallery!
4. Click image to view full size!

## Files in This Project 📁

```
18-image-gallery/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Gallery display
├── static/              # Static files
│   ├── style.css       # Stylesheet
│   └── images/         # Images folder (add your images here)
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Add your own images
2. ✅ Test different image formats
3. ✅ Understand image serving
4. ✅ You've completed 18 projects! 🎉

---

**Congratulations! You've completed 18 projects! 🎉**

