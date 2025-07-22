from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, g
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

load_dotenv()
def __init__db():
    conn = sqlite3.connect('todo_users.db')
    cursor = conn.cursor()
    # the database initialised
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )"""
    )
    conn.commit()

__init__db()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('todo_users.db')
        db.row_factory = sqlite3.Row 
    return db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# main route
@app.route("/")
def main():
    if 'user_id' in session:
        db = get_db()
        user_id = session['user_id']
        tasks=db.execute("""
                   SELECT * FROM tasks WHERE user_id = ?
                   """,(user_id,)).fetchall()
        return render_template('dashboard.html', todo=tasks)
    return render_template('index.html')

# add route
@app.route("/add", methods=['POST'])
def add():
    if 'user_id' not in session:
        flash('You must be logged in to add tasks!', 'danger')
        return redirect(url_for('login'))
    todo = request.form['task']
    if todo:
        db = get_db()
        user_id = session['user_id']
        db.execute("""
                   INSERT INTO tasks (user_id, content) VALUES (?, ?)
                   """, (user_id, todo))
        db.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Task content cannot be empty!', 'danger')
    return redirect(url_for('main'))

# finished toggle route
@app.route('/task_finished/<int:task_id>', methods=['POST'])
def toggle(task_id):
    if 'user_id' not in session:
        flash('You must be logged in to toggle task status!', 'danger')
        return redirect(url_for('login'))
    db = get_db()
    user_id = session['user_id']
    
    task = db.execute(
        """SELECT done FROM tasks WHERE user_id = ? AND id = ?""", (user_id, task_id)
    ).fetchone()
    
    if task:
        new_status = 0 if task['done'] else 1
        db.execute('''UPDATE tasks SET done = ? WHERE user_id = ? AND id = ?''',
                   (new_status, user_id, task_id))
        db.commit()
        flash('Task status updated successfully!', 'success')
    else:
        flash('Task not found!', 'danger')
    return redirect(url_for('main'))

# edit route
@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    if 'user_id' not in session:
        flash('You must be logged in to edit tasks!', 'danger')
        return redirect(url_for('login'))
    new = request.get_json()
    new_content = new.get('content', '').strip()
    if new_content:
        db = get_db()
        user_id = session['user_id']
        db.execute('''UPDATE tasks SET content = ? WHERE user_id = ? AND id = ?''',
                   (new_content, user_id, task_id))
        db.commit()
        return jsonify({'success': True, 'message': 'Task updated successfully!', 'new_content': new_content})
    else:
        return jsonify({'success': False, 'message': 'Task content cannot be empty!'}), 400

# delete route
@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 'user_id' not in session:
        flash('You must be logged in to delete tasks!', 'danger')
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute(
        """DELETE FROM tasks WHERE user_id = ? AND id = ?""",
        (session['user_id'], task_id)
    )
    db.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main'))

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('signup'))
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        try:
            cursor = db.cursor()
            cursor.execute("""
                           INSERT INTO users  (username, email, password) VALUES (?, ?, ?)
                           """, (username, email, generate_password_hash(password))
            )
            user_id = cursor.lastrowid
            db.commit()
            session['user_id'] = user_id
            session['username'] = username
            session['email'] = email
            session['password'] = password
            flash('Sign up successful!', 'success')
            return redirect(url_for('main'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('signup'))
    return render_template('signup.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            """SELECT * FROM users WHERE username = ?""", (username,)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)