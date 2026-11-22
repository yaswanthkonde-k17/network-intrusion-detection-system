import sqlite3
from datetime import datetime, timedelta

DB_NAME = "alerts.db"

def check_failed_logins(threshold=3, minutes=5):
    """
    Detects brute-force attacks: Checks if an IP has multiple failed logins 
    ('/login-submit' with access denied / POST requests) within a recent timeframe.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Calculate time window (e.g., last 5 minutes)
    time_window = (datetime.now() - timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
    
    # Query recent login-submit requests
    cursor.execute('''
        SELECT client_ip, COUNT(*) as fail_count
        FROM web_logs
        WHERE endpoint = '/login-submit' AND timestamp >= ?
        GROUP BY client_ip
        HAVING fail_count >= ?
    ''', (time_window, threshold))
    
    suspicious_ips = cursor.fetchall()
    
    alerts_generated = 0
    for ip, count in suspicious_ips:
        # Check if we already logged this recently to avoid duplicate alert spam
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save a security alert into the main alerts table
        cursor.execute('''
            INSERT INTO alerts (timestamp, src_port, dst_port, packet_size, confidence, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, 0, 80, count * 100, 0.95, f"Brute-Force Suspect ({count} failed attempts from {ip})"))
        
        alerts_generated += 1
        
    conn.commit()
    conn.close()
    return alerts_generated