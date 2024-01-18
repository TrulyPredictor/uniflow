
from flask import Flask, request, jsonify
from celery import Celery
from expand_reduce_flow_module import ExpandReduceFlow
import sqlite3
from typing import Sequence

app = Flask(__name__)
celery = Celery(__name__)

# Configure Celery to use a broker (e.g., Redis)
celery.conf.broker_url = 'redis://localhost:6379/0'

# SQLite database initialization
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS output_data (key TEXT, value TEXT)")
connection.commit()

@celery.task(bind=True)
def run_expand_reduce_flow(self, job_id, nodes):
    try:
        flow = ExpandReduceFlow(database_path=f"{job_id}.db")
        result_nodes = flow(nodes)
        # Store additional job information or results in the database
        for node in result_nodes:
            for key, value in node.value_dict.items():
                cursor.execute("INSERT INTO output_data VALUES (?, ?)", (key, value))
        connection.commit()
        return {'status': 'completed'}
    except Exception as e:
        return {'status': 'failed', 'error': str(e)}

@app.route('/async_run_expand_reduce_flow', methods=['POST'])
def async_run_expand_reduce_flow():
    job_id = generate_unique_job_id()  # Implement your logic to generate a unique job ID
    nodes = request.json['nodes']
    
    # Run the task asynchronously
    task = run_expand_reduce_flow.apply_async(args=[job_id, nodes])

    return jsonify({'job_id': job_id, 'status': 'pending'}), 202

@app.route('/check_status/<job_id>', methods=['GET'])
def check_status(job_id):
    task = run_expand_reduce_flow.AsyncResult(job_id)
    if task.state == 'PENDING':
        response = {'status': 'pending'}
    elif task.state == 'SUCCESS':
        response = {'status': 'completed'}
    else:
        response = {'status': 'failed', 'error': str(task.result)}

    return jsonify(response)

@app.route('/get_all_key_value_pairs', methods=['GET'])
def get_all_key_value_pairs():
    cursor.execute("SELECT * FROM output_data")
    key_value_pairs = cursor.fetchall()

    return jsonify({'key_value_pairs': key_value_pairs})

if __name__ == '__main__':
    app.run(debug=True)
