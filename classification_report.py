import pickle
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Attention
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# 🔹 Load tokenizer (if needed later for text preprocessing)
with open("dataa/tokenizer_20260531_073337.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# 🔹 Load test data
X_test = pd.read_csv("dataa/X_test_20260531_073337.csv").values
y_test = pd.read_csv("dataa/y_test_20260531_073337.csv").values.ravel()

# 🔹 Load trained model with Attention fix
model = load_model("cnn_bilstm_attention.h5", custom_objects={"Attention": Attention})

# 🔹 Predictions
y_pred = (model.predict(X_test) > 0.5).astype("int32")

# 🔹 Core metrics
acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec  = recall_score(y_test, y_pred)
f1   = f1_score(y_test, y_pred)

print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")

# 🔹 Confusion matrix
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
fpr = fp / (fp + tn)
fnr = fn / (fn + tp)

print(f"False Positive Rate: {fpr:.4f}")
print(f"False Negative Rate: {fnr:.4f}")

# 🔹 Full classification report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
