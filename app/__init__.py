from flask import Flask
from flask_cors import CORS
import os
# Import models, blueprints, and anything else needed to set up the app or database
from flasgger import Swagger
from .models import board, card
from .db import db, migrate
from .routes.board_routes import bp as board_bp
from .routes.card_routes import bp as cards_bp


def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)
    # Swagger UI info
    # default APIDOCS route endpoint is /apidocs
    # http://127.0.0.1:5000/apidocs/
    
    app.config['SWAGGER'] = {
        "title": "Inspiration Board API",
        "uiversion": 3,
        "description": "API for managing boards and cards with likes and assignments"
    }

    # Initialize app with SQLAlchemy db and Migrate
    Swagger(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints 
    app.register_blueprint(board_bp)
    app.register_blueprint(cards_bp)

    CORS(app)
    return app
