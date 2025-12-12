from app.config.db_connection import connectToMySQL

class Rifa_number:
    def __init__(self, data):
        self.id = data['id']
        self.number = data['number']
        self.user_id = data['user_id']

    @classmethod
    def all_numbers(cls):
        all_numbers = connectToMySQL().query_db('SELECT * FROM rifa_number')
        
        return False if len(all_numbers) >= 1000 else True