from app.config.db_connection import connectToMySQL

class Admin:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def insert_admin(cls, data):
        new_admin = connectToMySQL().query_db('INSERT INTO admin (email, password) VALUES (%(email)s, %(password)s);', data)
        return new_admin

    @classmethod
    def get_admin_by_email(cls, email):
        admin_existant = connectToMySQL().query_db('SELECT * FROM admin WHERE email = %(email)s;', { 'email': email })
        return admin_existant[0] if admin_existant else None

    @classmethod
    def get_admin_by_id(cls, id):
        admin_existant = connectToMySQL().query_db('SELECT * FROM admin WHERE id = %(id)s;', { 'id': id })
        return admin_existant[0] if admin_existant else None