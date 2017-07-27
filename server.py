from flask import Flask, render_template, request, redirect
#mysql import
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'products_demo')

@app.route('/')
def products():
    # gather up products from database
    query = "SELECT * FROM products"
    products = mysql.query_db(query)
    print products
    # display them
    # render template
    return render_template('products.html', all_products=products)

@app.route('/products', methods=["POST"])
def create_product():
    # take form info and save into database
    query = "INSERT INTO products (title, description, qty, price, created_at, updated_at) VALUES (:title, :desc, :qty, :price, NOW(), NOW())"
    data = {
        'title': request.form['title'],
        'desc': request.form['description'],
        'qty': request.form['qty'],
        'price': request.form['price']
    }
    mysql.query_db(query, data)

    return redirect('/')

app.run(debug=True)