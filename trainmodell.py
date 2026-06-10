import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # hide INFO + WARNING
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Conv1D, MaxPooling1D, LSTM, Bidirectional, Dense, Dropout, Flatten, Attention

# 🔹 Step 1: Load tokenizer (saved during preprocessing)
with open("dataa/tokenizer_20260531_073337.pkl", "rb") as f:
    tokenizer = pickle.load(f)

X_train = pd.read_csv("dataa/X_train_20260531_073337.csv").values
y_train = pd.read_csv("dataa/y_train_20260531_073337.csv").values.ravel()
X_test = pd.read_csv("dataa/X_test_20260531_073337.csv").values
y_test = pd.read_csv("dataa/y_test_20260531_073337.csv").values.ravel()

MAX_LEN = 200
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 128

# 🔹 Step 3: Define model
inputs = Input(shape=(MAX_LEN,))
x = Embedding(vocab_size, embedding_dim, input_length=MAX_LEN)(inputs)

# CNN block
x = Conv1D(filters=128, kernel_size=5, activation="relu")(x)
x = MaxPooling1D(pool_size=2)(x)

# BiLSTM block
x = Bidirectional(LSTM(64, return_sequences=True))(x)

# Attention block
attn = Attention()([x, x])
x = Flatten()(attn)

# Dense layers
x = Dense(64, activation="relu")(x)
x = Dropout(0.5)(x)
outputs = Dense(1, activation="sigmoid")(x)

model = Model(inputs, outputs)
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 🔹 Step 4: Train model
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=7,
    batch_size=64
)

# 🔹 Step 5: Evaluate
loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc:.4f}")

# 🔹 Step 6: Save model
model.save("cnn_bilstm_attention.h5")
print("✅ Model saved as cnn_bilstm_attention.h5")

# 🔹 Step 7: Plot training curves
plt.figure(figsize=(12,5))

# Accuracy plot
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.title("Accuracy over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

# Loss plot
plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title("Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.tight_layout()
plt.show()

# 🔹 Step 8: Classification report
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print(classification_report(y_test, y_pred))

