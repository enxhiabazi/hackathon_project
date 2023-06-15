from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
phone_number_pattern = re.compile(r"^\+?[1-9]\d{1,14}$")


class User:
    db_name = 'eco_auto'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #READ
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return results
    
    #READ
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return results
    
    #READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users
    #merr postet qe ka bere like user-i i loguar
    #READ
    @classmethod
    def get_user_liked_autos(cls, data):
        query = "SELECT auto_id as id from likes WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likedAutos = []
        if results:
            for row in results:
                likedAutos.append(row['id'])
            return likedAutos
        return likedAutos
    #READ
    @classmethod
    def get_user_saved_autos(cls, data):
        query = "SELECT auto_id as id from saves WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        savedAutos = []
        if results:
            for row in results:
                savedAutos.append(row['id'])
            return savedAutos
        return savedAutos
    @classmethod
    def get_user_saved_autos_all(cls, data):
        query = "Select *, COUNT(likes.auto_id) as num_likes FROM autos left join actions on actions.auto_id = autos.id left JOIN users ON autos.user_id = users.id left JOIN likes ON autos.id = likes.auto_id left join saves on saves.auto_id = autos.id WHERE saves.user_id = %(user_id)s GROUP BY saves.auto_id;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        savedAutos = []
        if results:
            for row in results:
                savedAutos.append(row)
            return savedAutos
        return savedAutos
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, phone_number, email, password, isVerified, verificationCode) VALUES ( %(first_name)s, %(last_name)s,%(phone_number)s, %(email)s, %(password)s,%(isVerified)s,%(verificationCode)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
     
    #UPDATE
    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE users SET  verificationCode = %(verificationCode)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    #UPDATE
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE users set isVerified = 1 WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        
        if len(user['first_name']) <2:
            flash('First name should be more than 2 characters!', 'firstNameRegister')
            is_valid= False
        if len(user['last_name']) <2:
            flash('Last name should be more than 2 characters!', 'lastNameRegister')
            is_valid= False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) <8:
            flash('Password should be more then 8 characters!', 'passwordRegister')
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match!', 'confirmPasswordRegister')
            is_valid = False
        if not phone_number_pattern.match(user['phone_number']):
           flash("Invalid phone number","phoneNumberRegister")
           is_valid = False
        return is_valid
        