from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

tasks = []

# {
#     'content' : 'abc',
#     'done' : False
# }

@app.route("/")
def main():
    return render_template('index.html', todo=tasks)

@app.route("/add", methods=['POST'])
def add():
    todo = request.form['task']
    if todo: 
        tasks.append({'content':todo, 'done':False})
        flash('Task added successfully!', 'success')
    else:
        flash('Task content cannot be empty!', 'danger')
    print(tasks)
    return redirect(url_for('main'))

@app.route('/task_finished/<int:task_id>', methods=['POST'])
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = not tasks[task_id]['done']
        flash(f"Task '{tasks[task_id]['content']}' status updated!", 'success')
    else:
        flash('Invalid task ID!', 'danger')
    return redirect(url_for('main'))


@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    
    if 0 <= task_id < len(tasks):
        new = request.get_json()
        new_content = new.get('content', '').strip()
        
        if new_content:
            tasks[task_id]['content'] = new_content
            return jsonify({'success': True, 'message': 'Task updated successfully!', 'new_content': new_content})
        else:
            return jsonify({'success': False, 'message': 'Task content cannot be empty!'}), 400
    else:
        return jsonify({'success': False, 'message': 'Task not found!'}), 404

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if 0 <= task_id < len(tasks):
        deleted_task = tasks.pop(task_id)
        print(tasks)
        flash(f"Task '{deleted_task['content']}' deleted successfully!", 'success')
    else:
        flash('Invalid task ID!', 'danger')
        
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)