import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from db import fetch_one, fetch_all, execute_query
from burnout import BurnoutAnalyzer

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "study-burnout-secret-key")


def login_required():
    return "user_id" in session


@app.route("/")
def index():
    if login_required():
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Please fill in all fields.")
            return redirect(url_for("register"))

        existing_user = fetch_one("SELECT id FROM users WHERE username = %s", (username,))
        if existing_user:
            flash("This username already exists.")
            return redirect(url_for("register"))

        execute_query(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, generate_password_hash(password)),
        )
        flash("Account created. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    entries = fetch_all(
        "SELECT * FROM burnout_entries WHERE user_id = %s ORDER BY entry_date DESC, created_at DESC LIMIT 7",
        (session["user_id"],),
    )

    latest = entries[0] if entries else None
    avg_burnout = round(sum(e["burnout_score"] for e in entries) / len(entries), 1) if entries else 0
    avg_productivity = round(sum(e["productivity_score"] for e in entries) / len(entries), 1) if entries else 0

    chart_labels = [str(e["entry_date"]) for e in reversed(entries)]
    burnout_data = [int(e["burnout_score"]) for e in reversed(entries)]
    productivity_data = [int(e["productivity_score"]) for e in reversed(entries)]
    sleep_data = [float(e["sleep_hours"]) * 10 for e in reversed(entries)]
    stress_data = [int(e["stress_level"]) * 10 for e in reversed(entries)]

    advice = BurnoutAnalyzer.get_advice(latest["risk_level"]) if latest else "Add your first daily record to see advice."

    return render_template(
        "dashboard.html",
        entries=entries,
        latest=latest,
        avg_burnout=avg_burnout,
        avg_productivity=avg_productivity,
        chart_labels=chart_labels,
        burnout_data=burnout_data,
        productivity_data=productivity_data,
        sleep_data=sleep_data,
        stress_data=stress_data,
        advice=advice,
    )
@app.route("/add", methods=["GET", "POST"])
def add_entry():
    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        sleep_hours = float(request.form.get("sleep_hours", 0))
        study_hours = float(request.form.get("study_hours", 0))
        stress_level = int(request.form.get("stress_level", 1))
        mood_level = int(request.form.get("mood_level", 1))
        breaks_count = int(request.form.get("breaks_count", 0))
        notes = request.form.get("notes", "")
        entry_date = request.form.get("entry_date") or date.today()

        burnout_score = BurnoutAnalyzer.calculate_burnout_score(
            sleep_hours, study_hours, stress_level, mood_level, breaks_count
        )
        risk_level = BurnoutAnalyzer.get_risk_level(burnout_score)
        productivity_score = BurnoutAnalyzer.calculate_productivity_score(
            sleep_hours, study_hours, stress_level, mood_level, breaks_count
        )

        execute_query(
            """
            INSERT INTO burnout_entries
            (user_id, entry_date, sleep_hours, study_hours, stress_level, mood_level,
             breaks_count, notes, burnout_score, risk_level, productivity_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session["user_id"], entry_date, sleep_hours, study_hours, stress_level,
                mood_level, breaks_count, notes, burnout_score, risk_level, productivity_score,
            ),
        )
        flash("Daily record added successfully.")
        return redirect(url_for("dashboard"))

    return render_template("add_entry.html")


@app.route("/delete/<int:entry_id>")
def delete_entry(entry_id):
    if not login_required():
        return redirect(url_for("login"))
    execute_query("DELETE FROM burnout_entries WHERE id = %s AND user_id = %s", (entry_id, session["user_id"]))
    flash("Record deleted.")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
