from flask import Flask, render_template, request, redirect, flash, session
#mysql import
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = "secret_stuff"
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'products_demo')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=["POST"])
def register():
    query = "SELECT * FROM users WHERE username = :un"
    data = {
        'un': request.form['username']
    }

    results = mysql.query_db(query,data) # [] , [{}]
    if len(results) > 0:
        flash('username already taken')
        return redirect('/')
    else: 
        if len(request.form['password']) < 8:
            flash('password not long enough')
            return redirect('/')
        else:
            enc_password = bcrypt.generate_password_hash(request.form['password'])
            query = "INSERT INTO users (username, password, created_at, updated_at) VALUES (:un, :password, NOW(), NOW())"
            data = {
                'un': request.form['username'],
                'password': enc_password
            }
            user_id = mysql.query_db(query,data)
            session['user_id'] = user_id 
            return redirect('/products')

@app.route('/products')
def products():
    # gather up products from database
    query = "SELECT * FROM products"
    products = mysql.query_db(query)
    print products
    # display them
    # render template
    return render_template('products.html', all_products=products)

@app.route('/create_products', methods=["POST"])
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