import flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from dotenv import load_dotenv
import json
import os
import sys
from statistics import mean, stdev

load_dotenv()
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)
minimum_allowed = os.getenv("MINIMUM_ALLOWED", "10")
try:
    minimum_allowed = int(minimum_allowed)
except ValueError:
    sys.exit(
        "Value of environment variable MINIMUM_ALLOWED cannot be converted to an integer")

# Create our data model


class ExportRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(18))
    count = db.Column(db.SmallInteger)


@app.route("/", methods=["GET"])
def get_main():
    print(request.headers)
    return jsonify({
        "status": "ok",
        "message": "Not used. The root endpoint is not used"
    })


@app.route("/record", methods=["POST"])
def store_record_count():
    print("### HTTP POST received on /record. Header data is as follows")
    print(request.headers)
    print("### request.args data received is as follows")
    print(request.args)
    print("### request.form data received is as follows")
    print(request.form)
    print("### Combined form and args data is as follows")
    print(request.values)
    print("### Fallback Data received is as follows")
    print(request.data)
    print("### End diagnostic info")

    if request.values.get('userId', 'Missing') == 'Missing':
        return jsonify({"status": "error", "message": "post data did not contain a userId field"})
    if request.values.get('count', 'Missing') == 'Missing':
        return jsonify({"status": "error", "message": "post data did not contain a count field"})

    received_user_id = request.values.get('userId')
    received_count = request.values.get('count')

    record_count = 0
    try:
        record_count = int(received_count)
    except ValueError:
        return jsonify({"status": "error",
                        "message": "could not convert the count value {0} to an integer".format(received_count)})

    new_record = ExportRecord(
        user_id=received_user_id, count=record_count)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({
        "status": "successful"
    })


@app.route("/records/<user_id>", methods=['GET'])
def get_record_boundary(user_id):
    db_results = ExportRecord.query.filter_by(user_id=user_id).all()
    raw_counts = [record.count for record in db_results]

    # If the user has not been seen before then there might be no records. So return the minimum allowed
    if len(raw_counts) == 0:
        return jsonify({
            "status": "success",
            "max_allowed": 10
        })

    # Calculate the mean and std deviation of this user's previous activity
    mean = mean(raw_counts)
    stdev = stdev(raw_counts)
    ceiling = round(mean + (2*stdev))
    return jsonify({
        "status": "success",
        "max_allowed": ceiling
    })


if __name__ == "__main__":
    app.run()
