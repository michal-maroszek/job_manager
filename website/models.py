from . import db
from flask_login import UserMixin
import datetime


class User(db.Model, UserMixin):
    # id = db.Column(db.Integer <- type of data, primary_key=True <- defining if it has unique ID)
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(
        db.String(100), unique=True
    )  # unique = True means that no other user can have the same email
    password = db.Column(db.String(150))
    company = db.Column(db.String(150))
    jobs = db.relationship("Job")
    clients = db.relationship("Client")
    # two last variables store data for all of users jobs and clients


class Job(db.Model):
    user = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # foreign key to reference specific user "ONE TO MANY RELATIONSHIP"
    client = db.Column(
        db.Integer, db.ForeignKey("client.id")
    )  # foreign key to reference specific client
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    job_type = db.Column(db.String(100))
    status = db.Column(db.String(100))
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    location = db.Column(db.String(500))
    info = db.Column(db.String(10000))
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    def days_left(self):
        time_left = self.end_time - datetime.datetime.today()
        days_left = time_left.days
        return days_left


class Client(db.Model):
    user = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # foreign key to reference specific user
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    company = db.Column(db.String(150))
    adress = db.Column(db.String(300))
    phone = db.Column(db.Integer)
    email = db.Column(db.String(250))
    info = db.Column(db.String(10000))

    def __repr__(self):
        return f"{self.company}, {self.firstname} {self.lastname}"
