from flask import Flask, render_template, abort, request, redirect, url_for
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
    return render_template("menu.html",title= "menu", menu = menu)


# displays admin informmation
@app.route("/admin")
def admin():
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Inventory ORDER BY item_name ASC;')
    inventory = cur.fetchall()
    print(inventory)
    return render_template("admin.html",title= "admin", inventory=inventory)



@app.route("/our story")
def our_story():
    return render_template("our_story.html",title= "our_story")


def insert_data(name, phone):
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO Orders(order_name, phone_no) VALUES(?,?)',(name, phone))
    conn.commit()
    conn.close()


def insert_data_joiningtable(token,name,phone,orders):
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    for orders in orders:
        cur.execute('INSERT  ')



        
    
        
    

@app.route("/customer_purchase", methods=['GET'])    
def customer_purchase():
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Recipe ORDER BY recipe_name ASC;')
    recipes = cur.fetchall()
    conn.close()
    return render_template("costumer_purchase.html",recipes=recipes )


@app.route("/customer_purchase", methods=['POST'])
def submit():
    
    name = request.form['name']
    phone = request.form['phone']
    order = request.form['order']
     
     
    insert_data(name, phone)
    return redirect(url_for('success'))    

@app.route("/success", methods=['GET'])
def success():
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    cur.execute('SELECT order_id FROM Orders ORDER BY order_id DESC LIMIT 1')
    token = cur.fetchone()
    return (f"Your order is successful, your order token is {token[0]}")



if __name__=="__main__":
    app.run(debug=True)
 
    



