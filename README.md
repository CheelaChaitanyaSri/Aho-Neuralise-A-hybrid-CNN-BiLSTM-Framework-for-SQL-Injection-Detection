# Overview
This project implements a hybrid detection pipeline for SQL injection attacks. It combines Aho‑Corasick string matching with a deep learning model (CNN + BiLSTM + Attention) to achieve high accuracy while ensuring fast rule‑based filtering.

# Datasets
We used four original datasets (total 8 .csv files): 

https://www.kaggle.com/datasets/sajid576/sql-injection-dataset
Modified_SQL_Dataset.csv

https://www.kaggle.com/datasets/syedsaqlainhussain/sql-injection-dataset
sqli.csv 

sqliv2.csv 

SQLiV3.csv

https://www.kaggle.com/datasets/grgorqutel/superviz25-sql-injection-detection-dataset
dataset.csv (new dataset with full_query + label)

Additionally, one dataset was already provided in split format:

https://www.kaggle.com/datasets/ayahkhaldi/sql-injection-dataset
Train.csv

Validation.csv

Test.csv

These three files belong to the same dataset and represent its training, validation, and testing partitions. They were used directly without merging, to preserve clean evaluation.

All datasets were merged and standardized into a unified format: Query + Label.
https://drive.google.com/file/d/1LDgX4bSXITbjjzFEIQuLC1UmBMohz8PB/view?usp=drive_link

# Preprocessing
Tokenization using Keras Tokenizer

Padding sequences to fixed length

Train/Test/Validation split stored as CSV files

No normalization applied (case and symbols preserved to detect obfuscation attacks)

Aho‑Corasick integration: queries are first scanned using Aho‑Corasick to quickly detect known malicious patterns before passing to ML.

# Model Architecture
Stage 1: Aho‑Corasick → fast string matching to flag obvious SQL injection keywords/patterns.

Stage 2: CNN + BiLSTM + Attention → deeper analysis of queries that pass Stage 1, capturing obfuscation and complex attack structures.

# Why Aho‑Corasick Was Used
Efficiency: Aho‑Corasick can scan queries in linear time against thousands of attack signatures.

Rule‑based filtering: It catches straightforward SQLi attempts without needing ML.

Hybrid robustness: By combining Aho‑Corasick with ML, the pipeline balances speed (rule‑based) and intelligence (deep learning).

Reduced false negatives: ML focuses on obfuscated or novel attacks, while Aho‑Corasick handles known signatures.

# Training Results
Best validation accuracy: 98.9% (epoch 2)

Final test accuracy: 98.7% (~99%)(epoch 7)

Model saved as: cnn_bilstm_attention.h5

#Evaluation Metrics
Accuracy

Precision

Recall

F1 Score

False Positive Rate (FPR)

False Negative Rate (FNR)

Classification Report
