#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#Initialize the app from Flask
app=Flask(__name__)
#Configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cobra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Define the database model
class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str:
        return '<Car %r>' % self.car_id

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str:
        return '<Customer %r>' % self.customer_id

class Showroom(db.Model):
    showroom_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str: 
        return '<Showroom %r>' % self.showroom_id

class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str: 
        return '<Manager %r>' % self.manager_id


class Sales(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    showroom_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(80), default=datetime.utcnow, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str:
        return '<Sales %r>' % self.sales_id


#Define structure of the app
@app.route('/')
def login():
    car=Car( car_id =1, model='Toyota', year=2019, color='Red', price=10000, quantity=10)
    db.session.add(car)
    db.session.commit()
    return render_template('login.html')

@app.route('/home')
def home():
    #return render_template('add_removeCar.html')
    return "Home Page"

@app.route('/add_removeCar')
def add_removeCar():
    #return render_template('add_removeCar.html')
    return "Add Or Remove Car Page"

@app.route('/sell')
def sell():
   # return render_template('sell.html')
   return "Sell Page"

@app.route('/view_db')
def viewdb():
    #return render_template('viewdb.html')
    return "View DB Page"

if __name__ == "__main__":
    app.run(debug =True)
