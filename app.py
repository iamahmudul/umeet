from flask import Flask, jsonify, render_template, request
from config.database import get_db_connection
import random
from datetime import datetime
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

@app.route('/api/user_profile', methods=['GET'])
def get_user_details():
    try:
        return jsonify({"message": f"Successfully fetched user!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/threads', methods=['GET'])
def get_threads():
    try:
        current_student_id = request.args.get('user_id')  # Get the student ID from the query parameters

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                m.id AS message_id,
                CASE 
                    WHEN m.group_id IS NOT NULL THEN g.name -- Group name if it's a group message
                    ELSE s2.name -- Other student's name if it's a direct message
                END AS thread_name,
                m.content AS last_message,
                m.created_at
            FROM messages m
            LEFT JOIN users s1 ON m.sender_id = s1.id
            LEFT JOIN users s2 ON m.receiver_id = s2.id
            LEFT JOIN groups g ON m.group_id = g.id
            LEFT JOIN group_members gm ON gm.group_id = m.group_id AND gm.student_id = %s
            WHERE 
                m.sender_id = %s 
                OR m.receiver_id = %s
                OR gm.student_id IS NOT NULL -- If part of a group, include group messages
            GROUP BY 
                m.id, thread_name, last_message, m.created_at
            ORDER BY 
                m.created_at DESC;
        """
        
        cursor.execute(query, (current_student_id, current_student_id, current_student_id))
        threads = cursor.fetchall()

        if threads:
            return jsonify({"threads": threads}), 200
        else:
            return jsonify({"message": "No threads found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close() 

@app.route('/api/thread/messages', methods=['GET'])
def get_thread_messages():
    try:
        current_student_id = request.args.get('current_student_id')
        selected_student_id = request.args.get('selected_student_id')
        selected_group_id = request.args.get('selected_group_id')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                m.id AS message_id,
                m.sender_id,
                s.name AS sender_name,
                m.content,
                m.created_at
            FROM messages m
            JOIN users s ON m.sender_id = s.id
            WHERE 
                (m.receiver_id = %s AND m.sender_id = %s)  -- direct message check (current student is receiver, selected student is sender)
                OR (m.sender_id = %s AND m.receiver_id = %s)  -- direct message check (current student is sender, selected student is receiver)
                OR (m.group_id = %s)  -- group message check (current student is a member of the group)
            ORDER BY 
                m.created_at ASC;
        """
        
        cursor.execute(query, (selected_student_id, current_student_id, selected_student_id, current_student_id, selected_group_id))
        messages = cursor.fetchall()

        if messages:
            return jsonify({"messages": messages}), 200
        else:
            return jsonify({"message": "No messages found in this thread."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')

        if not sender_id or not receiver_id or not content:
            return jsonify({"error": "Missing required fields."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO messages (sender_id, receiver_id, content, created_at)
        VALUES (%s, %s, %s, %s)
        """
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(query, (sender_id, receiver_id, content, created_at))
        
        conn.commit()

        return jsonify({"message": "Message sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if conn:
            conn.close()

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

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and user[2] == password:
            return jsonify({"message": "Login successful!"})
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

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
    app.run()
