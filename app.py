from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# MediaPipe 손동작 인식과 모델 로드
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
model = load_model('models/model.keras')

actions = ['greetings', 'hello', 'meet', 'part', 'glad', 'worry', 'introduction', 'name', 'age', 'you', 'me', 'live', 'know', 'dont know', 'right', 'no', 'what', 'thanks', 'fine', 'want']
translations = {action: action for action in actions}

def generate_frames():
    cap = cv2.VideoCapture(0)
    seq = []
    action_seq = []

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    joint = np.zeros((21, 3))
                    for j, lm in enumerate(hand_landmarks.landmark):
                        joint[j] = [lm.x, lm.y, lm.z]
                    seq.append(joint.flatten())

                    if len(seq) == 30:
                        input_data = np.expand_dims(np.array(seq), axis=0)
                        input_data_padded = np.pad(input_data, ((0,0), (0,0), (0,36)), mode='constant', constant_values=0)
                        y_pred = model.predict(input_data_padded).squeeze()
                        i_pred = int(np.argmax(y_pred))
                        conf = y_pred[i_pred]

                        if conf > 0.9:
                            action = actions[i_pred]
                            action_seq.append(action)

                            if len(action_seq) == 5:
                                most_common = max(set(action_seq), key=action_seq.count)
                                action_text = translations[most_common]
                                cv2.putText(frame, f'Translated Text: {action_text}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                                action_seq = []

                        seq.pop(0)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('cam.ejs')

if __name__ == '__main__':
    app.run(debug=True)
