from flask_app import app
from flask import render_template,redirect, request, session, flash
from flask_app.models.user import User
from flask_app.controllers import items
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Route for the dashboard
@app.route("/dashboard")
def dashboard():
    # Check if the user is logged in 
    if 'user_id' not in session:
        # If the user is not logged in, redirect to the logout route
        return redirect('/logout')
    
    # Get the user ID from the session
    user_id = session['user_id']
    
    # Render the dashboard template with the user's data
    return render_template("dashboard.html", user=User.get_by_id(user_id))

#   Route for Login In User 
@app.route("/user/login", methods=['POST'])
def login():
    #Retrieve the user from the database based on the provided email 
    user = User.get_by_email(request.form)
    if not User.validate_login(request.form):
        #Redirect the user back to the login/registration form
        flash ("Invalid Email/Password")
        return redirect('/admin')    
    #Check if the user exists and the password is valid
    if not user or not bcrypt.check_password_hash(user.password, request.form ['password']):
        #Flash an error message if the email/password is invalid
        flash("Invalid Email/Password")
        #Redirect the user back to the login/registration form
        return redirect('/')
    #Store User's ID and First Name in Session
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    #Redirect the user to the dashboard
    return redirect('/dashboard')  

#Route for logging out the User
@app.route("/logout")
def logout():
    #Clear the User's session data
    session.clear()
    #Redirect the User to the login/registration page 
    return redirect('/')

@app.route("/dashboard/new_item")
def newitem():
    items.add_item
    return render_template('add_item.html')