from app.config.db_connection import connectToMySQL
from app.models.Rifa_number import Rifa_number
import random

class Voucher:
    def __init__(self, data):
        self.id = data['id']
        self.image_url = data['image_url']
        self.verified = data['verified']
        self.num_of_numbers = data['num_of_numbers']
        self.user_id = data['user_id']

    @classmethod
    def insert_voucher(cls, data):
        data.setdefault('verified', None)

        new_voucher_id = connectToMySQL().query_db('INSERT INTO voucher (image_url, verified, user_id, num_of_numbers) VALUES (%(image_url)s, %(verified)s, %(user_id)s, %(num_of_numbers)s);', data)
        return new_voucher_id

    @classmethod
    def get_voucher_from_user(cls, user_id):
        voucher_existant = connectToMySQL().query_db('SELECT * FROM voucher WHERE user_id = %(user_id)s;', { 'user_id': user_id })
        return voucher_existant[0] if voucher_existant else None

    @classmethod
    def verif_voucher(cls, data):
        get_voucher = connectToMySQL().query_db('SELECT * FROM voucher WHERE id = %(id)s', { 'id': data['id'] })
        connectToMySQL().query_db('UPDATE voucher SET verified = 1 WHERE id = %(id)s', { 'id': data['id'] })

        user_id = get_voucher[0]['user_id']

        all_numbers = connectToMySQL().query_db('SELECT * FROM rifa_number')
        if len(all_numbers) >= 200:
            return { 'full': 'No hay más números para comprar' }
            
        numbers_for_user = []
            # La lista empieza vacía, por lo que si es == a 2 no entraría en el bucle
        while len(numbers_for_user) < data['num_of_numbers']:
            random_number = random.randint(1, 200)
            number_used = connectToMySQL().query_db('SELECT * FROM rifa_number WHERE number = %(number)s;', { 'number': random_number })
            if not number_used:
                connectToMySQL().query_db('INSERT INTO rifa_number (number, user_id) VALUES (%(number)s, %(user_id)s);', { 'number': random_number, 'user_id': user_id })
                numbers_for_user.append(random_number)

        return numbers_for_user

    @classmethod
    def get_voucher_by_id(cls, id):
        voucher_existant = connectToMySQL().query_db('SELECT * FROM voucher WHERE id = %(id)s;', { 'id': id })
        return voucher_existant[0] if voucher_existant else None

    @classmethod
    def delete_vouchers(cls):
        connectToMySQL().query_db('UPDATE voucher SET verified = 0;')
        elim = connectToMySQL().query_db('DELETE FROM rifa_number;')
        return 'Números eliminados' if elim else 'Error en la base de datos'