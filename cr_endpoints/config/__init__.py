from config.settings import load_config
from flask_sqlalchemy import SQLAlchemy
from pymilvus import connections

db = SQLAlchemy()


def init_config(app):
    config = load_config()
    app.config.from_object(config)


def init_sqlalchemy(app):
    print("\n=== {:30} ===\n".format("Start connecting to MySQL"))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql://{app.config['MYSQL_USER']}:{app.config['MYSQL_PASSWORD']}@{app.config['HOST']}/{app.config['MYSQL_DB']}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    print("Connected to MySQL")


def init_milvus_connection(app):
    print("\n=== {:30} ===\n".format("Start connecting to Milvus"))
    connections.connect(
        "default",
        host=app.config["HOST"],
        port=app.config["MILVUS_PORT"],
        user=app.config["MILVUS_USER"],
        password=app.config["MILVUS_PASSWORD"],
    )
    print("Connected to Milvus")
