"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Manejo de sesiones y mensajes para una agencia de IA
TECNOLOGÍA: Python, SQLite
"""

import sqlite3
import os
from datetime import datetime
import time
import sys

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class SessionManager:
    def __init__(self, db_name='agency_data.db'):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS sessions
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               start_time TEXT,
                               status TEXT,
                               description TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               session_id INTEGER,
                               sender TEXT,
                               content TEXT,
                               timestamp TEXT,
                               FOREIGN KEY(session_id) REFERENCES sessions(id))''')
            conn.commit()

    def create_session(self, description="Nueva Tarea de Automatización"):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO sessions (start_time, status, description) VALUES (?, ?, ?)",
                           (now, "Iniciada", description))
            session_id = cursor.lastrowid
            conn.commit()
            time.sleep(2)
            return session_id

    def add_message(self, session_id, sender, content):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO messages (session_id, sender, content, timestamp) VALUES (?, ?, ?, ?)",
                           (session_id, sender, content, now))
            conn.commit()
            time.sleep(2)

    def get_all_sessions(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, start_time, status, description FROM sessions ORDER BY id DESC")
            return cursor.fetchall()

    def get_session_messages(self, s_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, sender, content FROM messages WHERE session_id=?", (s_id,))
            return cursor.fetchall()

def main():
    if len(sys.argv) > 1:
        monto = float(sys.argv[1])
        tasa = float(sys.argv[2])
        plazo = int(sys.argv[3])
    else:
        monto = 2000000
        tasa = 9.5
        plazo = 20
        print(f"Usando valores por defecto: monto={monto}, tasa={tasa}, plazo={plazo}")

    manager = SessionManager()
    session_id = manager.create_session(f"Prueba de Sesión con monto {monto}, tasa {tasa} y plazo {plazo}")
    manager.add_message(session_id, "IA", f"Mensaje de prueba con monto {monto}, tasa {tasa} y plazo {plazo}")
    sessions = manager.get_all_sessions()
    for session in sessions:
        print(f"Sesión {session[0]} - {session[1]} - {session[2]} - {session[3]}")
        messages = manager.get_session_messages(session[0])
        for message in messages:
            print(f"  {message[0]} - {message[1]} - {message[2]}")

if __name__ == "__main__":
    with open(__file__, 'r', encoding='utf-8') as file:
        pass
    main()