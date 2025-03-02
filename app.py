from flask import Flask, session, url_for, redirect, render_template, flash, send_file, request
from flask_session import Session
from flask_wtf import CSRFProtect
from forms.forms import LoginForm, RegisterForm, AddProducts, UpdatePassword, UpdateProfile, EditProducts
from cs50 import SQL
from werkzeug.utils import secure_filename
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
        if user:
            user = user[0]
            if user['email'] == email and user['password'] == password:
                session['id'] = user['id']
                session['name'] = user['firstname']
                return redirect(url_for('dashboard'))
            flash("Wrong email or password")
        flash("Wrong email or password")
    return render_template("login.html", title='Login', form=form)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        db.execute("INSERT INTO users(firstname, lastname, email, password) VALUES(?, ?, ?, ?)", firstname, lastname, email, password)
        flash("Registered successfully!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Route for dashboard
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    user_id = session.get('id')   
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
    user_id = session.get('id')
    products = db.execute("SELECT id, name, description, price FROM products WHERE user_id = ?", (user_id))
    if not products:
        return render_template('products.html', title='Products', message="No products available!")
    return render_template('products.html', title='Products', products=products)

#Retrieve the image route
@app.route('/product_image/<product_id>')
def image(product_id):
    product = db.execute("SELECT image FROM products WHERE id = ?", (product_id))

    if product and product[0]['image']:
        return send_file(BytesIO(product[0]['image']), mimetype="image/jpeg")
    return "Image not found!", 404

# Add products route
@app.route('/add_products', methods=["GET", "POST"])
def add_products():
    user_id = session.get('id')
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

#Profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form=UpdatePassword()

    user_id = session.get('id')
    user = db.execute("SELECT * FROM users WHERE id = (?)", user_id)
    if not user:
        flash("User not found!")
    
    user = user[0]

    if form.validate_on_submit():
        password = form.password.data
        db.execute("UPDATE users SET password = ? WHERE id = ?", password, user_id)
        flash("Password updated successfully!")
        return redirect(url_for('dashboard'))
    return render_template('profile.html', user=user, form=form)


# Market place route
@app.route('/market_place')
def market_place():
    user_id = session.get('id')
    products = db.execute("SELECT * FROM products WHERE NOT user_id = ?", user_id)
    return render_template('market.html', title='Market Place', products=products)


# update profile route
@app.route('/update_profile/<user_id>', methods=['POST', 'GET'])
def update_profile(user_id):
    form=UpdateProfile()

    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if not user:
        return redirect(url_for("error.html"))

    if request.method == 'GET':
        form.firstname.data = user[0]['firstname']
        form.lastname.data = user[0]['lastname']
        form.email.data = user[0]['email']

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data

        db.execute("UPDATE users SET firstname = ?, lastname = ?, email = ? WHERE id = ?", firstname, lastname, email, user_id)
        flash("Profile updated successfully!")
        return redirect(url_for('profile'))
    return render_template('update_profile.html', form=form)

# edit product route
@app.route('/edit_products/<product_id>', methods=["POST", "GET"])
def edit_product(product_id):
    form=EditProducts()
    product = db.execute("SELECT * FROM products WHERE id = ?", product_id)

    if request.method == "GET":
        form.productName.data = product[0]['name']
        form.description.data = product[0]['description']
        form.price.data = product[0]['price']
        form.image.data = product[0]['image']

    if form.validate_on_submit():
        productName = form.productName.data 
        description = form.description.data 
        price = form.price.data 
        image = form.image.data 

        filename = secure_filename(image.filename)
        image_data = image.read() # Read image is binary data
        db.execute("UPDATE products SET name = ?, description = ?, price = ?, image = ? WHERE id = ?", productName, description, price, image_data, product_id)
        flash("Product updated!")        
        return redirect(url_for("products"))
        
    return render_template('edit_product.html', title='Update Product', form=form, product=product)