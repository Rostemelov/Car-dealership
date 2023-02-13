#!/usr/bin/env python3
from flask import Flask,session,g,render_template, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from inflection import camelize
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)
# Base = declarative_base()

app.secret_key=os.urandom(24)

class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    def _repr_(self):
        return '<Car %r>' % self.car_id

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    def _repr_(self):
        return '<Customer %r>' % self.customer_id

class Showroom(db.Model):
    showroom_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer(), nullable=False)
    def _repr_(self): 
        return '<Showroom %r>' % self.showroom_id

class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    showroom_id = db.Column(db.Integer, nullable=False)
    def _repr_(self): 
        return '<Manager %r>' % self.manager_id


class Sales(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    showroom_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    def _repr_(self):
        return '<Sales %r>' % self.sales_id


with app.app_context():
    db.create_all()
    print("Created all tables successfully")


@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route("/dropsession")
def dropsession():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['username'] == 'admin': 
            session.pop('username', None)
            if request.form['password'] == 'password':
                session['username'] = request.form['username']
                return redirect(url_for('home'))

    return render_template('index.html')

@app.route("/home/base", methods=['GET', 'POST'])
def base():
    if g.username:
        return render_template('base.html',username=session['username'])
    return redirect(url_for('index'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    if g.username:
        if request.method == 'POST':
            form_type = request.form['form_type']
            if form_type == 'view_database':
                return redirect(url_for('viewdb_fun'))
            elif form_type == 'crud':
                return redirect(url_for('crud'))
            else:
                # Handle unexpected form type
                pass
        else:
            return render_template('home.html',username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route("/home/viewdb", methods=['GET', 'POST'])
def viewdb_fun():
    if g.username:
        tablename = ""
        if request.method == 'POST':
            tablename = request.form['tablename']
            return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
        return render_template('viewdb.html', tablename=tablename,username=session['username'])
    return redirect(url_for('index'))

@app.route("/home/viewdb/<tablename>", methods=['GET'])
def viewdb_fun_table(tablename):
    if g.username:
        table = db.engine.execute(f'SELECT * FROM {tablename}')
        return render_template('viewdb.html', tablename=table,username=session['username'],displayname=tablename)
    return redirect(url_for('index'))

@app.route("/home/<tablename>/create", methods=['GET', 'POST'])
def create_record(tablename):
    if g.username:
        table_class = getattr(sys.modules[__name__], tablename.capitalize())
        if request.method == 'POST':
            data = request.form.to_dict()
            new_record = table_class(**data) 
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
        columns = table_class.__table__.columns.keys()
        return render_template('create_record.html', tablename=tablename, columns=columns,username=session['username'])
    return redirect(url_for('index'))

@app.route("/home/<tablename>/delete/<int:id>", methods=['GET', 'POST','DELETE'])
def delete_record(tablename,id):
    if g.username:
        id = request.form.get('id')
        print("*****************************************")
        # print(**tablename)
        print(tablename,type(tablename))
        table_class = getattr(sys.modules[__name__], tablename.capitalize())
        record = table_class.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for('viewdb_fun_table', tablename=tablename, username=session['username']))
    return redirect(url_for('index'))


@app.route("/home/crud")
def crud():
    if g.username:
        return render_template('crud.html',username=session['username'])
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
