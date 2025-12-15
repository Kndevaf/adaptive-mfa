# auth/risk.py

def calculate_risk(username: str, ip_address: str, device: str, login_hour: int, failed_attempts: int) -> int:
    """
    Simple risk scoring example:
    - New IP: +2
    - New device: +2
    - Login at unusual hour: +1
    - Multiple failed attempts: +3
    Returns a risk score (0-8)
    """
    score = 0

    if ip_address != "known_ip":
        score += 2
    if device != "known_device":
        score += 2
    if login_hour < 6 or login_hour > 22:
        score += 1
    if failed_attempts > 2:
        score += 3

    return score
