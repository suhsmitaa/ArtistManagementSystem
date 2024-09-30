# config.py
import os

class Config:
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'devuser',
        'password': 'roooooot',
        'database': 'artist_management_system'
    }
    SECRET_KEY = os.environ.get('SECRET_KEY', 'AMS')
