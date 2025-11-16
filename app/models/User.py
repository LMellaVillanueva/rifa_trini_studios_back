from app.config.db_connection import connectToMySQL
from app.models.Rifa_number import Rifa_number
from app.models.Voucher import Voucher
import random

class User:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.phone = data['phone']
        self.verif = data['verif']
        self.email = data['email']

    @staticmethod
    def validate_user(user):
        errors = []
        if len(str(user['phone'])) > 9:
            errors.append('El teléfono no puede tener más de 10 dígitos')
        return errors

    @classmethod
    def insert_user(cls, data):
        data.setdefault('verif', None)
        # all_numbers = connectToMySQL().query_db('SELECT * FROM rifa_number')
        # if len(all_numbers) >= 200:
        #     return { 'full': 'No hay más números para comprar' }

        new_user_id = connectToMySQL().query_db('INSERT INTO user (name, phone, verif, email) VALUES (%(name)s, %(phone)s, %(verif)s, %(email)s);', data)

        return new_user_id
        # numbers_for_user = []

        # while True:
        #     random_number = random.randint(1, 200)
        #     number_used = connectToMySQL().query_db('SELECT * FROM rifa_number WHERE number = %(number)s;', { 'number': random_number })
        
        #     if not number_used:
        #         connectToMySQL().query_db('INSERT INTO rifa_number (number, user_id) VALUES (%(number)s, %(user_id)s);', { 'number': random_number, 'user_id': new_user_id })
        #         numbers_for_user.append(random_number)

        #     if len(numbers_for_user) == 2:
        #         return { 'user': get_user['name'], 'numbers': numbers_for_user, 'phone': get_user['phone'], 'voucher': get_user['voucher'] }     


    # @classmethod
    # def new_numbers_for_user(cls, user_id):
    #     all_numbers = connectToMySQL().query_db('SELECT * FROM rifa_number')
    #     if len(all_numbers) >= 200:
    #         return { 'full': 'No hay más números para comprar' }

    #     numbers_for_user = []
    #     while True:
    #         random_number = random.randint(1, 200)
    #         number_used = connectToMySQL().query_db('SELECT * FROM  rifa_number WHERE number = %(number)s', { 'number': random_number })

    #         if not number_used:
    #             connectToMySQL().query_db('INSERT INTO rifa_number (number, user_id) VALUES (%(number)s, %(user_id)s);', { 'number': random_number, 'user_id': user_id })
    #             numbers_for_user.append(random_number)

    #         if len(numbers_for_user) == 2:
    #             return numbers_for_user 

    # Concatenar el nuevo voucher a un user
    # @classmethod
    # def concat_voucher(cls, id, new_voucher):
    #     connectToMySQL().query_db( """
    #     UPDATE user
    #     SET voucher = CASE
    #         WHEN voucher IS NULL OR voucher = '' THEN %(new_voucher)s
    #         ELSE CONCAT(voucher, ',', %(new_voucher)s)
    #     END,
    #     verif = 0
    #     WHERE id = %(id)s;
    # """, { 'id': id, 'new_voucher': new_voucher })

    @classmethod
    def get_user_by_phone(cls, phone):
        user_existant = connectToMySQL().query_db('SELECT * FROM user WHERE phone = %(phone)s;', { 'phone': phone })
        return user_existant[0] if user_existant else None

    @classmethod
    def get_user_by_id(cls, user_id):
        user_existant = connectToMySQL().query_db('SELECT * FROM user WHERE id = %(user_id)s;', { 'user_id': user_id })
        return user_existant[0] if user_existant else None


    @classmethod
    def delete_user(cls, id):
        user_existant = connectToMySQL().query_db('SELECT * FROM user WHERE id = %(id)s;', { 'id': id })
        if not user_existant:
            return 'Este usuario no existe.'

        elim = connectToMySQL().query_db('DELETE FROM user WHERE id = %(id)s;', { 'id': id })

        return 'Usuario eliminado.' if elim else 'Error de conexión.'
        
    @classmethod
    def get_all_users(cls):
        # all_users = connectToMySQL().query_db("SELECT u.id AS user_id,u.name,u.phone,(SELECT GROUP_CONCAT(DISTINCT r.number ORDER BY r.number) FROM rifa_number r WHERE r.user_id = u.id) AS numbers,(SELECT GROUP_CONCAT(CONCAT(v.id, '|', v.image_url, '|', v.verified) SEPARATOR ';') FROM voucher v WHERE v.user_id = u.id) AS vouchers FROM user u;")
        all_users = connectToMySQL().query_db("SELECT u.id AS user_id, u.name, u.phone, u.email, GROUP_CONCAT(DISTINCT rn.number ORDER BY rn.number SEPARATOR ';') AS rifa_numbers, GROUP_CONCAT(DISTINCT CONCAT(v.id, '|', v.image_url, '|', v.verified, '|', v.num_of_numbers) SEPARATOR ';') AS vouchers FROM user u LEFT JOIN rifa_number rn ON rn.user_id = u.id LEFT JOIN voucher v ON v.user_id = u.id GROUP BY u.id, u.name, u.phone;")
        return all_users

    @classmethod
    def get_user_numbers(cls, id):
        user_existant = connectToMySQL().query_db('SELECT * FROM user WHERE id = %(id)s;', { 'id': id })
        if not user_existant:
            return 'Este usuario no existe.'

        user_with_numbers = connectToMySQL().query_db('select * from user LEFT JOIN rifa_number on user.id = rifa_number.user_id where user.id = %(id)s;', { 'id': id })
        print(user_with_numbers)
        return user_with_numbers

    @classmethod
    def delete_users(cls):
        connectToMySQL().query_db('DELETE FROM rifa_number;')
        connectToMySQL().query_db('DELETE FROM voucher;')
        connectToMySQL().query_db('DELETE FROM user;')
        return 'Users eliminados' 

    @classmethod
    def delete_numbers_of_user(cls, id):
        connection = connectToMySQL()
        try:
            connection.query_db('UPDATE voucher SET verified = 0 WHERE user_id = %(id)s;', { 'id': id })
            connectToMySQL().query_db('DELETE FROM rifa_number WHERE user_id = %(id)s;', { 'id': id })

            return 'Números eliminados con éxito' 
        
        except Exception:
            return 'Error en la base de datos'

    