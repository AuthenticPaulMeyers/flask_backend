from flask import Flask, session, url_for, redirect, render_template, flash
from flask_session import Session
from flask_wtf import CSRFProtect

app = Flask(__name__)
# Initialise session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# Configure secret key
app.config["SECRET_KEY"] = 'this_is_a_secre_key'
csrf = CSRFProtect(app)

# index route
@app.route('/')
def index():
    return render_template('index.html')

