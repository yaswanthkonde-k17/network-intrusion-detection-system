import sqlite3
from datetime import datetime

DB_NAME = "alerts.db"

def init_db():
    """Initializes the SQLite database and creates necessary tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for security intrusion alerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            packet_size INTEGER,
            confidence REAL,
            status TEXT
        )
    ''')
    
    # Table for website request logs and security monitoring
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS web_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            client_ip TEXT,
            method TEXT,
            endpoint TEXT,
            status_code INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def save_alert(src_port, dst_port, packet_size, confidence, status):
    """Saves a new security alert into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO alerts (timestamp, src_port, dst_port, packet_size, confidence, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, src_port, dst_port, packet_size, confidence, status))
    conn.commit()
    conn.close()

def get_all_alerts():
    """Retrieves all stored alerts from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def log_web_request(client_ip, method, endpoint, status_code):
    """Saves an incoming website request log."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO web_logs (timestamp, client_ip, method, endpoint, status_code)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, client_ip, method, endpoint, status_code))
    conn.commit()
    conn.close()

def get_web_logs():
    """Retrieves all website access logs."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM web_logs ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return rows