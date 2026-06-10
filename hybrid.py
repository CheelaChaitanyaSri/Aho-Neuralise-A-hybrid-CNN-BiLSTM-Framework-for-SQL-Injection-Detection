import os
# Suppress TensorFlow INFO + WARNING logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Layer

# --- Custom Attention layer patch ---
class Attention(Layer):
    def __init__(self, score_mode="dot", use_scale=False, dropout=0.0, **kwargs):
        # Fix corrupted serialization: if score_mode is a function, force "dot"
        if callable(score_mode):
            score_mode = "dot"
        super().__init__(**kwargs)
        self.score_mode = score_mode
        self.use_scale = use_scale
        self.dropout = dropout

    def call(self, inputs):
        query, values = inputs
        score = tf.matmul(query, values, transpose_b=True)
        weights = tf.nn.softmax(score, axis=-1)
        if self.dropout > 0.0:
            weights = tf.nn.dropout(weights, rate=self.dropout)
        return tf.matmul(weights, values)

# --- Load ML model ---
print("Loading CNN-BiLSTM-Attention model...")
model = load_model("cnn_bilstm_attention.h5", custom_objects={"Attention": Attention})
print("Model loaded successfully.")

# --- Load tokenizer ---
with open("dataa/tokenizer_20260529_082552.pkl", "rb") as f:
    tokenizer = pickle.load(f)

MAXLEN = 200  # must match training

def run_ml(query):
    seq = tokenizer.texts_to_sequences([query])
    padded = pad_sequences(seq, maxlen=MAXLEN)
    score = model.predict(padded, verbose=0)[0][0]
    return score

# --- Main loop ---
if __name__ == "__main__":
    while True:
        query = input("\nEnter SQL query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        score = run_ml(query)
        if score > 0.5:
            print(f"Blocked by ML model (score={score:.2f})")
        else:
            print(f"Clean query (score={score:.2f})")

