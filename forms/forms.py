from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, EqualTo
from wtforms import StringField, EmailField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()], render_kw={"placeholder": "Firstname"})
    lastname = StringField("Lastname", validators=[DataRequired()], render_kw={"placeholder": "Lastname"})
    email = EmailField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

class AddProducts(FlaskForm):
    productName = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Product name"})
    description = StringField("Description", validators=[DataRequired()], render_kw={"placeholder": "Product description"})
    price = StringField("Price", validators=[DataRequired()], render_kw={"placeholder": "Product price"})
    image = FileField("Image", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'File format not allowed!')])
    submit = SubmitField("Add product")



