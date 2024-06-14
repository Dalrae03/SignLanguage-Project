import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model

# MediaPipe 손동작 인식 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 학습된 모델 로드
model = load_model('models/model.keras')

# 액션 리스트 정의
actions = ['greetings', 'hello', 'meet', 'part', 'glad', 'worry', 'introduction', 'name', 'age', 'you', 'me', 'live', 'know', 'dont know', 'right', 'no', 'what', 'thanks', 'fine', 'want']
translations = {
    'greetings': 'greetings',
    'hello': 'hello',
    'meet': 'meet',
    'part': 'part',
    'glad': 'glad',
    'worry': 'worry',
    'introduction': 'introduction',
    'name': 'name',
    'age': 'age',
    'you': 'you',
    'me': 'me',
    'live': 'live',
    'know': 'know',
    'dont know': 'dont know',
    'right': 'right',
    'no': 'no',
    'what': 'what',
    'thanks': 'thanks',
    'fine': 'fine',
    'want': 'want'
}


# 웹캠 초기화
cap = cv2.VideoCapture(0)

seq = []  # 손동작 시퀀스 데이터 저장 리스트
action_seq = []  # 인식된 액션 시퀀스 저장 리스트

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue

    img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            joint = np.zeros((21, 3))
            for j, lm in enumerate(hand_landmarks.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # 손동작 시퀀스에 추가
            seq.append(joint.flatten())

            if len(seq) == 30:  # 시퀀스 길이 확인
                input_data = np.expand_dims(np.array(seq), axis=0)
                # 모델이 기대하는 차원으로 입력 데이터 조정
                input_data_padded = np.pad(input_data, ((0,0), (0,0), (0,36)), mode='constant', constant_values=0)
                y_pred = model.predict(input_data_padded).squeeze()
                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]

                if conf > 0.9:
                    action = actions[i_pred]
                    action_seq.append(action)

                    if len(action_seq) == 5:
                        most_common = max(set(action_seq), key=action_seq.count)
                        action_text = translations[most_common]  # 번역된 텍스트를 정의하는 부분
                        print(f"Action: {most_common}, Confidence: {conf:.2f}")
                        # 화면에 번역된 텍스트를 출력하는 부분
                        cv2.putText(img, f'Translated Text: {action_text}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        action_seq = []


                seq.pop(0)

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
