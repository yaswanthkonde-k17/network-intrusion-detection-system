from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from backend.database import init_db, save_alert, get_all_alerts, log_web_request, get_web_logs
from src.web_detector import check_failed_logins

app = FastAPI(title="Network Intrusion Detection & Website Monitoring API", version="1.0")

# Initialize database on startup
init_db()

# Load model and scaler safely
MODEL_PATH = "models/model.pkl"
SCALER_PATH = "models/scaler.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
else:
    model = None
    scaler = None

class TrafficInput(BaseModel):
    duration: float
    protocol: int
    src_port: int
    dst_port: int
    packet_size: int
    flow_Bytes_s: float

# --- MONITORING MIDDLEWARE ---
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    """Intercepts website requests to log traffic activity safely."""
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    endpoint = request.url.path
    
    response = await call_next(request)
    
    # Log non-API page requests
    if not endpoint.startswith("/docs") and not endpoint.startswith("/openapi.json"):
        log_web_request(client_ip, method, endpoint, response.status_code)
        
    return response

# --- EXISTING NETWORK IDS ENDPOINTS ---

@app.get("/api-status")
def home():
    return {"message": "Network Intrusion Detection API is running with Database Integration!"}

@app.post("/predict")
def predict_traffic(data: TrafficInput):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or scaler not found.")
    
    input_data = pd.DataFrame([{
        'duration': data.duration,
        'protocol': data.protocol,
        'src_port': data.src_port,
        'dst_port': data.dst_port,
        'packet_size': data.packet_size,
        'flow_Bytes_s': data.flow_Bytes_s
    }])
    
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0].max()
    
    result = "Attack" if prediction == 1 else "Normal"
    status = "Suspicious" if result == "Attack" else "Safe"
    
    if result == "Attack":
        save_alert(
            src_port=data.src_port,
            dst_port=data.dst_port,
            packet_size=data.packet_size,
            confidence=float(probability),
            status=status
        )
    
    return {
        "prediction": result,
        "confidence": float(probability),
        "status": status
    }

@app.get("/alerts")
def get_alerts():
    """Endpoint to fetch all logged attack alerts."""
    alerts = get_all_alerts()
    return {"total_alerts": len(alerts), "alerts": alerts}

@app.get("/web-logs-api")
def get_web_logs_api():
    """Endpoint to fetch recent website traffic logs."""
    logs = get_web_logs()
    return {"total_logs": len(logs), "logs": logs}

# --- STYLISH TEST WEBSITE ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
def website_home():
    return """
    <html>
        <head>
            <title>Secure Portal - Home</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .card { background: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center; width: 400px; border: 1px solid #334155; }
                h1 { color: #38bdf8; margin-bottom: 10px; font-size: 24px; }
                p { color: #94a3b8; font-size: 14px; margin-bottom: 30px; }
                .btn { display: inline-block; padding: 12px 24px; background: #0284c7; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; }
                .btn:hover { background: #0369a1; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🛡️ Secure Portal</h1>
                <p>Monitored test environment connected to real-time intrusion detection.</p>
                <a href="/login-page" class="btn">Proceed to Login</a>
            </div>
        </body>
    </html>
    """

@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return """
    <html>
        <head>
            <title>Secure Portal - Login</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .card { background: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 350px; border: 1px solid #334155; }
                h2 { color: #38bdf8; margin-top: 0; text-align: center; }
                label { font-size: 13px; color: #94a3b8; display: block; margin-bottom: 5px; }
                input { width: 100%; padding: 10px; margin-bottom: 20px; background: #0f172a; border: 1px solid #475569; border-radius: 6px; color: white; box-sizing: border-box; }
                .btn { width: 100%; padding: 10px; background: #10b981; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }
                .btn:hover { background: #059669; }
                .back { display: block; text-align: center; margin-top: 15px; color: #94a3b8; text-decoration: none; font-size: 13px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h2>Portal Login</h2>
                <form action="/login-submit" method="post">
                    <label>Username</label>
                    <input type="text" name="username" placeholder="Enter username" required>
                    <label>Password</label>
                    <input type="password" name="password" placeholder="Enter password" required>
                    <button type="submit" class="btn">Sign In</button>
                </form>
                <a href="/" class="back">← Back to Home</a>
            </div>
        </body>
    </html>
    """

@app.post("/login-submit", response_class=HTMLResponse)
def login_submit(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret123":
        return """
        <html>
            <head><style>body { font-family: 'Segoe UI'; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }.card { background: #1e293b; padding: 40px; border-radius: 12px; text-align: center; border: 1px solid #334155; width: 350px; }h2 { color: #10b981; }a { color: #38bdf8; text-decoration: none; display: inline-block; margin-top: 20px; }</style></head>
            <body><div class="card"><h2>✅ Access Granted</h2><p>Welcome back, admin.</p><a href="/login-page">Sign Out</a></div></body>
        </html>
        """
    else:
        # Trigger brute-force check on failed login
        check_failed_logins(threshold=3, minutes=5)
        
        return """
        <html>
            <head><style>body { font-family: 'Segoe UI'; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }.card { background: #1e293b; padding: 40px; border-radius: 12px; text-align: center; border: 1px solid #334155; width: 350px; }h2 { color: #ef4444; }a { color: #38bdf8; text-decoration: none; display: inline-block; margin-top: 20px; }</style></head>
            <body><div class="card"><h2>❌ Access Denied</h2><p>Invalid credentials provided.</p><a href="/login-page">Try Again</a></div></body>
        </html>
        """