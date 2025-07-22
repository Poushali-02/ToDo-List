from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

task = []

@app.route("/")
def main():
    return render_template('index.html', todo=task)

@app.route("/add", methods=['POST'])
def add():
    todo = request.form['task']
    if todo: 
        task.append(todo)
        flash('Task added successfully!', 'success')
    else:
        flash('Task content cannot be empty!', 'danger')
    print(task)
    return redirect(url_for('main'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(task):
        deleted_task = task.pop(task_id)
        print(task)
        flash(f"Task '{deleted_task}' deleted successfully!", 'success')
    else:
        flash('Invalid task ID!', 'danger')
        
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)