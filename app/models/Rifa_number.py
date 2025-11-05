from app.config.db_connection import connectToMySQL

class Rifa_number:
    def __init__(self, data):
        self.id = data['id']
        self.number = data['number']
        self.user_id = data['user_id']
