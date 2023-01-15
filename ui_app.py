from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/items")
def items():
    return render_template("items.html")

@app.route("/stores")
def stores():
    return render_template("stores.html")


@app.route("/")
def ui_root():
    return redirect(url_for("items"))


@app.route("/register")
def register():
    pass


@app.route("/login")
def login():
    pass


@app.route("/forgot-password")
def forgot_password():
    pass


@app.route("/reset-password")
def reset_password():
    pass


@app.route("/my-lists")
def lists():
    pass


@app.route("/favourites")
def favourites():
    pass


@app.route("/basket")
def basket():
    pass


if __name__ == "__main__":
    app.run()
