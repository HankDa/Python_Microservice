from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create Flask app instance
app = Flask(__name__)
# mysql://username:password@server/db
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

# Initialize SQLAlchemy and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

