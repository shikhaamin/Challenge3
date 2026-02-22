# ...existing code...
from flask import Flask, render_template, jsonify, request
import sqlite3
from typing import Any, Dict
from logic import redistribute_tasks

app = Flask(__name__)

def get_db_connection():
    # This connects to the SQLite file you saw in DataGrip
    conn = sqlite3.connect('identifier.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Flask looks inside the /templates/ folder for this file
    return render_template('challenge3.html')

@app.route('/get_tasks')
def get_tasks():
    conn = get_db_connection()
    query = 'SELECT id, title, start_time AS start, end_time AS end FROM tasks'
    tasks = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in tasks])

@app.route('/get_employees')
def get_employees():
    conn = get_db_connection()
    rows = conn.execute('SELECT id, name FROM employees').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/get_tasks_today')
def get_tasks_today():
    conn = get_db_connection()
    query = """
      SELECT t.id, t.title, t.start_time AS start, t.end_time AS end,
             t.assigned_to, e.name AS assigned_name
      FROM tasks t
      LEFT JOIN employees e ON t.assigned_to = e.id
      WHERE date(t.start_time) = date('now','localtime') OR date(t.end_time) = date('now','localtime')
    """
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')
    assigned = data.get('assigned')

    if not title or not start or not end:
        return jsonify({'error': 'missing fields'}), 400

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO tasks (title, start_time, end_time, assigned_to) VALUES (?, ?, ?, ?)',
        (title, start, end, assigned)
    )
    conn.commit()
    conn.close()
    return jsonify({'ok': True}), 201

@app.route('/update_task', methods=['POST'])
def update_task():
    data = request.get_json()
    task_id = data.get('id')
    start = data.get('start')
    end = data.get('end')

    if not task_id:
        return jsonify({'error': 'missing task id'}), 400

    conn = get_db_connection()
    conn.execute('UPDATE tasks SET start_time = ?, end_time = ? WHERE id = ?', (start, end, task_id))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/reassign_task', methods=['POST'])
def reassign_task():
    data = request.get_json()
    task_id = data.get('taskId') or data.get('task_id') or data.get('id')
    employee_id = data.get('employeeId') or data.get('employee_id') or data.get('assigned')

    if not task_id or employee_id is None:
        return jsonify({'error': 'missing fields'}), 400

    conn = get_db_connection()
    conn.execute('UPDATE tasks SET assigned_to = ? WHERE id = ?', (employee_id, task_id))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/check_session')
def check_session():
    # placeholder: accept all sessions for now
    return jsonify({'ok': True})

@app.route('/redistribute', methods=['POST'])
def redistribute():
    try:
        result = redistribute_tasks('identifier.sqlite')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)