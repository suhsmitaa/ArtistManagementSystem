from flask import Flask
from utils.db import init_db
from routes.music import bp as music_bp
from routes.auth import bp as auth_bp
from routes.users import bp as user_bp
from routes.artists import bp as artist_bp
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(Config)

    init_db(app)

    # Register Blueprints
    app.register_blueprint(music_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(artist_bp)

    @app.route('/')
    def home():
        return "Welcome to the Music API!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 
