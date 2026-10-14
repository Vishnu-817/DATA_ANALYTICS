import logging
import os
import re
from datetime import date, datetime
from pathlib import Path

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_from_directory

load_dotenv()

app = Flask(__name__, static_folder=None)
logging.basicConfig(level=logging.INFO)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=int(os.getenv("PGPORT", "5432")),
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        dbname=os.environ["PGDATABASE"],
        sslmode="require"
    )


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/styles.css")
def stylesheet():
    return send_from_directory(Path(app.root_path) / "public", "styles.css")


@app.get("/app.js")
def javascript():
    return send_from_directory(Path(app.root_path) / "public", "app.js")


@app.get("/api/menu")
def menu():
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            "SELECT id, name, description, price, category, image_url "
            "FROM menu_items WHERE available = TRUE ORDER BY category, name"
        )
        items = cursor.fetchall()
        return jsonify(items)
    except psycopg2.Error:
        app.logger.exception("Could not load menu from PostgreSQL")
        return jsonify({"error": "The menu is temporarily unavailable."}), 503
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.post("/api/reservations")
def create_reservation():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Please submit a valid reservation."}), 400

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    reservation_date = str(data.get("date", "")).strip()
    reservation_time = str(data.get("time", "")).strip()
    notes = str(data.get("notes", "")).strip()

    try:
        guests = int(data.get("guests", 0))
        parsed_date = datetime.strptime(reservation_date, "%Y-%m-%d").date()
        datetime.strptime(reservation_time, "%H:%M")
    except (TypeError, ValueError):
        return jsonify({"error": "Choose a valid date, time, and party size."}), 400

    if (
        not name
        or len(name) > 100
        or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
        or len(email) > 254
        or len(phone) > 30
        or len(notes) > 1000
        or not 1 <= guests <= 20
        or parsed_date < date.today()
    ):
        return jsonify({"error": "Please check the reservation details and try again."}), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO reservations "
            "(customer_name, email, phone, reservation_date, reservation_time, guests, notes) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, email, phone or None, reservation_date, reservation_time, guests, notes or None),
        )
        connection.commit()
        return jsonify({"message": "Your table request has been received."}), 201
    except psycopg2.Error:
        if connection is not None:
            connection.rollback()
        app.logger.exception("Could not save reservation to PostgreSQL")
        return jsonify({"error": "We couldn't save your reservation. Please try again."}), 503
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")   