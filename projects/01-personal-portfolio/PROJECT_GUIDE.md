# Complete Guide: Building Your Personal Portfolio Website 📚

## Welcome! 👋

This guide will teach you EVERYTHING step by step. We'll build a beautiful portfolio website together!

## Part 1: Understanding What We're Building 🎯

### What is a Portfolio Website?

**Portfolio** = A collection of your work

Think of it like:
- **Art Portfolio** = Artist shows their paintings
- **Your Portfolio** = You show your coding projects
- **Website** = Everyone on internet can see it!

**We're building a website to show off your work!**

### What Pages Do We Need?

1. **Home Page** (`/`) - First page people see
2. **About Page** (`/about`) - Tell people about you
3. **Projects Page** (`/projects`) - Show your projects
4. **Contact Page** (`/contact`) - How to reach you

**4 pages = Complete website!**

## Part 2: Setting Up Your Project 🛠️

### Step 1: Create Project Structure

**Folders we need:**
- `templates/` - For HTML files
- `static/` - For CSS and images

**Why?**
- **Templates** = HTML pages (what people see)
- **Static** = CSS (makes it pretty) and images

### Step 2: Install Flask

**What is Flask?**
Flask = Tool that helps us build websites

**How to install:**
```bash
pip install flask
```

**That's it! Flask is ready!**

## Part 3: Creating Your First Flask App 🚀

### What is app.py?

**app.py** = The main file that runs your website

Think of it like:
- **app.py** = The brain of your website
- **It controls** = What happens when people visit

### Creating app.py:

