# src/app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify, Response
from database.db_helper import DBHelper
from database.journal_db import init_journal_db, add_journal_entry, get_journal_entries, delete_journal_entry
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import chatbot as ch
import numpy as np

app = Flask(__name__)
app.secret_key = 'e5b0b6ce3b7b2b3e8f2c9c5c4b6a7d9a2e3c4e5f6a7b8c9d'  # Replace with a strong secret key

# --- Automatic Database Initialization ---
with app.app_context():
    # Creates the database tables before the first request
    # This will run once when the first user visits the site
    init_journal_db()
    print("Database initialized automatically on first request.")

def get_db():
    if 'db' not in g:
        g.db = DBHelper()
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.create_connection().close()

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('login3'))

@app.route('/login3', methods=['GET', 'POST'])
def login3():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_db().get_user(username, password)
        if user:
            session['user_id'] = user[0]  # Store user ID in session
            session['username'] = user[1]  # Store username in session
            flash(f"User {username} logged in successfully.", 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login3.html')

@app.route('/register', methods=['GET', 'POST'])
def register2():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        education = request.form['education']
        dob = request.form['dob']
        try:
            get_db().create_user(username, password, name, age, gender, education, dob)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login3'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
    return render_template('register2.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login3'))
    
    user = get_db().get_user_by_id(session['user_id'])
    if user is None:
        flash('User not found', 'error')
        return redirect(url_for('login3'))

    user_data = {
        'username': user[1],
        'name': user[3],
        'age': user[4],
        'gender': user[5],
        'education': user[6],
        'dob': user[7]
    }
    return render_template('profile.html', user=user_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login3'))

@app.route('/mood-tracker', methods=['GET', 'POST'])
def mood_tracker():
    if request.method == 'POST':
        mood = request.form['mood']
        note = request.form['note']
        get_db().insert_mood(mood, note)
        flash('Mood saved successfully!', 'success')
        return redirect(url_for('mood_tracker'))
    return render_template('mood_tracker.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_route():  # Renamed to avoid conflict
    user_input = ""
    response = ""
    
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = ch.get_chatbot_response(user_input)
        return jsonify({"response": response})

    return render_template('chatbot.html', user_input=user_input, response=response)


@app.route('/visualization')
def visualization():
    mood_data = get_db().get_mood_data()
    return render_template('visualization.html', mood_data=mood_data)

@app.route('/mindfulness')
def mindfulness():
    return render_template('mindfulness.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route("/breathing")
def breathing():
    return render_template("breathing.html")

@app.route('/game1')
def game1():
    return render_template('game1.html')

@app.route('/game2')
def game2():
    return render_template('game2.html')

# --- The route that handles the journaling page ---
@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'user_id' not in session:
        return redirect(url_for('login3'))
    
    user = get_db().get_user_by_id(session['user_id'])
    if user is None:
        flash('User not found', 'error')
        return redirect(url_for('login3'))

    if request.method == 'POST':
        entry_text = request.form.get('entry')
        if entry_text:
            add_journal_entry(entry_text, session['user_id'])
            flash('Your gratitude entry has been saved!', 'success')
            return redirect(url_for('journal'))
    
    entries = get_journal_entries(session['user_id'])
    return render_template('journal.html', entries=entries, username=user[1])

@app.route('/delete-journal/<int:entry_id>', methods=['POST'])
def delete_journal(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login3'))

    # Call the new delete function from journal_db
    delete_journal_entry(entry_id, session['user_id'])
    flash('Journal entry deleted successfully.', 'success')
    return redirect(url_for('journal'))

# from emotion_detector import EmotionDetector
# import os
# import uuid

# import cv2

# from flask_cors import CORS
# CORS(app)

#   # Enable CORS for the entire app
# detector = EmotionDetector()


# # Route for the emotion detection page
# @app.route('/emotion-detection')
# def emotion_detection():
#     return render_template('emotion_detection.html')

# # Video feed endpoint
# # @app.route('/video-feed')
# # def video_feed():
# #     return Response(generate_frames(), 
# #                    mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed')
# def video_feed():
#     def generate():
#         cap = cv2.VideoCapture(0)
#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break
#             processed_frame, _ = detector.process_frame(frame)
#             ret, buffer = cv2.imencode('.jpg', processed_frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#         cap.release()
#     return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


# # def generate_frames():
# # #     cap = cv2.VideoCapture(0)
# # #     while True:
# # #         success, frame = cap.read()
# # #         if not success:
# # #             break
        
# # #         # Process frame
# # #         processed_frame, _ = detector.process_frame(frame)
        
# # #         # Encode frame
# # #         ret, buffer = cv2.imencode('.jpg', processed_frame)
# # #         frame_bytes = buffer.tobytes()
        
# # #         yield (b'--frame\r\n'
# # #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
# # import base64
# # @app.route('/process-frame', methods=['POST'])                                                                                                                                                                                              

# # def process_frame():
# #     try:
# #         data = request.get_json()
# #         header, encoded = data['frame'].split(",", 1)
#         frame = cv2.imdecode(np.frombuffer(base64.b64decode(encoded)), cv2.IMREAD_COLOR)
#         processed_frame, analysis = detector.process_frame(frame)
#         _, buffer = cv2.imencode('.jpg', processed_frame)
#         return jsonify({
#             'faces': analysis,
#             'processed_frame': f"data:image/jpeg;base64,{base64.b64encode(buffer).decode()}"
#         })
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Image upload endpoint
# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     # Save uploaded file
#     filename = f"{uuid.uuid4()}.jpg"
#     save_path = os.path.join('static', 'uploads', filename)
#     file.save(save_path)
    
#     # Process image
#     image = cv2.imread(save_path)
#     processed_image, results = detector.process_frame(image)
#     cv2.imwrite(save_path, processed_image)
    
#     return jsonify({
#         'image_url': f'/static/uploads/{filename}',
#         'analysis': results
#     })


if __name__ == '__main__':
    app.run(debug=True)
