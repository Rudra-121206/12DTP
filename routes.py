from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html",title= "Rudra's restaurant")



@app.route("/menu")
def menu():
    return render_template("menu.html",title= "menu")



@app.route("/admin")
def admin():
    return render_template("admin.html",title= "admin")



@app.route("/our story")
def our_story():
    return render_template("our_story.html",title= "our_story")
    
    





