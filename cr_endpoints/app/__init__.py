from flask import Flask
from flask_cors import CORS
from config import init_config, init_milvus_connection, db, init_sqlalchemy
from .models import db


def init_app():
    app = Flask(__name__)
    CORS(app)

    init_config(app)
    init_milvus_connection(app)
    init_sqlalchemy(app)

    # Import blueprints and register them here to avoid circular imports
    from .routes import milvus_bp

    app.register_blueprint(milvus_bp, url_prefix="/milvus")

    with app.app_context():
        db.create_all()

    return app
