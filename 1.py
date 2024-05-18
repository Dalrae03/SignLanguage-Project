# 필요한 라이브러리를 임포트합니다.
import cv2
import mediapipe as mp
import numpy as np
import time, os

# 인식할 손동작과 해당 동작의 번역을 정의합니다.
actions = ['greetings', 'hello', 'meet', 'part', 'glad', 'worry', 'introduction', 'name', 'age', 'you', 'me', 'live', 'know', 'dont know', 'right', 'no', 'what', 'thanks', 'fine', 'want']
translations = {
    'greetings': 'greet',
    'hello': 'hello',
    'meet': 'meet',
    'part': 'part',
    'glad': 'glad',
    'worry': 'worry',
    'introduction': 'intro',
    'name': 'name',
    'age': 'age',
    'you': 'u',
    'me': 'me',
    'live': 'live',
    'know': 'know',
    'dont know': 'dont know',
    'right': 'right',
    'no': 'no',
    'what': 'what',
    'thanks': 'thank',
    'fine': 'fine',
    'want': 'want'
}

# 데이터 수집 시 설정할 시퀀스 길이와 각 동작을 수집하는 시간(초)입니다.
seq_length = 30
secs_for_action = 60

# MediaPipe 라이브러리로 손동작 인식 모델을 초기화합니다.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# 웹캠을 초기화합니다.
cap = cv2.VideoCapture(1)
created_time = int(time.time())
os.makedirs('dataset', exist_ok=True) # 데이터셋을 저장할 폴더를 생성합니다.

# 웹캠이 열려 있는 동안 루프를 실행합니다.
while cap.isOpened():
    for idx, action in enumerate(actions): # 정의된 각 동작에 대해 반복합니다.
        data = []
        print(f'Collecting data for {action}...')
        start_time = time.time()

        while time.time() - start_time < secs_for_action: # 설정한 시간 동안 데이터를 수집합니다.
            ret, img = cap.read()
            img = cv2.flip(img, 1) # 이미지를 좌우 반전합니다.
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if result.multi_hand_landmarks is not None:
                for res in result.multi_hand_landmarks:
                    joint = np.zeros((21, 4)) # 손의 랜드마크를 저장할 배열을 초기화합니다.
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

                    # 랜드마크 간의 각도를 계산합니다.
                    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3]
                    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3]
                    v = v2 - v1
                    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                    angle = np.arccos(np.einsum('nt,nt->n', v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]))
                    angle = np.degrees(angle)

                    angle_label = np.array([angle], dtype=np.float32)
                    angle_label = np.append(angle_label, idx)

                    d = np.concatenate([joint.flatten(), angle_label])

                    data.append(d)

                    mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

            # 화면에 동작의 번역 텍스트를 표시합니다.
            cv2.putText(img, f'Translation: {translations[action]}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.imshow('img', img)
            if cv2.waitKey(1) == ord('q'): # 'q'를 누르면 종료합니다.
                break

        data = np.array(data)
        print(f'{action} Data Shape:', data.shape)
        np.save(os.path.join('dataset', f'raw_{action}_{created_time}'), data) # 수집된 데이터를 저장합니다.

        # 시퀀스 데이터를 생성합니다.
        full_seq_data = []
        for seq in range(len(data) - seq_length):
            full_seq_data.append(data[seq:seq + seq_length])

        full_seq_data = np.array(full_seq_data)
        print(f'{action} Sequence Data Shape:', full_seq_data.shape)
        np.save(os.path.join('dataset', f'seq_{action}_{created_time}'), full_seq_data)

cap.release()
cv2.destroyAllWindows()