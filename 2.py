import numpy as np
import os
import glob
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# GPU 설정
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

# 액션 정의
actions = ['greetings', 'hello', 'meet', 'part', 'glad', 'worry', 'introduction', 'name', 'age', 'you', 'me', 'live', 'know', 'dont know', 'right', 'no', 'what', 'thanks', 'fine', 'want']

max_length = 0
data_list = []
label_list = []

# 데이터 로딩 및 최대 길이 계산
for action in actions:
    file_pattern = f'dataset/seq_{action}_*.npy'
    for file_path in glob.glob(file_pattern):
        data = np.load(file_path)
        if data.size == 0:  # 빈 파일 건너뛰기
            print(f"Skipping {file_path} due to unexpected shape {data.shape}")
            continue
        if data.shape[1] > max_length:
            max_length = data.shape[1]
        labels = np.full((data.shape[0],), actions.index(action))  # 액션별 레이블 생성
        data_list.append(data)
        label_list.append(labels)

# 패딩 및 데이터 결합
padded_data_list = []
for data in data_list:
    padding_length = max_length - data.shape[1]
    padding = np.zeros((data.shape[0], padding_length, data.shape[2]))
    padded_data = np.concatenate([data, padding], axis=1)
    padded_data_list.append(padded_data)

padded_data = np.concatenate(padded_data_list, axis=0)
labels = np.concatenate(label_list, axis=0)

# 데이터 전처리
x_data = padded_data[:, :, :-1]
y_data = to_categorical(labels, num_classes=len(actions))

x_data = x_data.astype(np.float32)
y_data = y_data.astype(np.float32)

# 데이터 분할
x_train, x_val, y_train, y_val = train_test_split(x_data, y_data, test_size=0.1, random_state=2021)

# 모델 구성
model = Sequential([
    LSTM(64, activation='tanh', input_shape=x_train.shape[1:]),
    Dense(32, activation='relu'),
    Dense(len(actions), activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])

# 모델 학습
history = model.fit(
    x_train,
    y_train,
    validation_data=(x_val, y_val),
    epochs=200,
    callbacks=[
        ModelCheckpoint('models/model.keras', monitor='val_acc', verbose=1, save_best_only=True, mode='auto'),
        ReduceLROnPlateau(monitor='val_acc', factor=0.5, patience=50, verbose=1, mode='auto')
    ]
)

# 학습 결과 시각화
fig, loss_ax = plt.subplots(figsize=(16, 10))
acc_ax = loss_ax.twinx()

loss_ax.plot(history.history['loss'], 'y', label='train loss')
loss_ax.plot(history.history['val_loss'], 'r', label='val loss')
acc_ax.plot(history.history['acc'], 'b', label='train acc')
acc_ax.plot(history.history['val_acc'], 'g', label='val acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuracy')
loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

# 검증 데이터에 대한 모델 예측 및 혼동 행렬 시각화
model = load_model('models/model.keras')
y_pred = model.predict(x_val)
y_pred_labels = np.argmax(y_pred, axis=1)
y_true_labels = np.argmax(y_val, axis=1)

cm = confusion_matrix(y_true_labels, y_pred_labels)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=actions, yticklabels=actions)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# 분류 보고서 출력
print(classification_report(y_true_labels, y_pred_labels, target_names=actions))