```python
# Import Flask (we need this!)
from flask import Flask, render_template

# Create Flask app (this is your website!)
app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

**Let's understand each part:**

1. **`from flask import Flask`** = Get Flask tools
2. **`app = Flask(__name__)`** = Create your website
3. **`@app.route('/')`** = When someone visits homepage
4. **`def home()`** = What to do (show index.html)
5. **`app.run(debug=True)`** = Start the website

**Simple! Right?**

## Part 4: Creating Templates 📄

### What are Templates?

**Templates** = HTML files that show content

Think of it like:
- **Template** = A blank page with your content
- **Flask** = Fills it with information
- **Browser** = Shows it to people

**Templates = What people see!**

### Creating Base Template:

**Why base template?**
- **Base template** = Like a frame
- **Other pages** = Use the same frame
- **Saves time** = Don't repeat code!

**`templates/base.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Portfolio{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <!-- Navigation (menu at top) -->
    <nav>
        <div class="container">
            <a href="/" class="logo">My Portfolio</a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/projects">Projects</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Main content (changes per page) -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer (bottom of page) -->
    <footer>
        <p>&copy; 2024 My Portfolio. All rights reserved.</p>
    </footer>
</body>
</html>
```

**What's happening:**
- **`{% block title %}`** = Place for page title
- **`{% block content %}`** = Place for page content
- **`{{ url_for('static', ...) }}`** = Link to CSS file

**Jinja2 = Flask's template language!**

## Part 5: Creating Pages 📑

### Home Page (index.html):

**`templates/index.html`:**
```html
{% extends "base.html" %}

{% block title %}Home - My Portfolio{% endblock %}

{% block content %}
<div class="hero">
    <div class="container">
        <h1>Welcome to My Portfolio!</h1>
        <p>Hi! I'm a web developer passionate about creating amazing websites.</p>
        <a href="/about" class="btn">Learn More About Me</a>
    </div>
</div>

<div class="container">
    <section class="intro">
        <h2>What I Do</h2>
        <div class="skills">
            <div class="skill">
                <h3>Web Development</h3>
                <p>I build beautiful and functional websites using Flask and Python.</p>
            </div>
            <div class="skill">
                <h3>Design</h3>
                <p>I create user-friendly and attractive designs.</p>
            </div>
            <div class="skill">
                <h3>Problem Solving</h3>
                <p>I love solving complex problems with code.</p>
            </div>
        </div>
    </section>
</div>
{% endblock %}
```

**What's happening:**
- **`{% extends "base.html" %}`** = Use base template
- **`{% block content %}`** = Put content here
- **HTML tags** = Structure the page

### About Page:

**`templates/about.html`:**
```html
{% extends "base.html" %}

{% block title %}About Me - My Portfolio{% endblock %}

{% block content %}
<div class="container">
    <section class="about">
        <h1>About Me</h1>
        <div class="about-content">
            <div class="about-text">
                <h2>Hello! I'm [Your Name]</h2>
                <p>
                    I'm a passionate web developer who loves creating amazing 
                    websites and applications. I enjoy learning new technologies 
                    and solving interesting problems.
                </p>
                <p>
                    When I'm not coding, I love reading, playing games, and 
                    exploring new places. I believe in continuous learning and 
                    always strive to improve my skills.
                </p>
                <h3>My Skills</h3>
                <ul>
                    <li>Python Programming</li>
                    <li>Flask Web Development</li>
                    <li>HTML & CSS</li>
                    <li>JavaScript</li>
                    <li>Database Design</li>
                </ul>
            </div>
        </div>
    </section>
</div>
{% endblock %}
```

### Projects Page:

**`templates/projects.html`:**
```html
{% extends "base.html" %}

{% block title %}My Projects - My Portfolio{% endblock %}

{% block content %}
<div class="container">
    <section class="projects">
        <h1>My Projects</h1>
        <div class="projects-grid">
            <div class="project-card">
                <h3>Project 1: Personal Portfolio</h3>
                <p>This very website! Built with Flask and Python.</p>
                <a href="#" class="btn">View Project</a>
            </div>
            <div class="project-card">
                <h3>Project 2: Todo App</h3>
                <p>A simple todo application to manage tasks.</p>
                <a href="#" class="btn">View Project</a>
            </div>
            <div class="project-card">
                <h3>Project 3: Weather App</h3>
                <p>An app that shows weather information.</p>
                <a href="#" class="btn">View Project</a>
            </div>
        </div>
    </section>
</div>
{% endblock %}
```

### Contact Page:

**`templates/contact.html`:**
```html
{% extends "base.html" %}

{% block title %}Contact Me - My Portfolio{% endblock %}

{% block content %}
<div class="container">
    <section class="contact">
        <h1>Get In Touch</h1>
        <p>I'd love to hear from you! Feel free to reach out.</p>
        <div class="contact-info">
            <div class="contact-item">
                <h3>Email</h3>
                <p>your.email@example.com</p>
            </div>
            <div class="contact-item">
                <h3>GitHub</h3>
                <p><a href="https://github.com/yourusername">github.com/yourusername</a></p>
            </div>
            <div class="contact-item">
                <h3>LinkedIn</h3>
                <p><a href="https://linkedin.com/in/yourusername">linkedin.com/in/yourusername</a></p>
            </div>
        </div>
    </section>
</div>
{% endblock %}
```

## Part 6: Adding Routes in app.py 🛣️

### Complete app.py:

```python
from flask import Flask, render_template

# Create Flask app
app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Projects page
@app.route('/projects')
def projects():
    return render_template('projects.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```

**What each route does:**
- **`/`** = Home page
- **`/about`** = About page
- **`/projects`** = Projects page
- **`/contact`** = Contact page

**Routes = URLs that show different pages!**

## Part 7: Adding CSS Styling 🎨

### What is CSS?

**CSS** = Makes your website pretty!

Think of it like:
- **HTML** = The structure (skeleton)
- **CSS** = The styling (clothes and makeup!)
- **Together** = Beautiful website!

**CSS = Makes it look good!**

### Creating style.css:

**`static/style.css`:**
```css
/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
nav {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
}

nav .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #3498db;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 4rem 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 2rem;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #2980b9;
}

/* Sections */
section {
    padding: 3rem 0;
}

h1 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: #2c3e50;
}

h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #34495e;
}

/* Skills grid */
.skills {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.skill {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.skill h3 {
    color: #3498db;
    margin-bottom: 1rem;
}

/* About section */
.about-content {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.about-content ul {
    margin-top: 1rem;
    margin-left: 2rem;
}

.about-content li {
    margin: 0.5rem 0;
}

/* Projects grid */
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.project-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.project-card:hover {
    transform: translateY(-5px);
}

.project-card h3 {
    color: #3498db;
    margin-bottom: 1rem;
}

/* Contact section */
.contact-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.contact-item {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.contact-item h3 {
    color: #3498db;
    margin-bottom: 1rem;
}

.contact-item a {
    color: #3498db;
    text-decoration: none;
}

.contact-item a:hover {
    text-decoration: underline;
}

/* Footer */
footer {
    background-color: #2c3e50;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

/* Responsive design */
@media (max-width: 768px) {
    .nav-links {
        flex-direction: column;
        gap: 1rem;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
}
```

**CSS = Makes everything beautiful!**

## Part 8: Running Your Website 🚀

### Step 1: Install Flask

```bash
pip install flask
```

### Step 2: Run the App

```bash
python app.py
```

### Step 3: Open Browser

Go to: `http://localhost:5000`

**Your website is live!**

## Part 9: Understanding Everything 🧠

### How It All Works:

1. **User visits** `http://localhost:5000/`
2. **Flask sees** route `/`
3. **Flask calls** `home()` function
4. **Function returns** `index.html` template
5. **Template uses** `base.html` for layout
6. **CSS styles** everything
7. **Browser shows** beautiful website!

**That's how Flask works!**

## Part 10: Customizing Your Portfolio ✨

### Change Your Information:

1. **Edit `about.html`** - Add your name and story
2. **Edit `projects.html`** - Add your real projects
3. **Edit `contact.html`** - Add your contact info
4. **Edit `style.css`** - Change colors and styles

**Make it yours!**

## What You've Learned! 🎓

✅ How to create a Flask app  
✅ How to create multiple pages  
✅ How to use templates  
✅ How to add CSS styling  
✅ How to create navigation  
✅ How Flask routing works  

## Next Steps 🚀

1. **Customize** - Add your own information
2. **Add images** - Put photos in `static/images/`
3. **Deploy** - Put it online (we'll learn this later!)
4. **Share** - Show it to friends!

---

**Congratulations! You built your first Flask website! 🎉**

