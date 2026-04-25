import os

import requests
from flask import Flask, render_template, request, session


app = Flask(__name__)
app.secret_key = os.environ.get("CLIENT_APP_SECRET", "client-app-dev-secret")

API_URL = "http://127.0.0.1:5000"


def api_unavailable():
    return {"error": "API non disponible"}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    result = None

    if request.method == "POST":
        data = request.form["data"]

        headers = {}
        if "token" in session:
            headers["Authorization"] = f"Bearer {session['token']}"

        try:
            res = requests.post(
                f"{API_URL}/encrypt",
                json={"data": data},
                headers=headers,
            )
            result = res.json()
        except requests.RequestException:
            result = api_unavailable()

    return render_template("encrypt.html", result=result)


@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    result = None

    if request.method == "POST":
        data = request.form["data"]
        try:
            res = requests.post(f"{API_URL}/decrypt", json={"data": data})
            result = res.json()
        except requests.RequestException:
            result = api_unavailable()

    return render_template("decrypt.html", result=result)


@app.route("/keys", methods=["GET", "POST"])
def keys():
    result = None

    if request.method == "POST":
        action = request.form["action"]
        try:
            res = requests.post(f"{API_URL}/keys/{action}")
            result = res.json()
        except requests.RequestException:
            result = api_unavailable()

    return render_template("keys.html", result=result)


@app.route("/auth", methods=["GET", "POST"])
def auth():
    result = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            res = requests.post(
                f"{API_URL}/auth",
                json={"username": username, "password": password},
            )
            result = res.json()

            if "token" in result:
                session["token"] = result["token"]
        except requests.RequestException:
            result = api_unavailable()

    return render_template("auth.html", result=result)


@app.route("/logs")
def logs():
    try:
        res = requests.get(f"{API_URL}/logs")
        logs = res.json()
    except requests.RequestException:
        logs = ["API non disponible"]

    return render_template("logs.html", logs=logs)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
