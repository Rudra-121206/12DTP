from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta


app = Flask(__name__)

# function for inserting and updating values in the database
def insert_database(*args):
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
    # if no values are to be inserted, statement runs
    if len(args) == 1:
        cur.execute(args[0])
    # a tuple is formed , the spare values are put into the tuples to be inserted into database, 
    # because safe methd of inserting values into databse is using tuples
    else:
        argument_tuple = ()
        for i in range(1, len(args)):
            argument_tuple += (args[i],)
        cur.execute(args[0], argument_tuple)
    conn.commit()
    conn.close()

# get the price of the customer's orders, to show them.
def get_price(token):
# uses the order id to get orders
    orders = select_database('SELECT recipe_id, qty FROM Recipe_Order WHERE order_id = ?', (token,), 1)
#for each order the price is checked, mutlilplied by the qty bought and value is added to price
    total_price = 0
    for order in orders: 
        price = select_database('SELECT price FROM Recipe where recipe_id = ?', (order[0],), 2) 
        price = price[0]*order[1]
        price = str(price)
        price = int(price)
        total_price = price + total_price
#total price is returned
    return total_price

# change stock according to what is bought by customers.
def adjust_stock(token):
# get recipes from token/order_id
    orders=select_database('SELECT recipe_id, qty FROM Recipe_Order WHERE order_id = ?', (token[0],), 1)
# for each recipe, check qty of each item used
    for order in orders:
        qty=order[1]
        recipe = order[0]
        results = select_database('SELECT * FROM Item_Recipe WHERE recipe_id = ?', (recipe,), 1)
        for result in results:
            #each item used should be multiplied by the amount of each recipe bought
            used_qty=result[0]
            total_used_qty=used_qty*qty          
            item_id=result[2]
            # subtrct original qty from the the qty, and new found value to database.
            original_qty=select_database('SELECT balance_qty FROM Inventory WHERE item_id = ?', item_id[0], 2)
            changed_qty=original_qty[0]-total_used_qty
            insert_database('UPDATE Inventory SET balance_qty = ? WHERE item_id = ?', changed_qty, item_id)
    return 'done'
# check that stock is enough to sell to customers, check that stock is not past expiry date, 
# if stock is then make all stock for that item 0
def check_stock():

    balance_qty=select_database('SELECT item_id, item_expiry, base_qty, balance_qty FROM Inventory', None, 1)
    status=True
    Date=(datetime.today())
    for balance in balance_qty:
        # get overall qty in the item and get balance qty in the item
        item_expiry=balance[1]
        # get expiry date and current date and make them the same format
        item_expiry=str(item_expiry)
        item_expiry = datetime.strptime(item_expiry, '%Y-%m-%d')
       #if balance qty is less the minimum qty or if any item on the menu is expired, don't allow the sale
        if balance[2]>balance[3]:
            status=False 
       # if item is expired throw out the item , so we have no stock of the item
        elif Date>(item_expiry):
            status=False
            insert_database('UPDATE Inventory SET balance_qty = 0 WHERE item_id = ?', balance[0])      
        else:
            status=status       
    return status


# Call function and arguments should be in this order:
# Statement -> OPTIONAL: arguments -> mode (1 = fetchall() and 2 = fetchone())

def select_database(statement,Parameters,mode):
    conn = sqlite3.connect('Inventory_management_system.db')
    cur = conn.cursor()
# checks if there are any values to put into the databse, if not executes the satament    
    if Parameters is None:
        cur.execute(statement)
# When there aare values its important to put them in using a tuple, so it takes each value and turns it into a tuple.
# When this has been done it executes the stament        
    else:
        argument_tuple = []
        for parameter in Parameters:            
            argument_tuple.append(parameter)

        argument_tuple = tuple(argument_tuple)
        cur.execute(statement, argument_tuple)
# depending on the mode it uses fetchall or fetchone
    if mode == 1:
        results = cur.fetchall()
    else:
        results = cur.fetchone()
    conn.close()
    return results


# direct to home page
@app.route("/")
def home():
    return render_template("home.html", title="Rudra's restaurant")


