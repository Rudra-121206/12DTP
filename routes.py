from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)


def insert_database(*args):
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    if len(args) == 1:
        cur.execute(args[0])
    else:
        argument_tuple = ()
        for i in range(1, len(args)):
            argument_tuple += (args[i],)
        cur.execute(args[0], argument_tuple)
    conn.commit()
    conn.close()


# Call function and arguments should be in this order:
# Statement -> OPTIONAL: arguments -> mode (1 = fetchall() and 2 = fetchone())
def select_database(*args):
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    if len(args) == 2:
        cur.execute(args[0])
    else:
        argument_tuple = ()
        for i in range(1, len(args)-1):
            argument_tuple += (args[i],)
        cur.execute(args[0], argument_tuple)
    if args[-1] == 1:
        results = cur.fetchall()
    else:
        results = cur.fetchone()
    conn.close()
    return results


@app.route("/")
def home():
    return render_template("home.html", title="Rudra's restaurant")


@app.route("/menu")
def menu():
    menu = select_database('SELECT * FROM Recipe ORDER BY recipe_name ASC;', 1)
    return render_template("menu.html", title="menu", menu=menu)


# displays admin informmation
@app.route("/admin")
def admin():
    inventory = select_database('SELECT * FROM Inventory ORDER BY \
item_name ASC;', 1)
    return render_template("admin.html", title="admin", inventory=inventory)


@app.route("/our story")
def our_story():
    return render_template("our_story.html", title="our_story")


@app.route("/customer_purchase", methods=['GET'])
def customer_purchase():
    recipes = select_database('SELECT * FROM Recipe ORDER BY \
recipe_name ASC;', 1)
    return render_template("costumer_purchase.html", recipes=recipes)


@app.route("/customer_purchase", methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    order = request.form.getlist('order')
    insert_database('INSERT INTO Orders(order_name, phone_no) \
VALUES (?,?)', name, phone)
    token = select_database('SELECT order_id FROM Orders ORDER BY \
order_id DESC LIMIT 1', 2)
    for i in order:
        insert_database('INSERT INTO Recipe_Order(recipe_id, order_id) \
VALUES (?,?)', i, token[0])
        
    return redirect(url_for('success'))


@app.route("/success", methods=['GET'])
def success():
    token = select_database('SELECT order_id FROM Orders ORDER BY \
order_id DESC LIMIT 1', 2)
    return (f"Your order is successful, your order token is {token[0]}")




if __name__ == "__main__":
    app.run(debug=True)