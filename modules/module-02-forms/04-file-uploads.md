# Lesson 2.4: File Uploads - Letting Users Upload Files! 📤

## What are File Uploads? 📁

File uploads let users send files to your website:
- **Images** (photos, pictures)
- **Documents** (PDFs, Word files)
- **Videos** (movie files)
- **Any file type!**

Think of it like email attachments - users can attach files to forms!

## Why Do We Need File Uploads? 🎯

Real-world examples:
- **Profile pictures** - Users upload their photos
- **Resume uploads** - Job applications
- **Document sharing** - Sharing files
- **Image galleries** - Photo collections
- **Avatar uploads** - User profile images

## Setting Up for File Uploads ⚙️

### Step 1: Configure Upload Settings

```python
from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to save files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB
```

### Understanding the Settings:

- **`UPLOAD_FOLDER`** = Where to save uploaded files
- **`MAX_CONTENT_LENGTH`** = Maximum file size allowed
  - `16 * 1024 * 1024` = 16 megabytes
  - Prevents huge files from crashing your server!

### Step 2: Create Upload Folder

```python
import os

# Create uploads folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')
```

## Basic File Upload (Without Flask-WTF) 📤

Let's start with a simple file upload:

```python
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' not in request.files:
            return 'No file selected!'
        
        file = request.files['file']
        
        # Check if file was actually selected
        if file.filename == '':
            return 'No file selected!'
        
        # Check if file type is allowed
        if file and allowed_file(file.filename):
            # Make filename safe
            filename = secure_filename(file.filename)
            
            # Save the file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return f'File {filename} uploaded successfully!'
        else:
            return 'File type not allowed!'
    
    # Show upload form
    return '''
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
    '''
```

### Breaking It Down:

- **`request.files['file']`** = Gets the uploaded file
- **`file.filename`** = Name of the file
- **`secure_filename()`** = Makes filename safe (removes dangerous characters)
- **`file.save()`** = Saves file to disk
- **`enctype="multipart/form-data"`** = Required for file uploads!

## Understanding `secure_filename()` 🔒

This function makes filenames safe:

```python
from werkzeug.utils import secure_filename

# Dangerous filename
filename = "../../../etc/passwd"  # ❌ Could access system files!
safe = secure_filename(filename)  # ✅ "etc_passwd" (safe!)

# Another example
filename = "my file (1).jpg"  # Has spaces and parentheses
safe = secure_filename(filename)  # "my_file_1.jpg" (safe!)
```

**Always use `secure_filename()` for security!**

## File Upload with Flask-WTF 📝

Using Flask-WTF is better and safer:

```python
from flask import Flask, render_template_string
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create uploads folder
if not os.path.exists('uploads'):
    os.makedirs('uploads')

class UploadForm(FlaskForm):
    file = FileField('Choose File', 
                    validators=[FileRequired(), 
                               FileAllowed(['jpg', 'png', 'pdf'], 'Images and PDFs only!')])
    submit = SubmitField('Upload')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return f'File {filename} uploaded successfully!'
    
    return render_template_string('''
    <form method="POST" enctype="multipart/form-data">
        {{ form.hidden_tag() }}
        <p>{{ form.file.label }}<br>{{ form.file() }}</p>
        {% if form.file.errors %}
            {% for error in form.file.errors %}
                <span style="color: red;">{{ error }}</span>
            {% endfor %}
        {% endif %}
        <p>{{ form.submit() }}</p>
    </form>
    ''', form=form)
```

### New Things:

- **`FileField`** = Field for file uploads
- **`FileRequired()`** = File must be uploaded
- **`FileAllowed(['jpg', 'png'])`** = Only allow these file types

## Validating File Types ✅

### Method 1: Using FileAllowed (Flask-WTF)
```python
file = FileField('File', validators=[
    FileAllowed(['jpg', 'png', 'pdf'], 'Only images and PDFs!')
])
```

### Method 2: Manual Check
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if file and allowed_file(file.filename):
    # File is allowed
