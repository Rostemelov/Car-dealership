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

class Customer(db.Model):

class Showroom(db.Model):

class Sales(db.Model):

class Employee(db.Model):

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

if __name__ == "__main__":
    app.run(debug =True)