import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Path to the JSON file where tasks will be stored
TASKS_FILE = 'tasks.json'

# Load tasks from the JSON file
def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)  # Load data from the file
    except FileNotFoundError:
        return []  # If file doesn't exist, return an empty list

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)  # Save the updated task list to the file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST', 'DELETE'])
def handle_tasks():
    tasks = load_tasks()  # Load current tasks from the JSON file

    if request.method == 'GET':
        return jsonify(tasks)  # Return all tasks in JSON format

    if request.method == 'POST':
        task = request.json.get('task')  # Get the task from the request
        if task:
            tasks.append(task)  # Add new task to the list
            save_tasks(tasks)  # Save the updated list to the JSON file
            return jsonify({"message": "Task added successfully"}), 201
        return jsonify({"message": "Task is required"}), 400

    if request.method == 'DELETE':
        task = request.json.get('task')  # Get the task to delete from the request
        if task in tasks:
            tasks.remove(task)  # Remove the task from the list
            save_tasks(tasks)  # Save the updated list to the JSON file
            return jsonify({"message": "Task deleted successfully"}), 200
        return jsonify({"message": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
