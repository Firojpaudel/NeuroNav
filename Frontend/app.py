from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# Sample data (in a real application, use a database)
users = {
    "test@example.com": {"name": "Test User", "password": "password123"}
}

@app.route("/")
def index():
    return render_template("index.html")  # Ensure this is your HTML file name

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate user credentials
    user = users.get(email)
    if user and user["password"] == password:
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("index"))
    else:
        flash("Invalid email or password.", "danger")
        return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if email already exists
    if email in users:
        flash("This email is already registered.", "danger")
        return redirect(url_for("index"))

    # Register the user
    users[email] = {"name": name, "password": password}
    flash("Registration successful! You can now log in.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)