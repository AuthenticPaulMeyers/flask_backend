from flask import Flask, session, url_for, redirect, render_template, flash
from flask_session import Session
from flask_wtf import CSRFProtect
from forms.forms import LoginForm, RegisterForm, AddProducts
from cs50 import SQL

db = SQL('sqlite:///instance/malonda.db')

app = Flask(__name__)

# Initialise session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# Configure secret key
app.config["SECRET_KEY"] = 'this_is_a_secret_key'
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
            if user['email'] == email:
                session['name'] = user['firstname']
                return render_template(url_for('dashboard'))
            flash("Wrong email or password")
        flash("wrong email of password")
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
