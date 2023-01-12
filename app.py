#!/usr/bin/env python3
from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import datetime





#Initialize the app from Flask
app=Flask(__name__)
#Configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
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
    sales = db.relationship('Sales', backref='car', lazy=True)

    def __repr__(self) -> str:
        return '<Car %r>' % self.car_id

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    sales = db.relationship('Sales', backref='customer', lazy=True)
    def __repr__(self) -> str:
        return '<Customer %r>' % self.customer_id

class Showroom(db.Model):
    showroom_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'), nullable=False)
    sales = db.relationship('Sales', backref='showroom', lazy=True)
    def __repr__(self) -> str: 
        return '<Showroom %r>' % self.showroom_id

class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password=db.Column(db.String(80), nullable=False)
    showroom = db.relationship('Showroom', backref='manager', lazy=True)
    def __repr__(self) -> str: 
        return '<Manager %r>' % self.manager_id


class Sales(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    showroom_id = db.Column(db.Integer, db.ForeignKey('showroom.showroom_id'), nullable=False)
    date = db.Column(db.DateTime(80), default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    def __repr__(self) -> str:
        return '<Sales %r>' % self.sales_id

with app.app_context():
    db.create_all()
    print("Tables updated successfully!")





#Define structure of the app
@app.route('/', methods=['GET', 'POST'])
def login():
    #Add operation
    if(request.method=='POST'):
        car_id=request.form['car_id']
        model=request.form['model']
        year=request.form['year']
        color=request.form['color']
        price=request.form['price']
        quantity=request.form['quantity']
        new_car=Car(car_id=car_id, model=model, year=year, color=color, price=price, quantity=quantity)
        db.session.add(new_car)
        db.session.commit()
        return redirect('/')
    carsdb=Car.query.all()
    return render_template('login.html', carsdb=carsdb)

@app.route('/home', methods=['GET', 'POST'])
def home():
    #Update operation
    if(request.method=='POST'):
        carid=request.form['car_id']
        quanTity=request.form['quantity']
        db.session.query(Car).filter_by(car_id=carid).update({'quantity':Car.quantity+quanTity})
        db.session.commit()
        return redirect('/')
    return "Home Page"

@app.route('/sell', methods=['GET', 'POST'])
def sell():
   # sell operation
   if(request.method=='POST'):
        carid=request.form['car_id']
        db.session.query(Car).filter_by(car_id=carid).update({'quantity':Car.quantity-1})
        db.session.commit()
        return redirect('/')
   return "Sell Page"

@app.route('/view_db', methods=['GET', 'POST'])
def viewdb():
    #Delete operation
    if(request.method=='POST'):
        carid=request.form['car_id']
        car_to_delete=Car.query.get(carid)
        db.session.delete(car_to_delete)
        db.session.commit()
        return redirect('/')
    return "View DB Page"

@app.route('/crud_db')
def crud():
    #return render_template('viewdb.html')

    return "Setup DB Page"



if __name__ == "__main__":
    app.run(debug =True)
