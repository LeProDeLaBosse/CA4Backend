from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to the MongoDB instance running on localhost and select the "todo" database
client = MongoClient('localhost', 27017)
db = client['todo']

# Define a route for the root URL
@app.route('/')
def index():
    # Retrieve all the documents from the "todos" collection
    todos = db.todos.find()
    # Render the "index.html" template with the todos as context
    return render_template('index.html', todos=todos)

# Define a route for adding a new todo
@app.route('/add', methods=['POST'])
def add():
    # Retrieve the new todo item from the request form
    todo_item = request.form['todo']
    # Insert the new todo item into the "todos" collection with a default "complete" value of False
    db.todos.insert_one({'text': todo_item, 'complete': False})
    # Redirect the user back to the root URL
    return redirect(url_for('index'))

# Define a route for marking a todo as complete
@app.route('/complete/<ObjectId:todo_id>')
def complete(todo_id):
    # Find the todo with the given ID in the "todos" collection
    todo = db.todos.find_one({'_id': todo_id})
    # Set the "complete" value of the todo to True
    todo['complete'] = True
    # Save the updated todo in the "todos" collection
    db.todos.save(todo)
    # Redirect the user back to the root URL
    return redirect(url_for('index'))

@app.route('/toggle_important/<ObjectId:todo_id>', methods=['POST'])
def toggle_important(todo_id):
    todo = db.todos.find_one({'_id': todo_id})
    todo['important'] = not todo.get('important', False)
    db.todos.save(todo)
    return redirect(url_for('index'))

@app.route('/delete/<ObjectId:todo_id>', methods=['POST'])
def delete(todo_id):
    db.todos.delete_one({'_id': todo_id})
    return redirect(url_for('index'))


# Run the Flask app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
