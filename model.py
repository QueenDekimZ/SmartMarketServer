# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from handler import db

class Smartmarket(db.Model):
    __tablename__ = 'smartmarket'

    MachineNo = db.Column(db.Integer, primary_key=True)
    WaterNum = db.Column(db.Integer, nullable=False)
    MaidongNum = db.Column(db.Integer, nullable=False)
    RedbullNum = db.Column(db.Integer, nullable=False)
