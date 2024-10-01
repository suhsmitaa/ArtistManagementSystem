# routes/__init__.py

from flask import Blueprint

# Import blueprints
from .artists import bp as artists_bp
from .music import bp as music_bp
from .users import bp as users_bp  
from .auth import bp as auth_bp      

def init_app(app):
    app.register_blueprint(artists_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(users_bp)  
    app.register_blueprint(auth_bp)   
