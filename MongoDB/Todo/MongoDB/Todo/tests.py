from app import app
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client['test-db']

def test_complete():
    # Add a sample todo to the database
    db.todos.insert_one({'text': 'Sample todo', 'complete': False})
    todo_id = db.todos.find_one()['_id']

    # Simulate a request to mark the sample todo as complete
    with app.test_client() as client:
        response = client.get(f'/complete/{todo_id}')

    # Check that the response redirects to the root URL
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'

    # Check that the sample todo is now marked as complete in the database
    todo = db.todos.find_one({'_id': ObjectId(todo_id)})
    assert todo['complete'] == True
