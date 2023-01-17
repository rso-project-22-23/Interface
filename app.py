from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS
import requests
import json
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)


@app.route("/items")
def items():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    store_list, _ = fetch_stores(perform_authenticate=False)

    return render_template("items.html", stores=store_list)


@app.route("/items/add-item")
def add_item():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    store_list, _ = fetch_stores(perform_authenticate=False)

    return render_template("add_item.html", stores=store_list)


@app.route("/items/<barcode>")
def item(barcode):
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    r = requests.get("http://20.31.253.184/entity-editor/v1/get-items", params={"barcode": barcode})
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        return "404: Item with this barcode not found", 404
    item_dict = list(dict(content).values())[0]

    store_list, _ = fetch_stores(perform_authenticate=False)

    return render_template("item.html", item=item_dict["Item"], prices=item_dict["Price"], stores=store_list)


@app.route("/stores")
def stores():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    return render_template("stores.html")


@app.route("/")
def ui_root():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
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


@app.route("/not-activated")
def not_activated():
    if authenticate(request) != "Not activated":
        return redirect(url_for("items"))
    return render_template("auth/not_activated.html")


@app.route("/reset-password")
def reset_password():
    if authenticate(request):
        return redirect(url_for("items"))
    return render_template("auth/reset_password.html")


@app.route("/my-lists")
def my_lists():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    return render_template("item_lists.html")


@app.route("/my-lists/<list_id>")
def my_list(list_id):
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    return render_template("item_list.html")


@app.route("/favourites")
def favourites():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    return render_template("favourites.html")


@app.route("/basket")
def basket():
    authenticated = authenticate(request)
    if authenticated == "Not activated":
        return redirect(url_for("not_activated"))
    elif not authenticate(request):
        return redirect(url_for("login"))

    return render_template("basket.html")


@app.route("/ajax/login", methods=["POST"])
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

    return content, r.status_code


@app.route("/ajax/logout", methods=["POST"])
def perform_logout():
    header_dict = {"user": json.loads(unquote(request.cookies.get("auth-data")))["auth-email"]}

    r = requests.post("http://20.31.253.184/authentication-service/v1/logout", headers=header_dict)
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        content = r.content.decode("utf8")

    return [content], r.status_code


@app.route("/ajax/register", methods=["POST"])
def perform_register():
    header_dict = {
        "user": request.form["user"],
        "password": request.form["password"],
        "repeatPassword": request.form["repeatPassword"]
    }

    r = requests.post("http://20.31.253.184/authentication-service/v1/register", headers=header_dict)
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        content = r.content.decode("utf8")

    if isinstance(content, bool):
        content = str(content)

    return content, r.status_code


@app.route("/ajax/stores")
def fetch_stores(perform_authenticate=True):
    if perform_authenticate:
        authenticated = authenticate(request)
        if authenticated == "Not activated":
            return redirect(url_for("not_activated"))
        elif not authenticated:
            return redirect(url_for("login"))

    store_filter = request.args.get("storeFilter")

    if not store_filter:
        r = requests.get("http://20.31.253.184/entity-editor/v1/get-stores")
    else:
        r = requests.get(f"http://20.31.253.184/entity-editor/v1/get-stores?nameContains={store_filter}")

    return json.loads(r.content.decode("utf8")), r.status_code


@app.route("/ajax/items")
def fetch_items(perform_authenticate=True):
    if perform_authenticate:
        authenticated = authenticate(request)
        if authenticated == "Not activated":
            return redirect(url_for("not_activated"))
        elif not authenticated:
            return redirect(url_for("login"))

    name_filter = request.args.get("nameFilter")
    store_filter = request.args.get("storeFilter")

    params = {}
    if name_filter not in ["", None]:
        params["nameContains"] = name_filter
    if store_filter not in ["", None]:
        params["storeName"] = store_filter
        params["storePriceOnly"] = True

    r = requests.get("http://20.31.253.184/entity-editor/v1/get-items", params=params)
    return json.loads(r.content.decode("utf8")), r.status_code


@app.route("/ajax/add-store", methods=["POST"])
def add_store(perform_authenticate=True):
    if perform_authenticate:
        authenticated = authenticate(request)
        if authenticated == "Not activated":
            return redirect(url_for("not_activated"))
        elif not authenticated:
            return redirect(url_for("login"))

    store_name = request.form["storeName"]

    if not store_name:
        return [{"Error": "Empty store name"}], 400

    r = requests.post("http://20.31.253.184/entity-editor/v1/add-store", headers={"storeName": store_name})
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        content = r.content.decode("utf8")

    return [content], r.status_code


@app.route("/ajax/add-price", methods=["POST"])
def perform_add_price(perform_authenticate=True):
    print("add price")
    if perform_authenticate:
        authenticated = authenticate(request)
        if authenticated == "Not activated":
            return redirect(url_for("not_activated"))
        elif not authenticated:
            return redirect(url_for("login"))

    header_dict = {
        "barcode": request.form["barcode"],
        "storeName": request.form["storeName"],
        "price": request.form["price"]
    }

    r = requests.post("http://20.31.253.184/entity-editor/v1/add-item-price", headers=header_dict)
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        content = r.content.decode("utf8")

    return [content], r.status_code


@app.route("/ajax/add-item", methods=["POST"])
def perform_add_item(perform_authenticate=True):
    if perform_authenticate:
        authenticated = authenticate(request)
        if authenticated == "Not activated":
            return redirect(url_for("not_activated"))
        elif not authenticated:
            return redirect(url_for("login"))

    header_dict = {
        "barcode": request.form["barcode"],
        "name": request.form["itemName"],
        "store": request.form["storeName"],
        "price": request.form["price"]
    }

    r = requests.post("http://20.31.253.184/entity-editor/v1/add-item", headers=header_dict)
    try:
        content = json.loads(r.content.decode("utf8"))
    except json.decoder.JSONDecodeError:
        content = r.content.decode("utf8")

    return [content], r.status_code


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
    content = r.content.decode("utf8")
    if content == "Not activated":
        return content
    try:
        content = json.loads(content)
        if not isinstance(content, bool):
            return False
    except json.decoder.JSONDecodeError:
        content = bool(content)

    return content


if __name__ == "__main__":
    app.run()