# add inventory when stocks are low so that restaurant can run, change expiry date, 
# check that existing stock doesnt have expiry date lower than today , if it does throw it all out before buying new stock
@app.route("/add_product", methods=['GET'])
def add_product():
    # gets id of item, and amt to buy from link
    added_qty= request.args.get('added_qty')
    added_qty= int(added_qty)
    item_id= request.args.get('id')
    # gets the expiry date and the qty
    result= select_database('SELECT item_expiry, balance_qty FROM Inventory WHERE item_id = ?', (item_id,), 1)
    qty= result[0][1]
    qty= int(qty)
    #gets total qty after buying stock 
    changed_qty= added_qty+qty
    # gets today's date
    current_date = datetime.today()
    item_expiry=result[0][0]
    item_expiry=str(item_expiry)
    #changes unit of today's date and expiry date to be the same
    item_expiry = datetime.strptime(item_expiry, '%Y-%m-%d')
    expiry_date = current_date + relativedelta(months=2)
    expiry_date=str(expiry_date)
    expiry_date=(expiry_date.split(" "))
    expiry_date=expiry_date[0]
    # compare current date and expiry date, if item is expired all stock is thrown out, and new 500 grams are bought, 
    # expiry date is adjusted two months from current date
    # if item isn't expired total stock replaces the "balance_qty", and 2 months from now is the expiry date
    if current_date>(item_expiry):
        insert_database('UPDATE Inventory SET item_expiry = ?, balance_qty = ? WHERE item_id = ?', expiry_date, added_qty, item_id)   
    else:
        insert_database('UPDATE Inventory SET item_expiry = ?, balance_qty = ? WHERE item_id = ?', expiry_date, changed_qty, item_id)

    return redirect(url_for("admin"))


#show all existing menu
@app.route("/menu")
def menu():
    menu = select_database('SELECT * FROM Recipe ORDER BY recipe_name ASC;', None, 1)
    return render_template("menu.html", title="menu", menu=menu)


# display admin informmation
@app.route("/admin")
def admin():
    inventory = select_database('SELECT * FROM Inventory ORDER BY \
item_name ASC;',None, 1)
    return render_template("admin.html", title="admin", inventory=inventory)


#display form page
@app.route("/customer_purchase", methods=['GET'])
def customer_purchase():
    recipes = select_database('SELECT * FROM Recipe ORDER BY \
recipe_name ASC;', None, 1)
    return render_template("costumer_purchase.html", recipes=recipes)


#get information from form, check that there is enough stock, 
# then adjust stock levels according what has been bought, redirect to success if order is successful
@app.route("/customer_purchase", methods=['GET','POST'])
def submit():
    status = check_stock()
    # git information from the form 
    if status is True:
        name = request.form['name']
        phone = request.form['phone']
        qty = request.form.getlist('order')
        qty = [int(y) for y in qty]
   #add info to the form 
        insert_database('INSERT INTO Orders(order_name, phone_no) \
    VALUES (?,?)', name, phone)
        token = select_database('SELECT order_id FROM Orders ORDER BY \
    order_id DESC LIMIT 1', None, 2)
        
        order = select_database('SELECT recipe_id FROM Recipe ORDER BY \
    recipe_name ASC;',None , 1)
        x = 0 
   # add info to joining tabe between order and recipe so based on the amt of reipes, 
   # order_id/token is added into a database with its corrosponding recipe and qty
        for i in qty:
            if i > 0:
                insert_database('INSERT INTO Recipe_Order(recipe_id, order_id, qty) \
    VALUES (?,?,?)', order[x][0], token[0], i)
            else:
                pass
            x=x+1   
    # stock is adjusted 
        adjust_stock(token)
        
        return redirect(url_for('success'))
    else:
        return("Sorry we do not have enough stock to process your order, press back to go to homepage")


 
# redirect to this url once the order is successful
@app.route("/success", methods=['GET'])
def success():
# gets the token of customer's order
    token = select_database('SELECT order_id FROM Orders ORDER BY \
order_id DESC LIMIT 1', None, 2)
    token = str(token[0])
    token = int(token)
# price function is run with the token so the price for that order can=be obtained
    price = get_price(token)
# token and price are returned
    return (f"Your order is successful, your order token is {token}. Your order costs ${price}")

#each recipe has one id, and a link for each recipe is created here
@app.route("/Recipe/<int:recipe_id>")
#shows info about the recipe
def recipe_id(recipe_id):
    print (recipe_id[0])
    recipe = select_database("SELECT recipe_id, recipe_name, description, price FROM Recipe WHERE recipe_id = ?", (recipe_id), 1)

    return render_template("recipe.html", recipe=recipe)
    
    




if __name__ == "__main__":
    app.run(debug=True)