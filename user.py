from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask_app import app
from flask import flash

# # create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User: 
    db = "login_and_registration"
    def __init__(self, data): #data is a dictionary { key: value }
        self.id = data['id']
        self.first_name= data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']
        self.posts = []

    #Insert Method/Query
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email_address, password) 
        VALUES (%(first_name)s,%(last_name)s,%(email_address)s,%(password)s);
        """
        #send query to the database to save the user info
        user_id = connectToMySQL(cls.db).query_db(query,data)
        return user_id
    
    #Get All Method/Query 
    @classmethod
    def get_all(cls):
        query = """
        SELECT * 
        FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        User = []
        for User in results:
            User.append(cls(User))
            return User
        
    #Get One Method/Query
    @classmethod
    def get_one(cls, id):
        query = """
        SELECT *
        FROM users 
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        user = cls(results [0])
        return user
    
    #Get by Email Method/Query 
    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * 
        FROM users 
        WHERE email_address = %(email)s;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:  
            return False
        return cls(result[0])
    
    #Validation for user form data
    @staticmethod
    def is_valid(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        #establishing a bool variable to return from function
        #validations and fields to include for first name
        if not user['first_name'].strip():
            is_valid = False
            flash("First Name Required", 'user')
        elif not user['first_name'].isalpha():
            is_valid = False
            flash("First Name should only contain letters", 'user')
        elif len(user['first_name']) < 3:
            is_valid = False
            flash("First Name must be at least 3 characters.")

        #validations and fields to include for last name
        if not user['last_name'].strip():
            is_valid = False
            flash("Last Name Required", 'user')
        elif not user['last_name'].isalpha():
            is_valid = False
            flash("Last Name should only contain letters", 'user')
        elif len(user['last_name']) < 3:
            is_valid = False
            flash("Last Name must be at least 3 characters.")

        #validations and fields to include for email
        if not user['email'].strip():
            is_valid = False
            flash("Email Required", 'user')
        if len(user['email']) < 3:
            is_valid = False
            flash("Email must be a Valid Email.")
        # test whether a field matches the pattern
        elif not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address!")
        #email already in database
        elif User.get_by_email({'email':user['email']}):
            is_valid = False
            flash("Email already in use")
            
        #validations and fields to include for password
        if not user["password"].strip():
            is_valid = False
            flash("Password Required", 'user')
        # checks password
        elif len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.", 'user')
        elif user['password'] != user['passConf']:
            is_valid = False
            flash("Passwords must match", 'user')
        
        # Validated
        return is_valid
        
    @staticmethod
    def validate_login(user):
        is_valid = True
        # checks email
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters", 'login')
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'login')
            is_valid = False
        # checks password
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters", 'login')
            is_valid = False
        return is_valid
        
        # checks database for emails in use
    @classmethod
    def check_database(cls, data):
        query = """
        SELECT * 
        FROM users 
        WHERE email_address = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
        #retrieve unique user
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * 
        FROM users 
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results [0]



