from flask import Flask, session, url_for, redirect, render_template, flash, send_file
from flask_session import Session
from flask_wtf import CSRFProtect
from forms.forms import LoginForm, RegisterForm, AddProducts
from cs50 import SQL
from werkzeug.utils import secure_filename
import os 
from io import BytesIO

db = SQL('sqlite:///instance/malonda.db')

app = Flask(__name__)

# Initialise session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# Configure secret key
app.config["SECRET_KEY"] = 'this_is_a_secret_key'

# secure the web froms 
csrf = CSRFProtect(app)

# index route
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Login form route
@app.route('/login', methods=['POST', 'GET'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not user:
            return "User not found!"
        
        user = user[0]
        if user['email'] == email and user['password'] == password:
            session['email'] = user['email']
            session['name'] = user['firstname']
            return redirect(url_for('dashboard'))
        flash("Wrong email or password")
    return render_template("login.html", title='Login', form=form)


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data

        firstname = firstname.upper()
        lastname = lastname.upper()

        email = form.email.data
        password = form.password.data

        db.execute("INSERT INTO users(firstname, lastname, email, password) VALUES(?, ?, ?, ?)", firstname, lastname, email, password)
        flash("Registered successfully!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route for dashboard
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    email = session.get('email')
    user = db.execute("SELECT id FROM users WHERE email = ?", (email,))
   
    if not user:
        return "User not found!", 404
    user_id = user[0]['id']
    total_products = db.execute("SELECT COUNT(*) AS total FROM products WHERE user_id = ?", user_id)

    return render_template('dashboard.html', username=session.get('name'), title='Dashboard', total_products=total_products[0])

#Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Products route
@app.route('/products')
def products():
    email = session.get('email')
    user = db.execute("SELECT id FROM users WHERE email = ?", (email,))
   
    if not user:
        return "User not found!", 404
    user_id = user[0]['id']

    products = db.execute("SELECT id, name, description, price FROM products WHERE user_id = ?", (user_id))

    return render_template('products.html', title='Products', products=products)

#Retrieve the image route
@app.route('/product_image/<product_id>')
def image(product_id):
    product = db.execute("SELECT image FROM products WHERE id = ?", (product_id))

    print(product)

    if product and product['image']:
        return send_file(BytesIO(product['image']), mimetype="image/jpeg")
    return "Image not found!", 404

# Add products route
@app.route('/add_products', methods=["GET", "POST"])
def add_products():
    user = db.execute("SELECT id FROM users WHERE email = ?", session.get('email'))
    if user:
        user_id = user[0]['id']

    form=AddProducts()

    if form.validate_on_submit():
        productname = form.productName.data
        description = form.description.data
        price = form.price.data
        image = form.image.data

        filename = secure_filename(image.filename)
        image_data = image.read() # Read image is binary data

        db.execute("INSERT INTO products(user_id, name, description, price, image) VALUES (?, ?, ?, ?, ?)", user_id, productname, description, price, image_data)
        flash("Product added!")        
        return redirect(url_for("products"))
    return render_template("add_products.html", form=form, title="Add Products")

# Delete product route
@app.route('/delete/<product_id>')
def delete(product_id):
    db.execute("DELETE FROM products WHERE id = ?", (product_id))
    return redirect(url_for('products'))

