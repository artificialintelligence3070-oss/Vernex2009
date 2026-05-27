from flask import Flask, request, jsonify
import requests
import secrets
import json
import os
import re
from datetime import datetime, timedelta

app = Flask(__name__)

KEYS_FILE = "keys.json"

UPSTREAM_API = "https://ft-osint-api.duckdns.org/api/number"
UPSTREAM_KEY = "YOUR_UPSTREAM_KEY"

# -------------------------
# CREATE STORAGE
# -------------------------

if not os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, "w") as f:
        json.dump({}, f)

# -------------------------
# LOAD KEYS
# -------------------------

def load_keys():
    with open(KEYS_FILE, "r") as f:
        return json.load(f)

# -------------------------
# SAVE KEYS
# -------------------------

def save_keys(data):
    with open(KEYS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# VALIDATE API KEY
# -------------------------

def validate_key(api_key):

    keys = load_keys()

    if api_key not in keys:
        return False

    expiry = datetime.fromisoformat(
        keys[api_key]["expiry"]
    )

    if datetime.utcnow() > expiry:

        del keys[api_key]
        save_keys(keys)

        return False

    return True

# -------------------------
# VALIDATE PHONE
# -------------------------

def valid_phone(number):

    return re.fullmatch(r"[0-9]{10}", number)

# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():

    return jsonify({
        "owner": "VERNEX",
        "status": "ONLINE"
    })

# -------------------------
# GENERATE KEY
# -------------------------

@app.route("/generate-key")
def generate_key():

    days = request.args.get(
        "days",
        default=1,
        type=int
    )

    api_key = "vernex-day-" + secrets.token_hex(8)

    expiry = datetime.utcnow() + timedelta(days=days)

    keys = load_keys()

    keys[api_key] = {
        "expiry": expiry.isoformat()
    }

    save_keys(keys)

    return jsonify({
        "success": True,
        "api_key": api_key,
        "expires_at": expiry.isoformat(),
        "valid_days": days
    })

# -------------------------
# NUMBER LOOKUP
# -------------------------

@app.route("/api/number")
def number_lookup():

    api_key = request.args.get("key")
    number = request.args.get("num")

    # KEY CHECK
    if not api_key:
        return jsonify({
            "success": False,
            "error": "API Key Required"
        })

    if not validate_key(api_key):
        return jsonify({
            "success": False,
            "error": "Invalid or Expired API Key"
        })

    # NUMBER CHECK
    if not number:
        return jsonify({
            "success": False,
            "error": "Phone Number Required"
        })

    if not valid_phone(number):
        return jsonify({
            "success": False,
            "error": "Invalid Phone Number"
        })

    try:

        response = requests.get(
            UPSTREAM_API,
            params={
                "key": UPSTREAM_KEY,
                "num": number
            },
            timeout=15
        )

        data = response.json()

        # REMOVE UNWANTED FIELDS
        if isinstance(data, dict):

            remove_fields = [
                "by",
                "channel",
                "cached",
                "cached_at"
            ]

            for field in remove_fields:
                data.pop(field, None)

        return jsonify({
            "success": True,
            "owner": "VERNEX",
            "searched_number": number,
            "result": data
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
