import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

class EmotionDetector:
    def __init__(self):
        self.model = load_model(os.path.join('src', 'models', 'emotion_model.h5'))
        self.face_cascade = cv2.CascadeClassifier(
            os.path.join('src', 'utils', 'haarcascade_frontalface_default.xml')
        )
        self.class_names = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

    def process_frame(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            analysis = []

            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (48, 48))
                face_roi = np.expand_dims(face_roi, axis=-1)
                face_roi = face_roi.reshape(1, 48, 48, 1) / 255.0
                
                prediction = self.model.predict(face_roi)
                emotion = self.class_names[np.argmax(prediction)]
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, emotion, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                analysis.append({
                    'emotion': emotion,
                    'confidence': float(np.max(prediction)),
                    'position': [int(x), int(y), int(w), int(h)]
                })

            return frame, analysis
        except Exception as e:
            print(f"Processing error: {str(e)}")
            return frame, []