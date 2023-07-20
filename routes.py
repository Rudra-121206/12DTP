from flask import Flask, render_template, abort
import sqlite3

#def create_app():
app = Flask(__name__)

    #with app.app_context():
        #init_db()

    #return app
#app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html",title= "Rudra's restaurant")



@app.route("/menu")
def menu():
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Recipe ORDER BY recipe_name ASC;')
    menu = cur.fetchall()
    print(menu)
    conn.close()
    return render_template("menu.html",title= menu)



@app.route("/admin")
def admin():
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM inventory ORDER BY item_name ASC;')
    inventory = cur.fetchall()
    print(inventory)
    return render_template("admin.html",title= "admin")



@app.route("/our story")
def our_story():
    return render_template("our_story.html",title= "our_story")
    
    

@app.route("/customer_purchase")    
def customer_purchase():



    return render_template("costumer_purchase.html",   )
    
if __name__=="__main__":
    app.run(debug=True)
 
    



