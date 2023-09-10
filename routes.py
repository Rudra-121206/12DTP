from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


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


def get_price(token):
    orders = select_database('SELECT recipe_id, qty FROM Recipe_Order WHERE order_id = ?', token, 1)
    total_price = 0
    for order in orders: 
        price = select_database('SELECT price FROM Recipe where recipe_id = ?', order[0], 2) 
        price = price[0]*order[1]
        price = str(price)
        price = int(price)
        total_price = price + total_price
    return total_price


def adjust_stock(token):
    orders=select_database('SELECT order_id, recipe_id FROM Recipe_Order WHERE order_id = ?', token[0], 1)
    for order in orders:
        qty=order[1]
        recipe = order[0]
        results= select_database('SELECT * FROM Item_recipe WHERE recipe_id = ?', recipe, 1)
        for result in results:
            used_qty=result[0]
            print (used_qty)
            total_used_qty=used_qty*qty
            print(qty)
            print(total_used_qty)          
            item_id=result[2]
            print(item_id)
            original_qty=select_database('SELECT balance_qty FROM Inventory WHERE item_id = ?', item_id[0], 2)
            print(original_qty)
            changed_qty=original_qty[0]-total_used_qty
            print(changed_qty)
            insert_database('UPDATE Inventory SET balance_qty = ? WHERE item_id = ?', changed_qty, item_id)
    return 'done'

def check_stock():
    balance_qty=select_database('SELECT item_id, item_expiry, base_qty, balance_qty FROM Inventory', 1)
    status=True
    Date=(datetime.today())
    for balance in balance_qty:
        item_expiry=balance[1]
        item_expiry=str(item_expiry)
        item_expiry = datetime.strptime(item_expiry, '%Y-%m-%d')

        if balance[2]>balance[3]:
            status=False 
        elif Date>(item_expiry):
            status=False
            insert_database('UPDATE Inventory SET balance_qty = 0 WHERE item_id = ?', balance[0])      
        else:
            status=status
    
            
    return status





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
    x=(date.today())
    print(x)

    return render_template("home.html", title="Rudra's restaurant")


@app.route("/add_product", methods=['GET'])
def add_product():
    added_qty= request.args.get('added_qty')
    added_qty= int(added_qty)
    item_id= request.args.get('id')
    item_id = int(item_id)
    result= select_database('SELECT item_expiry, balance_qty FROM Inventory WHERE item_id = ?', item_id, 1)
    qty= result[0][1]
    qty= int(qty)
    changed_qty= added_qty+qty
    current_date = datetime.today()
    item_expiry=result[0][0]
    item_expiry=str(item_expiry)
    item_expiry = datetime.strptime(item_expiry, '%Y-%m-%d')
    expiry_date = current_date + relativedelta(months=2)
    expiry_date=str(expiry_date)
    expiry_date=(expiry_date.split(" "))
    expiry_date=expiry_date[0]
    if current_date>(item_expiry):
        insert_database('UPDATE Inventory SET item_expiry = ?, balance_qty = ? WHERE item_id = ?', expiry_date, added_qty, item_id)   
    else:
        insert_database('UPDATE Inventory SET item_expiry = ?, balance_qty = ? WHERE item_id = ?', expiry_date, changed_qty, item_id)

    return redirect(url_for("admin"))



@app.route("/menu")
def menu():
    menu = select_database('SELECT * FROM Recipe ORDER BY recipe_name ASC;', 1)
    return render_template("menu.html", title="menu", menu=menu)


# display admin informmation
@app.route("/admin")
def admin():
    inventory = select_database('SELECT * FROM Inventory ORDER BY \
item_name ASC;', 1)
    return render_template("admin.html", title="admin", inventory=inventory)

#display our story's page
@app.route("/our story")
def our_story():
    return render_template("our_story.html", title="our_story")

#display form page
@app.route("/customer_purchase", methods=['GET'])
def customer_purchase():
    recipes = select_database('SELECT * FROM Recipe ORDER BY \
recipe_name ASC;', 1)
    return render_template("costumer_purchase.html", recipes=recipes)

#get information from form
@app.route("/customer_purchase", methods=['GET','POST'])
def submit():
    status = check_stock()
    print(status)
    if status is True:
        name = request.form['name']
        phone = request.form['phone']
        qty = request.form.getlist('order')
        qty = [int(y) for y in qty]
        insert_database('INSERT INTO Orders(order_name, phone_no) \
    VALUES (?,?)', name, phone)
        token = select_database('SELECT order_id FROM Orders ORDER BY \
    order_id DESC LIMIT 1', 2)
        
        order = select_database('SELECT recipe_id FROM Recipe ORDER BY \
    recipe_name ASC;', 1)
        x = 0 
        for i in qty:
            if i > 0:
                insert_database('INSERT INTO Recipe_Order(recipe_id, order_id, qty) \
    VALUES (?,?,?)', order[x][0], token[0], i)
            else:
                pass
            x=x+1    
        adjust_stock(token)
        
        return redirect(url_for('success'))
    else:
        return("Sorry we do not have enough stock to process your order, press back to go to homepage")


 

@app.route("/success", methods=['GET'])
def success():
    token = select_database('SELECT order_id FROM Orders ORDER BY \
order_id DESC LIMIT 1', 2)
    token = str(token[0])
    token = int(token)
    price = get_price(token)
    return (f"Your order is successful, your order token is {token}. Your order costs ${price}")





if __name__ == "__main__":
    app.run(debug=True)