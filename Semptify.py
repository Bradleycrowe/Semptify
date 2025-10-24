# filepath: d:\Semptify\Semptify\Semptify.py
import os, json, time, uuid
from flask import Flask, render_template
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")

# register blueprints if present
try:
    from admin.routes import admin_bp
    app.register_blueprint(admin_bp)
except Exception:
    pass
for m in ("register","metrics","readyz","vault"):
    try:
        mod = __import__(m)
        app.register_blueprint(getattr(mod, m + "_bp"))
    except Exception:
        pass

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return {"status":"ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

