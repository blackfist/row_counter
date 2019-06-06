import flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from dotenv import load_dotenv
import json
import os

load_dotenv()
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

# Create our data model
class ExportRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(18))
    count = db.Column(db.Numeric(1, 6))

@app.route("/", methods=["GET"])
def get_main():
    return jsonify({
        "status": "ok",
        "message": "Not used. The root endpoint is not used"
    })

if __name__ == "__main__":
    app.run()