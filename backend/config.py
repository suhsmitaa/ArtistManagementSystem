import os

DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'devuser',
    'password': 'roooooot',
    'database': 'artist_management_database'
}

SECRET_KEY = os.environ.get('SECRET_KEY') or 'sushmita_key'