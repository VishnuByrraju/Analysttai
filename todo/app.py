from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = MongoClient("Your_mongodb_link")
db = client["todolist"]
users_collection = db["users"]
tasks_collection = db["tasks"]

@app.route('/')
def index():
    if 'username' in session:
        user_tasks = tasks_collection.find({"user_id": session['user_id']})
        return render_template('create_task.html', tasks=user_tasks)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not users_collection.find_one({"username": username}):
            user_id = users_collection.insert_one({"username": username, "password": password}).inserted_id
            session['username'] = username
            session['user_id'] = str(user_id)
            return redirect(url_for('index'))
        else:
            return "Username already exists!"
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            session['username'] = username
            session['user_id'] = str(user["_id"])
            return redirect(url_for('index'))
        else:
            return "Invalid username or password!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_task():
    if 'username' in session:
        task = request.form['task']
        tasks_collection.insert_one({"task": task, "user_id": session['user_id']})
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/delete/<string:task_id>')
def delete_task(task_id):
    if 'username' in session:
        tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/view_tasks')
def view_tasks():
    if 'username' in session:
        user_tasks = tasks_collection.find({"user_id": session['user_id']})
        return render_template('view_tasks.html', tasks=user_tasks)
    return redirect(url_for('login'))

@app.route('/create_task')
def create_task():
    if 'username' in session:
        return render_template('create_task.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
