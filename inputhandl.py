import pandas as pd
import pickle
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from datetime import datetime

# 🔹 Robust CSV loader function
def load_csv_robust(path, col_type="Sentence"):
    """
    Robust loader for SQLi datasets.
    - Forces exactly two columns: Sentence/Query + Label.
    - Handles cases where Label is stuck at the end of Sentence.
    """
    encodings = ["utf-8", "latin1", "cp1252"]
    for enc in encodings:
        try:
            df = pd.read_csv(
                path,
                encoding=enc,
                engine="python",
                names=[col_type, "Label"],  # enforce 2 columns
                header=0,
                delimiter=",",
                quotechar='"',
                on_bad_lines="skip"
            )
            print(f"Loaded {path} successfully with encoding={enc}")
            return df
        except Exception as e:
            print(f"Failed with encoding={enc}: {e}")
    raise ValueError(f"❌ Could not load {path} with any tested encoding.")

# 🔹 Step 1: Load datasets
data_folder = "dataa"
files = [
    ("Modified_SQL_Dataset.csv", "Query"),   # already Query + Label
    ("sqli.csv", "Sentence"),
    ("sqliv2.csv", "Sentence"),
    ("SQLiV3.csv", "Sentence"),
    ("dataset.csv", "full_query"),   # ✅ new dataset with full_query + label
    ("Train.csv", "Query"),          # ✅ if already split
    ("Validation.csv", "Query"),
    ("Test.csv", "Query")
]

dfs = []
for f, col_type in files:
    path = os.path.join(data_folder, f)
    if not os.path.exists(path):
        print(f"⚠️ Skipping {f} (file not found)")
        continue

    df = load_csv_robust(path, col_type)

    # Normalize column names
    if "Sentence" in df.columns:
        df.rename(columns={"Sentence": "Query"}, inplace=True)
    if "full_query" in df.columns:
        df.rename(columns={"full_query": "Query"}, inplace=True)

    # Ensure Label is numeric
    df["Label"] = pd.to_numeric(df["Label"], errors="coerce")
    df = df.dropna(subset=["Label"])  # drop rows without valid labels
    df["Label"] = df["Label"].astype(int)

    dfs.append(df)

# 🔹 Step 2: Merge datasets
dataset = pd.concat(dfs, ignore_index=True)
# ✅ Only keep Query + Label
dataset = dataset[["Query", "Label"]]
# ✅ Clean Query column to avoid float.translate error
dataset = dataset.dropna(subset=["Query"])        # remove rows with missing queries
dataset["Query"] = dataset["Query"].astype(str)   # ensure all queries are strings

# 🔹 Step 3: Tokenization (case + symbols preserved)
tokenizer = Tokenizer(char_level=False, lower=False, filters="")
tokenizer.fit_on_texts(dataset["Query"])

sequences = tokenizer.texts_to_sequences(dataset["Query"])

# 🔹 Step 4: Padding (fixed length for CNN+BiLSTM)
MAX_LEN = 200
X = pad_sequences(sequences, maxlen=MAX_LEN, padding="post", truncating="post")
y = dataset["Label"].values 

# 🔹 Step 5: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Dataset ready!")
print("Train shape:", X_train.shape, "Test shape:", X_test.shape)

# 🔹 Step 6: Save merged dataset
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
dataset.to_csv(f"dataa/merged_dataset_{ts}.csv", index=False)

# 🔹 Step 7: Save train/test splits
pd.DataFrame(X_train).to_csv(f"dataa/X_train_{ts}.csv", index=False)
pd.DataFrame(y_train).to_csv(f"dataa/y_train_{ts}.csv", index=False)
pd.DataFrame(X_test).to_csv(f"dataa/X_test_{ts}.csv", index=False)
pd.DataFrame(y_test).to_csv(f"dataa/y_test_{ts}.csv", index=False)

# 🔹 Step 8: Save tokenizer for reuse
with open(f"dataa/tokenizer_{ts}.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("Processed files saved in dataa folder with timestamped names!")

