from flask import Flask, request, jsonify
from auth.login import authenticate, users
from auth.risk import calculate_risk
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/')
def home():
    return jsonify({"status": "Adaptive MFA Engine Running"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    ip_address = data.get("ip_address", "unknown_ip")
    device = data.get("device", "unknown_device")

    # Get current hour for risk calculation
    login_hour = datetime.datetime.now().hour

    # Count failed attempts
    user = users.get(username)
    failed_attempts = user.get("failed_attempts", 0) if user else 0

    # Authenticate password first
    if not authenticate(username, password):
        if user:
            user["failed_attempts"] = failed_attempts + 1
        return jsonify({"message": "Invalid credentials"}), 401

    # Reset failed attempts on successful login
    if user:
        user["failed_attempts"] = 0

    # Calculate risk score
    risk_score = calculate_risk(username, ip_address, device, login_hour, failed_attempts)

    # Decide if MFA is required
    if risk_score >= 4:
        return jsonify({"message": "MFA required", "risk_score": risk_score}), 200
    else:
        return jsonify({"message": "Login successful", "risk_score": risk_score}), 200

if __name__ == "__main__":
    app.run(debug=True)
from auth.mfa import verify_totp

# After risk_score >= 4
if risk_score >= 4 and user.get("mfa_enabled"):
    token = data.get("totp_token")
    if not token or not verify_totp(user["totp_secret"], token):
        return jsonify({"message": "MFA required or invalid token", "risk_score": risk_score}), 403
