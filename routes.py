from flask import Flask, render_template
from flask_wtf import Flaskform
from wtffroms_sqlalchemy.fields import QuerySelectField
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
RadioField)

app = Flask(__name__)

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
    
    

@app.route("customer_purchase")    
def customer_purchase():






