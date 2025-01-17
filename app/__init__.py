from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    #if test_config is None:
    if not test_config: # pragma: no cover
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    db.init_app(app)
    migrate.init_app(app, db)
    # Import models here for Alembic setup
    from app.models.task import Task
    from app.models.goal import Goal


    # Register Blueprints here
    # Task Model
    from .task_routes import tasks_bp
    app.register_blueprint(tasks_bp)
    # Goal Model 
    from .goal_routes import goals_bp
    app.register_blueprint(goals_bp)

    return app