```

## Validating File Size 📏

```python
from flask import request

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    
    # Check file size
    file.seek(0, os.SEEK_END)  # Go to end of file
    file_size = file.tell()  # Get size
    file.seek(0)  # Go back to start
    
    if file_size > MAX_FILE_SIZE:
        return f'File too large! Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB'
    
    # Continue with upload...
```

## Complete Example: Image Upload with Preview 🖼️

```python
from flask import Flask, render_template_string, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

if not os.path.exists('uploads'):
    os.makedirs('uploads')

class ImageUploadForm(FlaskForm):
    image = FileField('Upload Image', 
                     validators=[
                         FileRequired(),
                         FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
                     ])
    submit = SubmitField('Upload')

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    form = ImageUploadForm()
    
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return f'''
        <h2>Upload Successful!</h2>
        <p>File: {filename}</p>
        <img src="/uploads/{filename}" alt="Uploaded image" style="max-width: 500px;">
        <br><a href="/upload">Upload another</a>
        '''
    
    return render_template_string('''
    <h2>Upload Image</h2>
    <form method="POST" enctype="multipart/form-data">
        {{ form.hidden_tag() }}
        <p>
            {{ form.image.label }}<br>
            {{ form.image() }}
            {% if form.image.errors %}
                {% for error in form.image.errors %}
                    <span style="color: red;">{{ error }}</span>
                {% endfor %}
            {% endif %}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
    ''', form=form)

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
```

## Serving Uploaded Files 📂

To show uploaded files, create a route:

```python
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
```

Now you can access files at: `http://localhost:5000/uploads/image.jpg`

## Security Best Practices 🔒

### 1. Always Use secure_filename()
```python
filename = secure_filename(file.filename)  # ✅ Safe
filename = file.filename  # ❌ Dangerous!
```

### 2. Validate File Types
```python
FileAllowed(['jpg', 'png'])  # ✅ Only allow safe types
# No validation  # ❌ Users could upload dangerous files!
```

### 3. Limit File Size
```python
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # ✅ 5MB limit
# No limit  # ❌ Server could crash!
```

### 4. Store Outside Web Root (Advanced)
For production, store files outside the web-accessible folder.

### 5. Scan Files (Advanced)
In production, scan uploaded files for viruses/malware.

## Practice Exercise 🏋️

Create a document upload form that:
1. Only allows PDF and DOC files
2. Limits size to 10MB
3. Shows success message with filename
4. Lists all uploaded files

**Try it yourself!**

## Common Mistakes 🔧

### Mistake 1: Forgetting enctype
```html
<form method="POST">  <!-- ❌ File uploads won't work! -->
<form method="POST" enctype="multipart/form-data">  <!-- ✅ Required! -->
```

### Mistake 2: Not Using secure_filename()
```python
filename = file.filename  # ❌ Security risk!
filename = secure_filename(file.filename)  # ✅ Safe
```

### Mistake 3: No File Type Validation
```python
file.save(filename)  # ❌ Could upload dangerous files!
# Always validate file types!  # ✅
```

### Mistake 4: No Size Limit
```python
# No MAX_CONTENT_LENGTH  # ❌ Server could crash!
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # ✅
```

## What You Learned! 📚

✅ How to handle file uploads in Flask  
✅ Using Flask-WTF for file uploads  
✅ Validating file types and sizes  
✅ Securing file uploads  
✅ Serving uploaded files  
✅ Security best practices  

## Key Concepts 💡

1. **`request.files`** = Dictionary of uploaded files
2. **`secure_filename()`** = Makes filenames safe
3. **`enctype="multipart/form-data"`** = Required for file uploads
4. **`FileField`** = Flask-WTF field for files
5. **`FileAllowed()`** = Validator for file types
6. **`MAX_CONTENT_LENGTH`** = Limits file size

## What's Next? 🚀

Congratulations! You've completed Module 2! You now know:
- ✅ HTML forms
- ✅ Handling forms in Flask
- ✅ Flask-WTF for better forms
- ✅ File uploads

**Next Module**: Database Integration - Learn how to store all this data!

---

**Amazing work! You can now handle forms and file uploads like a pro! 🎉**

