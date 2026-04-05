from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE = "tasks.json"

# Load tasks
def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

# Save tasks
def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f)

@app.route('/')
def home():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get('task')
    tasks = load_tasks()

    if task_text:
        tasks.append({"task": task_text, "status": 0})
        save_tasks(tasks)

    return redirect('/')

@app.route('/toggle/<int:id>')
def toggle(id):
    tasks = load_tasks()
    tasks[id]["status"] = 1 - tasks[id]["status"]
    save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    tasks = load_tasks()
    tasks.pop(id)
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run()