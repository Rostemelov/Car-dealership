#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

#Initialize the app from Flask
app=Flask(__name__)
#Configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Define the database model
class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    credit_card = db.Column(db.Integer, nullable=False)
class Showroom(db.Model):
    showroom_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer(80), nullable=False)
class Sales(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    showroom_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    showroom_id = db.Column(db.Integer, nullable=False)
#Define structure of the app
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return "Meow Meow Nigga"

@app.route('/add_removeCar')
def login():
    return render_template('add_removeCar.html')

@app.route('/sell')
def login():
    return render_template('sell.html')

@app.route('/view_db')
def login():
    return render_template('viewdb.html')

if __name__ == "__main__":
    app.run(debug =True)
