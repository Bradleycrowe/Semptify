# filepath: d:\Semptify\Semptify\security.py
import os, json, time, uuid, hashlib
from flask import session, request, abort, make_response

ADMIN_FILE = os.path.join("security","admin_tokens.json")
USERS_FILE = os.path.join("security","users.json")

def _load_json(p):
    try:
        if os.path.exists(p):
            return json.load(open(p,"r",encoding="utf-8"))
    except:
        pass
    return {}

# metrics
_metrics = {"requests_total":0,"admin_requests_total":0,"releases_total":0,"rate_limited_total":0}
def incr_metric(name, amount=1):
    _metrics[name] = _metrics.get(name,0) + int(amount)
def get_metrics():
    return _metrics

# CSRF
def _get_or_create_csrf_token():
    if "csrf" not in session:
        session["csrf"] = uuid.uuid4().hex
    return session["csrf"]

# admin auth simple
def _require_admin_or_401():
    t = request.headers.get("X-Admin-Token") or request.args.get("admin_token")
    if not t and os.getenv("SECURITY_MODE","open") == "open":
        return True
    if not t:
        abort(401)

    # Rate limiting logic
    rate_window = int(os.getenv("ADMIN_RATE_WINDOW", 60))
    rate_max = int(os.getenv("ADMIN_RATE_MAX", 10))
    client_ip = request.remote_addr
    now = time.time()

    # Load rate limit data
    rate_limit_data = _load_json("logs/rate_limit.json")
    client_data = rate_limit_data.get(client_ip, {"timestamps": []})

    # Filter timestamps within the rate window
    client_data["timestamps"] = [ts for ts in client_data["timestamps"] if now - ts <= rate_window]

    if len(client_data["timestamps"]) >= rate_max:
        abort(429)  # Too Many Requests

    # Add current timestamp and save data
    client_data["timestamps"].append(now)
    rate_limit_data[client_ip] = client_data
    open("logs/rate_limit.json", "w", encoding="utf-8").write(json.dumps(rate_limit_data, indent=2))

    entries = _load_json(ADMIN_FILE).get("tokens", [])
    for e in entries:
        if hashlib.sha256(t.encode()).hexdigest() == e.get("hash"):
            incr_metric("admin_requests_total")
            return True
    legacy = os.getenv("ADMIN_TOKEN")
    if legacy and t == legacy:
        incr_metric("admin_requests_total")
        return True
    abort(401)

# basic user token save
def save_user_token(plain=None):
    if not plain:
        plain = str(int(time.time()))[-6:]
    h = hashlib.sha256(plain.encode()).hexdigest()
    data = _load_json(USERS_FILE)
    data[plain] = {"hash":h,"created":int(time.time())}
    open(USERS_FILE,"w",encoding="utf-8").write(json.dumps(data,indent=2))
    return plain

