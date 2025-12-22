# Project 14: File Upload App 📁

Welcome to Project 14! This app allows users to upload files!

## What is This Project? 🤔

**File Upload App** = An app that lets users upload and download files!

**Think of it like:**
- **Upload** = Sending file to server
- **Storage** = Saving file on server
- **Download** = Getting file from server

**File Upload = Sending files to server!**

## What You'll Learn 📚

✅ File upload handling
✅ File validation
✅ Secure filename handling
✅ File storage
✅ File serving
✅ Security practices

## What This App Does 🎯

1. **Upload Files** - Users can upload files
2. **Validate Files** - Checks file type and size
3. **Store Files** - Saves files to server
4. **List Files** - Shows uploaded files
5. **Download Files** - Users can download files

**Features:**
- 📁 File upload
- ✅ File type validation
- 🔒 Secure filename handling
- 📋 File listing
- ⬇️ File download
- 📏 File size limits

## Step-by-Step Explanation 📖

### Step 1: Configure Upload Settings
```python
UPLOAD_FOLDER = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg'}
```
**What this does:**
- Sets upload folder
- Limits file size
- Defines allowed file types

**Simple explanation:**
- Configuration = Upload settings
- Limits = Security measures!

### Step 2: Validate File
```python
if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(file_path)
```
**What this does:**
- Checks file extension
- Secures filename
- Saves file

**Simple explanation:**
- Validate = Check if allowed
- Secure = Make safe
- Save = Store file!

### Step 3: Serve File
```python
return send_from_directory(UPLOAD_FOLDER, filename)
```
**What this does:**
- Sends file to user
- From upload folder
- Downloads or displays

**Simple explanation:**
- Serve = Send file
- Download = Get file!

## Key Concepts 🎓

### 1. File Upload

**What is file upload?**
- Sending file from client to server
- Through HTTP POST request
- Multipart form data

**Process:**
1. User selects file
2. Form submits file
3. Server receives file
4. Server saves file

### 2. File Validation

**Why validate?**
- Security
- Prevent dangerous files
- Control file types

**What to validate:**
- File extension
- File size
- File content (optional)

### 3. Secure Filenames

**Why secure?**
- Prevent path traversal
- Remove dangerous characters
- Ensure safe storage

**secure_filename():**
- Removes ../ (path traversal)
- Removes special characters
- Makes filename safe

### 4. File Storage

**Where to store?**
- Dedicated folder
- Outside web root (better)
- Organized structure

**Security:**
- Validate before saving
- Secure filenames
- Limit file size

## How to Run 🚀

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python app.py
```

**Note:** The 'uploads' folder will be created automatically.

### Step 3: Open in Browser
Visit: `http://127.0.0.1:5000`

**How to use:**
1. Select a file
2. Click "Upload File"
3. View uploaded files
4. Download files!

## Files in This Project 📁

```
14-file-upload-app/
├── app.py              # Main Flask application
├── requirements.txt     # Dependencies
├── templates/           # HTML templates
│   └── index.html      # Upload form and file list
├── static/              # CSS stylesheet
│   └── style.css       # Stylesheet
├── uploads/             # Uploaded files folder (created automatically)
└── README.md           # This file
```

## Next Steps 🎯

After completing this project:

1. ✅ Try uploading different file types
2. ✅ Test file validation
3. ✅ Download uploaded files
4. ✅ You've completed 14 projects! 🎉

---

**Congratulations! You've completed 14 projects! 🎉**

