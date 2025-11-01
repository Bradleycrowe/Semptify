# filepath: d:\Semptify\Semptify\security.py
import os, json, time, uuid, hashlib, secrets
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
_metrics = {"requests_total":0,"admin_requests_total":0,"releases_total":0,"rate_limited_total":0, "breakglass_used_total": 0}
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
        stored = e.get("hash") or ""
        # Support stored hash formats like 'sha256:<hex>' or raw hex
        if stored.startswith("sha256:"):
            stored_hex = stored.split(':', 1)[1]
        else:
            stored_hex = stored
        if hashlib.sha256(t.encode()).hexdigest() == stored_hex:
            incr_metric("admin_requests_total")
            # If this token entry is marked as breakglass and the breakglass flag exists, count its use
            if e.get('breakglass') and os.path.exists(os.path.join('security', 'breakglass.flag')):
                incr_metric('breakglass_used_total')
                try:
                    os.remove(os.path.join('security', 'breakglass.flag'))
                except Exception:
                    pass
            return True
    legacy = os.getenv("ADMIN_TOKEN")
    if legacy and t == legacy:
        incr_metric("admin_requests_total")
        return True
    abort(401)

# basic user token save
def save_user_token(plain=None):
    # Generate a secure random token if not provided
    if not plain:
        # URL-safe, reasonably short token for user convenience
        plain = secrets.token_urlsafe(8)

    h = hashlib.sha256(plain.encode()).hexdigest()
    data = _load_json(USERS_FILE)

    # Normalize existing storage: support either dict (legacy) or list (preferred)
    if isinstance(data, dict):
        # Convert dict keyed by plaintext token to list of entries
        new_list = []
        for k, v in data.items():
            entry = {
                'id': k if isinstance(k, str) else uuid.uuid4().hex[:6],
                'name': v.get('name', f'User {k}'),
                'hash': v.get('hash') or v.get('h') or hashlib.sha256(k.encode()).hexdigest(),
                'enabled': True,
                'created': v.get('created', int(time.time()))
            }
            new_list.append(entry)
        data = new_list

    if not isinstance(data, list):
        data = []

    # Create a user id and append an entry
    user_id = 'u' + uuid.uuid4().hex[:6]
    entry = {
        'id': user_id,
        'name': f'User {user_id}',
        'hash': h,
        'enabled': True,
        'created': int(time.time())
    }
    data.append(entry)

    os.makedirs(os.path.dirname(USERS_FILE) or '.', exist_ok=True)
    open(USERS_FILE, "w", encoding="utf-8").write(json.dumps(data, indent=2))
    return user_id, plain

