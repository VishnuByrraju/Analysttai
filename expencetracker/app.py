from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'my_key'

# MongoDB connection
client = MongoClient('mongodb+srv://admin:admin@cluster1.hbxmhai.mongodb.net/')
db = client['expense_tracker']

# Create collection if not exists
expenses_collection = db['expenses']
users_collection = db['users']

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        expenses = list(expenses_collection.find({'user_id': user_id}))
        return render_template('index.html', expenses=expenses)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if not user:
            user_id = users_collection.insert_one({'username': username, 'password': password}).inserted_id
            session['user_id'] = str(user_id)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' in session:
        user_id = session['user_id']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        expenses_collection.insert_one({'user_id': user_id, 'amount': amount, 'category': category, 'date': date})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
