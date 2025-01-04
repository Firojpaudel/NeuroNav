from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# Define caretaker credentials
CARETAKER_EMAIL = "caretaker@mail.com"
CARETAKER_PASSWORD = "caretaker123"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/caretaker", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate caretaker credentials
    if email == CARETAKER_EMAIL and password == CARETAKER_PASSWORD:
        flash("Welcome, Caretaker! Login successful.", "success")
        return redirect(url_for("caretaker"))
    else:
        flash("Invalid caretaker email or password.", "danger")
        return redirect(url_for("index"))

@app.route("/caretaker")
def caretaker():
    return render_template("caretaker.html")

if __name__ == "__main__":
    app.run(debug=True)
