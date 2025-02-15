from flask import Flask, jsonify, render_template, request
from config.database import get_db_connection
import random
from datetime import datetime

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    try:
        return jsonify({"message": f"Successfully added genre!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/user_profile', methods=['GET'])
def get_user_details():
    try:
        return jsonify({"message": f"Successfully added genre!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/connect', methods=['POST'])
def create_connect():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        val1 = ''
        val2 = ''

        cursor.execute(
            "INSERT INTO Message (Title, Message) VALUES (%s, %s)", 
            (val1, val2)
        )

        conn.commit()
        conn.close()
        return jsonify({"message": f"Successfully added director!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/search_connect', methods=['GET'])
def search_connectsearch_connect():
    try:
        return jsonify({
            "execution_time": round(121212212, 3)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
