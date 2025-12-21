# Flask-WTF Example
# This shows how to use Flask-WTF for better form handling

from flask import Flask, render_template_string
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo
import secrets

app = Flask(__name__)
# Generate a secret key (in production, use a fixed, secure key)
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Define the form class
class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

# Registration form example
class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=13, max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password', 
                                    message='Passwords must match')])
    submit = SubmitField('Register')

# Contact form route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Get form data
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Process the data (save to database, send email, etc.)
        return f'Thank you, {name}! We received your message and will reply to {email}.'
    
    # Show the form
    return render_template_string('''
    <html>
    <head><title>Contact Us</title></head>
    <body>
        <h1>Contact Us</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            
            <p>
                {{ form.name.label }}<br>
                {{ form.name() }}
                {% if form.name.errors %}
                    {% for error in form.name.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>
                {{ form.email.label }}<br>
                {{ form.email() }}
                {% if form.email.errors %}
                    {% for error in form.email.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>
                {{ form.message.label }}<br>
                {{ form.message() }}
                {% if form.message.errors %}
                    {% for error in form.message.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>{{ form.submit() }}</p>
        </form>
    </body>
    </html>
    ''', form=form)

# Registration form route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        age = form.age.data
        password = form.password.data
        
        # In real app, you'd hash the password and save to database
        return f'Registration successful! Welcome, {name}! (Age: {age})'
    
    return render_template_string('''
    <html>
    <head><title>Register</title></head>
    <body>
        <h2>Register</h2>
        <form method="POST">
            {{ form.hidden_tag() }}
            
            <p>
                {{ form.name.label }}<br>
                {{ form.name() }}
                {% if form.name.errors %}
                    {% for error in form.name.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>
                {{ form.email.label }}<br>
                {{ form.email() }}
                {% if form.email.errors %}
                    {% for error in form.email.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>
                {{ form.age.label }}<br>
                {{ form.age() }}
                {% if form.age.errors %}
                    {% for error in form.age.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>
                {{ form.password.label }}<br>
                {{ form.password() }}
                {% if form.password.errors %}
                    {% for error in form.password.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>
                {{ form.confirm_password.label }}<br>
                {{ form.confirm_password() }}
                {% if form.confirm_password.errors %}
                    {% for error in form.confirm_password.errors %}
                        <span style="color: red;">{{ error }}</span>
                    {% endfor %}
                {% endif %}
            </p>
            
            <p>{{ form.submit() }}</p>
        </form>
    </body>
    </html>
    ''', form=form)

if __name__ == '__main__':
    app.run(debug=True)

