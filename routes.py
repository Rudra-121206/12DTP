
import sqlite3
from flask import Flask, render_template, abort
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms_alchemy import QuerySelectField, QuerySelectMultipleField
from wtforms import StringField, IntegerField, BooleanField, RadioField, SelectMultipleField


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Inventory_management_system.db'
db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("home.html",title= "Rudra's restaurant")



@app.route("/menu")
def menu():
    conn = sqlite3.connect('Inventory management system.db')
    cur = conn.cursor
    cur.execute('SELECT * FROM Recipe ORDER BY name ASC;')
    menu = cur.fetchall()
    print(menu)
    conn.close()
    return render_template("menu.html",title= "menu")



@app.route("/admin")
def admin():
    conn = sqlite3.connect('Inventory management system.db')
    cur = conn.cursor
    cur.execute('SELECT * FROM inventory ORDER BY name ASC;')
    inventory = cur.fetchall()
    print(inventory)
    return render_template("admin.html",title= "admin")



@app.route("/our story")
def our_story():
    return render_template("our_story.html",title= "our_story")
    
    

@app.route("/customer_purchase", methods = ["GET","POST"])    
def customer_purchase():
    form = customer_purchase()
    form.dishes.query =  Recipe.query.all()
    return render_template("our_story.html", )
    
   
if __name__ == "__main__":
    app.run()



