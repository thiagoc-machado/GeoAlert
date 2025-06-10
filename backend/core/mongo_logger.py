# core/mongo_logger.py

from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
collection = db['ia_logs']

def log_ia_action(user_id: int, action_type: str, input_data: dict, result_data: dict):
    log_entry = {
        'user_id': user_id,
        'type': action_type,
        'input': input_data,
        'result': result_data,
        'timestamp': datetime.now()
    }
    try:
        collection.insert_one(log_entry)
    except Exception as e:
        pass
