from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:8428544485@todolist-db.c72qeeoaky6t.ap-southeast-1.rds.amazonaws.com/todolist'

# Initialize the SQLAlchemy ORM
db = SQLAlchemy(app)

# Define the Task model (represents the tasks table in the database)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Create the database tables if they don't exist
@app.before_first_request
def create_tables():
    db.create_all()

# The main route, displays the to-do list
@app.route('/')
def index():
    # Fetch all tasks from the database
    todo_list = Task.query.all()
    return render_template('index.html', todo_list=todo_list)

# Add a new task
@app.route('/add', methods=['POST'])
def add():
    # Get the content of the new task from the form
    task_content = request.form.get('content')
    new_task = Task(content=task_content)

    # Add the new task to the database
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Mark a task as complete
@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get(task_id)
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Run the Flask application on port 8000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
