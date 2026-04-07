"""
ÁREA: Desarrollo de Aplicaciones Web
DESCRIPCIÓN: Aplicación web para la gestión de tareas y áreas de conocimiento
TECNOLOGÍA: Flask, Celery, Tailwind CSS
"""

from flask import Flask, render_template, request, jsonify
import os
import json

# Import RootAssistant and SessionManager
from root_assistant import RootAssistant
from database import SessionManager

# Import Celery app to query task statuses
from celery_app import celery_app

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

app = Flask(__name__)

# Initialize the RootAssistant to use asynchronous task submission by default.
assistant = RootAssistant(enable_async=True)

# Global session manager for conversation tracking
session_manager = SessionManager()

# Lista de tareas en ejecución
tareas_en_ejecucion = []

@app.route('/')
def index():
    try:
        # Ahora renderizamos el HTML que acabamos de crear
        return render_template('index.html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def handle_query():
    try:
        user_query = request.json.get('query')
        # Allow passing session_id for continuous conversations
        session_id = request.json.get('session_id')
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        response_content, new_session_id = assistant.process_query(user_query, session_id)
        return jsonify({
            "query": user_query,
            "response": response_content,
            "session_id": new_session_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit_task', methods=['POST'])
def submit_task():
    try:
        task_description = request.form.get('description')
        context_str = request.form.get('context', '{}')

        if not task_description:
            return jsonify({"status": "error", "message": "Task description is required"}), 400

        try:
            context = json.loads(context_str)
        except json.JSONDecodeError:
            context = {}  # Default to an empty dict if the context JSON is invalid.

        # Submit the task using the RootAssistant, which delegates to Celery.
        response = assistant.submit_automation_request(task_description, context)

        if response['status'] == 'submitted':
            # Task successfully submitted to Celery, return 202 Accepted.
            tareas_en_ejecucion.append(response['task_id'])
            return jsonify({"status": "success", "message": "Task submitted successfully.", "task_id": response['task_id']}), 202
        elif response['status'] == 'completed_sync':
            # Task was processed synchronously (async disabled), return 200 OK.
            return jsonify({"status": "warning", "message": "Task processed synchronously (async disabled).", "result": response['result']}), 200
        else:
            # Handle other potential errors during submission.
            return jsonify({"status": "error", "message": response.get('error', 'Unknown error during task submission.')}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/task_status/<task_id>')
def task_status(task_id):
    try:
        task = celery_app.AsyncResult(task_id)
        response_data = {
            'task_id': task.id,
            'state': task.state,  # Current state (e.g., PENDING, STARTED, PROGRESS, SUCCESS, FAILURE)
            'info': {}            # Contains task-specific information (e.g., progress, result, error)
        }

        if task.state == 'PENDING':
            response_data['info'] = {'status': 'Task is pending or unknown.'}
        elif task.state == 'FAILURE':
            response_data['info'] = {'status': str(task.info), 'traceback': task.traceback}
        else:  # States like STARTED, PROGRESS, SUCCESS
            response_data['info'] = task.info or {}  # Custom info from task.update_state() or the final result

        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/panic', methods=['POST'])
def panic():
    try:
        global tareas_en_ejecucion
        for task_id in tareas_en_ejecucion[:]:  # Iterar sobre una copia para evitar problemas de concurrencia
            task = celery_app.AsyncResult(task_id)
            task.revoke(terminate=True)
        tareas_en_ejecucion = []
        return jsonify({"status": "success", "message": "Todas las tareas han sido detenidas."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/areas')
def areas():
    try:
        areas = [
            {'name': 'Finanzas', 'color': 'bg-green-500', 'description': 'Área de finanzas'},
            {'name': 'Real Estate', 'color': 'bg-blue-500', 'description': 'Área de bienes raíces'},
            {'name': 'Cerebro', 'color': 'bg-purple-500', 'description': 'Área de conocimiento'}
        ]
        return render_template('areas.html', areas=areas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/boton_panic')
def boton_panic():
    try:
        return render_template('boton_panic.html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)