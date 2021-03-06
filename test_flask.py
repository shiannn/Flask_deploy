import os
import json
import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def get_config():
    query = Booking.query.first()
    print(query)
    if not query:
        config = {}
    else:
        config = {
            'course': query.course,
            'date': query.date,
            'position': query.position,
            'last_update': query.last_update
        }
    
    return render_template('home.html', post = config)

@app.route("/", methods=['POST'])
def set_config():
    course = request.form['course']
    date = request.form['date']
    position = request.form['position']
    today = str(datetime.datetime.now())
    
    Booking.query.delete()
    booking = Booking(course, date, position, today)
    print(booking)
    db.session.add(booking)
    db.session.commit()

    config = {
        'course': course,
        'date': date,
        'position': position,
        'last_update': today
    }

    return render_template('home.html', post = config)

def main():
    db.drop_all()
    db.create_all()
    app.run()

class Booking(db.Model):
    """ Booking model """

    __tablename__ = "Booking"
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False) # unique
    position = db.Column(db.String(), nullable=False)
    last_update = db.Column(db.String(), nullable=False)

    def __init__(self, course, date, position, last_update):
        self.course = course
        self.date = date
        self.position = position
        self.last_update = last_update
    
    def __repr__(self):
        return "Booking {} {} {}".format(self.course, self.date, self.position)

if __name__ == '__main__':
    main()