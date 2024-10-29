from flask_app import app
from flask import render_template,request,redirect, session
from flask_app.models.user import User

#Initialize Bcrypt for password hashing
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Route for the login/registration form
@app.route("/")
def index():
    #Render the login/registration HTML template
    return render_template("index.html")

#Route for submitting the user registration form
@app.route("/user/register", methods=['POST'])
def register():
    #Validate the user's registration form data
    if User.is_valid(request.form):
    #Create a New User in the Database
        data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email_address': request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password']),
        }
        #send form data to a user.py User class
        #save user info to the DB
        session['user_id'] = User.create(data)
        return redirect('dashboard')
    return redirect('/')
