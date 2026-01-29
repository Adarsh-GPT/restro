"""
Model Training Script for Restaurant Sentiment Analysis
Uses LinearSVC (no Naive Bayes) with TF-IDF vectorization and probability calibration.
"""

import os
import pickle
import logging

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

from preprocess import preprocess_text

# Configuration
DATA_PATH = 'data/Yelp Restaurant Reviews.csv'
MODEL_PATH = 'sentiment_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger('train_model')


def load_dataset(filepath):
    logger.info(f"Loading dataset from {filepath}...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Dataset shape: {df.shape}")
    logger.info(f"Columns: {df.columns.tolist()}")
    return df


def create_sentiment_labels(df, rating_col='stars'):
    logger.info(f"Creating sentiment labels from '{rating_col}' column...")
    df = df.copy()
    df['sentiment'] = df[rating_col].apply(lambda x: 1 if x >= 4 else (0 if x <= 2 else None))
    df_filtered = df[df['sentiment'].notna()].copy()
    df_filtered['sentiment'] = df_filtered['sentiment'].astype(int)
    logger.info(f"Dataset after removing neutral reviews: {df_filtered.shape}")
    logger.info(f"Sentiment distribution:\n{df_filtered['sentiment'].value_counts().to_dict()}")
    return df_filtered


def preprocess_dataset(df, text_col='text'):
    logger.info("Preprocessing text data...")
    texts = df[text_col].astype(str).apply(preprocess_text).tolist()
    labels = df['sentiment'].tolist()
    return texts, labels


def build_and_train_model(X_train_texts, y_train, max_features=5000):
    logger.info("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=(1, 2), stop_words='english')
    X_train = vectorizer.fit_transform(X_train_texts)
    logger.info("Training LinearSVC model and calibrating probabilities...")
    base_clf = LinearSVC(class_weight='balanced', max_iter=10000, random_state=42)
    clf = CalibratedClassifierCV(base_clf, cv=5)  # enables predict_proba
    clf.fit(X_train, y_train)
    logger.info("Training complete.")
    return vectorizer, clf


def evaluate_model(vectorizer, model, X_test_texts, y_test):
    logger.info("Evaluating model on test set...")
    X_test = vectorizer.transform(X_test_texts)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    logger.info(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
    logger.info("Classification report:\n" + classification_report(y_test, preds))
    return {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}


def save_model_and_vectorizer(model, vectorizer, model_path, vectorizer_path):
    logger.info(f"Saving model to {model_path} and vectorizer to {vectorizer_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    logger.info("Saved model and vectorizer.")


def main():
    df = load_dataset(DATA_PATH)
    df_filtered = create_sentiment_labels(df, rating_col='Rating')
    texts, labels = preprocess_dataset(df_filtered, text_col='Review Text')
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)
    vectorizer, model = build_and_train_model(X_train, y_train)
    metrics = evaluate_model(vectorizer, model, X_test, y_test)
    save_model_and_vectorizer(model, vectorizer, MODEL_PATH, VECTORIZER_PATH)
    logger.info("Training pipeline finished.")


if __name__ == '__main__':
    main()
