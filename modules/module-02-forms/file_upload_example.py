# File Upload Example
# This shows how to handle file uploads in Flask

from flask import Flask, render_template_string, send_from_directory, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Create uploads folder if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Form for image upload
class ImageUploadForm(FlaskForm):
    image = FileField('Upload Image', 
                     validators=[
                         FileRequired(),
                         FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
                     ])
    submit = SubmitField('Upload')

# Form for document upload
class DocumentUploadForm(FlaskForm):
    document = FileField('Upload Document', 
                        validators=[
                            FileRequired(),
                            FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')
                        ])
    submit = SubmitField('Upload')

# Image upload route
@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    form = ImageUploadForm()
    
    if form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return f'''
        <html>
        <head><title>Upload Successful</title></head>
        <body>
            <h2>Upload Successful!</h2>
            <p>File: {filename}</p>
            <img src="/uploads/{filename}" alt="Uploaded image" style="max-width: 500px;">
            <br><br>
            <a href="/upload-image">Upload another image</a>
        </body>
        </html>
        '''
    
    return render_template_string('''
    <html>
    <head><title>Upload Image</title></head>
    <body>
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
    </body>
    </html>
    ''', form=form)

# Document upload route
@app.route('/upload-document', methods=['GET', 'POST'])
def upload_document():
    form = DocumentUploadForm()
    
    if form.validate_on_submit():
        file = form.document.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return f'''
        <html>
        <head><title>Upload Successful</title></head>
        <body>
            <h2>Document Uploaded Successfully!</h2>
            <p>File: {filename}</p>
            <p>File saved to: {filepath}</p>
            <a href="/upload-document">Upload another document</a>
        </body>
        </html>
        '''
    
    return render_template_string('''
    <html>
    <head><title>Upload Document</title></head>
    <body>
        <h2>Upload Document</h2>
        <form method="POST" enctype="multipart/form-data">
            {{ form.hidden_tag() }}
            <p>
                {{ form.document.label }}<br>
                {{ form.document() }}
                {% if form.document.errors %}
                    {% for error in form.document.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            <p>{{ form.submit() }}</p>
        </form>
    </body>
    </html>
    ''', form=form)

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Basic file upload without Flask-WTF (for comparison)
@app.route('/upload-basic', methods=['GET', 'POST'])
def upload_basic():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file selected!'
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No file selected!'
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'File {filename} uploaded successfully!'
    
    return '''
    <html>
    <head><title>Basic Upload</title></head>
    <body>
        <h2>Upload File (Basic)</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

