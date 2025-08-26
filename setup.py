# NOTE: flask_bootstrap support provided via Bootstrap-Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
import os

# Create the Flask app instance and set up bootstrap
app = Flask(__name__)
Bootstrap5(app)

# Create an instance folder if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)

# Define a database path inside the instance folder
db_path = os.path.join(app.instance_path, "app.sqlite")

# Configuration for the SQL database
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy without directly associating it with the app
db = SQLAlchemy()

# Initialize App
def init_app():
    db.init_app(app)

    # Ensure the database file is created
    with app.app_context():
        if not os.path.exists(db_path):
            db.create_all()
            print(f"Database created at {db_path}")
    return app
