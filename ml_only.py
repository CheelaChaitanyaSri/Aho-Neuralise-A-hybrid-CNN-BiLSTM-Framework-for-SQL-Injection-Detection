import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # hide INFO + WARNING, keep errors
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # suppress TF warnings

import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# --- Load ML model ---
print("Loading CNN-BiLSTM-Attention model...")
model = load_model("cnn_bilstm_attention.h5")
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
