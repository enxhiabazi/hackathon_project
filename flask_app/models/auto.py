from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Auto:
    db_name = 'eco_auto'
    def __init__( self , data ):
        self.id = data['id']
        self.comments = data['comments']
        self.make = data['make']
        self.model = data['model']
        self.price = data['price']
        self.year = data['year']
        self.image = data['image']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #READ
    @classmethod
    def get_auto_by_id(cls, data):
        query = "SELECT * FROM autos WHERE autos.id = %(auto_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    #READ
    @classmethod
    def get_autos_and_their_users(cls, data):
        query = "select * from autos left join users on autos.user_id = users.id where autos.id = %(auto_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    #READ
    @classmethod
    def get_all(cls):
        query = "Select *, COUNT(likes.auto_id) as num_likes FROM autos left join actions on actions.auto_id = autos.id left JOIN users ON autos.user_id = users.id left JOIN likes ON autos.id = likes.auto_id where autos.isAvailable=0 GROUP BY autos.id ORDER BY autos.updated_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        autos = []
        if results:
            for auto in results:
                autos.append(auto)
            return autos
        return autos
    #READ
    @classmethod
    def get_all_rent(cls):
        query = "Select *, COUNT(likes.auto_id) as num_likes FROM autos left join actions on actions.auto_id = autos.id left JOIN users ON autos.user_id = users.id left JOIN likes ON autos.id = likes.auto_id  where autos.isAvailable=1 GROUP BY autos.id ORDER BY autos.updated_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        autos = []
        if results:
            for auto in results:
                autos.append(auto)
            return autos
        return autos
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO autos (make, model, price, year, comments, new_used, image, isAvailable, user_id) VALUES ( %(make)s, %(model)s, %(price)s, %(year)s, %(comments)s, %(new_used)s, %(image)s, %(isAvailable)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data) 
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE autos SET make = %(make)s, model = %(model)s, price = %(price)s, year = %(year)s, new_used = %(new_used)s,comments = %(comments)s WHERE autos.id = %(auto_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM autos WHERE autos.id = %(auto_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #DELETE
    @classmethod
    def deleteAllLikes(cls, data):
        query = "DELETE FROM likes WHERE auto_id = %(auto_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    #DELETE
    @classmethod
    def deleteAllSaves(cls, data):
        query = "DELETE FROM saves WHERE auto_id = %(auto_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    #CREATE  #add like
    @classmethod
    def addLike(cls, data):
        query = "INSERT INTO likes (auto_id, user_id) VALUES ( %(auto_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE #remove like
    @classmethod
    def unLike(cls, data):
        query = "DELETE FROM likes WHERE auto_id = %(auto_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #CREATE  #add save
    @classmethod
    def addSave(cls, data):
        query = "INSERT INTO saves (auto_id, user_id) VALUES ( %(auto_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE #remove save
    @classmethod
    def unSave(cls, data):
        query = "DELETE FROM saves WHERE auto_id = %(auto_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    #CREATE  #sent comments to comments table in db
    @classmethod
    def comment(cls, data):
        query = "INSERT INTO comments (comments, auto_id, user_id) VALUES ( %(comments)s,%(auto_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #DELETE  #remove comment
    @classmethod
    def deleteComment(cls, data):
        query = "DELETE FROM comments WHERE auto_id = %(auto_id)s and user_id = %(user_id)s and comments.id = %(comments_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #DELETE all comments
    @classmethod
    def deleteAllComments(cls, data):
        query = "DELETE FROM comments WHERE auto_id = %(auto_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #READ  #get comment from comments table in db
    @classmethod
    def get_auto_comments(cls, data):
        query = "SELECT autos.id as autos_id, comments.id,comments.comments,comments.user_id, comments.updated_at,comments.auto_id, users.first_name, users.last_name FROM comments LEFT JOIN autos on comments.auto_id = autos.id LEFT JOIN users on comments.user_id = users.id WHERE autos.id = %(auto_id)s ORDER BY comments.updated_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        comments = []
        if results:
            for comment in results:
                comments.append(comment)
            return comments
        return comments
    
    #READ #get those who liked the auto
    @classmethod
    def get_auto_likers(cls, data):
        query = "SELECT * from likes LEFT JOIN users on likes.user_id = users.id WHERE auto_id = %(auto_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfLikes = []
        if results:
            for row in results:
                nrOfLikes.append(row['email'])
            return nrOfLikes
        return nrOfLikes

    #READ
    @classmethod
    def get_users_autos(cls, data):
        query="SELECT autos.id, autos.user_id, autos.image, autos.comments, users.first_name as first_name, users.last_name, autos.updated_at, COUNT(likes.auto_id) as num_likes FROM autos LEFT JOIN users ON autos.user_id = users.id LEFT JOIN likes ON autos.id = likes.auto_id WHERE users.id = %(user_id)s GROUP BY autos.id ORDER BY autos.created_at DESC;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersAutos = []
        if results:
            for row in results:
                usersAutos.append(row)
            return usersAutos
        return usersAutos

    @staticmethod
    def validate_auto(auto):
        is_valid = True
        if len(auto['make']) <2:
            flash('Make should be more than 2 characters!', 'make')
            is_valid= False
        if len(auto['model']) <2:
            flash('Model should be more than 2 characters!', 'model')
            is_valid= False
        if auto['price'] == '':
            flash('Price should not be empty!', 'price')
            is_valid= False
        if auto['price'] != '':
            if int(auto['price']) <0:
                flash('Price should not be less than zero', 'price')
                is_valid = False
        if auto['year'] == '':
            flash('Year should not be empty!', 'year')
            is_valid= False        
        if len(auto['new_used']) <2:
            flash('It should be more than 2 characters!', 'new_used')
            is_valid= False 
        if len(auto['comments']) <2:
            flash('Comment should be more than 2 characters!', 'comment')
            is_valid= False   
        return is_valid
        