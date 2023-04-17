from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Connect to the MongoDB instance running on localhost
client = MongoClient("mongodb://localhost:27017/")
# Select the "test" database
db = client["test"]
# Select the "messages" collection
collection = db["messages"]

# Define a route for the root URL
@app.route("/")
def hello():
    # Define a message to store in MongoDB
    message = {"text": "Hello, World!"}
    # Insert the message into the MongoDB collection
    collection.insert_one(message)
    # Return a string indicating that the message was stored in MongoDB
    return "Message stored in MongoDB."

# Run the Flask app if this script is executed directly
if __name__ == "__main__":
    app.run()
