from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS
import requests
import json
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)


@app.route("/items")
def items():
    if not authenticate(request):
        return redirect(url_for("login"))

    return render_template("items.html")


@app.route("/items/add-item")
def add_item():
    if not authenticate(request):
        return redirect(url_for("login"))

    return render_template("add_item.html")


@app.route("/items/<barcode>")
def item(barcode):
    if not authenticate(request):
        return redirect(url_for("login"))

    return render_template("item.html")


@app.route("/stores")
def stores():
    if not authenticate(request):
        return redirect(url_for("login"))

    return render_template("stores.html")


@app.route("/stores/add-store")
def add_store():
    if not authenticate(request):
        return redirect(url_for("login"))

    return render_template("add_store.html")


@app.route("/")
def ui_root():
    if not authenticate(request):
        return redirect(url_for("login"))

    return redirect(url_for("items"))


@app.route("/register")
def register():
    if authenticate(request):
        return redirect(url_for("items"))
    return render_template("auth/register.html")


@app.route("/login")
def login():
    if authenticate(request):
        return redirect(url_for("items"))
    return render_template("auth/login.html")


@app.route("/reset-password")
def reset_password():
    if authenticate(request):
        return redirect(url_for("items"))
    return render_template("auth/reset_password.html")


@app.route("/my-lists")
def lists():
    authenticated = authenticate(request)
    if not authenticated:
        return redirect(url_for("login"))

    return render_template("item_lists.html")


@app.route("/my-lists/<list_id>")
def list(list_id):
    authenticated = authenticate(request)
    if not authenticated:
        return redirect(url_for("login"))

    return render_template("item_list.html")


@app.route("/favourites")
def favourites():
    authenticated = authenticate(request)
    if not authenticated:
        return redirect(url_for("login"))

    return render_template("favourites.html")


@app.route("/basket")
def basket():
    authenticated = authenticate(request)
    if not authenticated:
        return redirect(url_for("login"))

    return render_template("basket.html")


@app.route("/ajax/login", methods=['POST'])
def perform_login():
    header_dict = {
        "user": request.form["user"],
        "password": request.form["password"]
    }

    r = requests.post("http://20.31.253.184/authentication-service/v1/login", headers=header_dict)
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        content = r.content.decode("utf8")
    print(content)

    return content, r.status_code


def authenticate(r):
    try:
        cookie = json.loads(unquote(r.cookies.get("auth-data")))
        header_dict = {
            "userEmail": cookie["auth-email"],
            "token": cookie["auth-token"]
        }
    except (TypeError, KeyError):
        return False

    r = requests.post("http://20.31.253.184/authentication-service/v1/authenticate", headers=header_dict)
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        print("except")
        content = bool(r.content.decode("utf8"))
    print(content)

    return content


if __name__ == "__main__":
    app.run()
