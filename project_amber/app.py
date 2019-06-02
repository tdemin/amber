from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from project_amber.config import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config["database"]
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "works"
