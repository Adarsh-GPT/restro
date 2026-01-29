"""
Model Training Script for Restaurant Sentiment Analysis
=========================================================
Trains a Linear SVM classifier using TF-IDF vectorization
on the Yelp Reviews dataset.
"""

import pandas as pd
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from preprocess import preprocess_text

# Configuration
DATA_PATH = 'data/Yelp Restaurant Reviews.csv'
MODEL_PATH = 'sentiment_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'


def load_dataset(filepath):
    """
    Load the Yelp reviews dataset.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    print(f"Loading dataset from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    return df


def create_sentiment_labels(df, rating_col='stars'):
    """
    Create binary sentiment labels from ratings.
    
    Mapping:
    - rating >= 4 → Positive (1)
    - rating <= 2 → Negative (0)
    - rating = 3 → Ignored (neutral)
    
    Args:
        df (pd.DataFrame): Dataset with rating column
        rating_col (str): Name of the rating column
        
    Returns:
        pd.DataFrame: Dataset with sentiment labels and filtered rows
    """
    print(f"\nCreating sentiment labels from '{rating_col}' column...")
    
    # Create sentiment column
    df['sentiment'] = df[rating_col].apply(
        lambda x: 1 if x >= 4 else (0 if x <= 2 else None)
    )
    
    # Remove neutral reviews (rating = 3)
    df_filtered = df[df['sentiment'].notna()].copy()
    
    print(f"Dataset after removing neutral reviews: {df_filtered.shape}")
    print(f"Sentiment distribution:\n{df_filtered['sentiment'].value_counts()}")
    print(f"- Positive reviews: {(df_filtered['sentiment'] == 1).sum()}")
    print(f"- Negative reviews: {(df_filtered['sentiment'] == 0).sum()}")
    
    return df_filtered


def preprocess_dataset(df, text_col='text'):
    """
    Preprocess all reviews in the dataset.
    
    Args:
        df (pd.DataFrame): Dataset with text column
        text_col (str): Name of the text column
        
    Returns:
        pd.DataFrame: Dataset with preprocessed text
    """
    print(f"\nPreprocessing {len(df)} reviews (this may take a few minutes)...")
    df['processed_text'] = df[text_col].apply(preprocess_text)
    print("Preprocessing complete!")
    return df


def build_and_train_model(X_train, y_train):
    """
    Build TF-IDF vectorizer and train Linear SVM classifier.
    
    Args:
        X_train (list): Training text samples
        y_train (list): Training labels
        
    Returns:
        tuple: (vectorizer, model)
    """
    print("\nBuilding TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        min_df=2,
        max_df=0.95,
        ngram_range=(1, 2),
        stop_words='english'
    )
    
    X_train_vectorized = vectorizer.fit_transform(X_train)
    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")
    print(f"Training set shape: {X_train_vectorized.shape}")
    
    print("\nTraining Linear SVM classifier...")
    
    # LinearSVC with balanced class weights to handle imbalanced data
    # class_weight='balanced' automatically adjusts weights inversely proportional to class frequency
    print(f"Using balanced class weights to handle data imbalance")
    print(f"  - Negative class gets higher weight")
    print(f"  - Positive class gets lower weight")
    
    # Train Linear SVM with class weight balancing
    # C=1.0 is good default, dual=False for faster training with large datasets
    base_model = LinearSVC(
        class_weight='balanced',  # Automatically balances classes
        max_iter=2000,            # Ensure convergence
        dual=False,               # Faster for sparse data
        random_state=42,          # Reproducibility
        C=1.0                     # Regularization parameter
    )
    base_model.fit(X_train_vectorized, y_train)
    
    # Wrap with CalibratedClassifierCV to add probability estimates
    print("\nCalibrating model for probability estimates...")
    model = CalibratedClassifierCV(base_model, cv=5)
    model.fit(X_train_vectorized, y_train)
    
    print("Model training and calibration complete!")
    
    return vectorizer, model


def evaluate_model(vectorizer, model, X_test, y_test):
    """
    Evaluate the trained model on test set.
    
    Args:
        vectorizer: TF-IDF vectorizer
        model: Trained classifier
        X_test (list): Test text samples
        y_test (list): Test labels
    """
    print("\nEvaluating model on test set...")
    
    X_test_vectorized = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vectorized)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\nModel Performance Metrics:")
    print(f"- Accuracy:  {accuracy:.4f}")
    print(f"- Precision: {precision:.4f}")
    print(f"- Recall:    {recall:.4f}")
    print(f"- F1-Score:  {f1:.4f}")
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Negative', 'Positive']))


def save_model_and_vectorizer(model, vectorizer, model_path, vectorizer_path):
    """
    Save trained model and vectorizer to files.
    
    Args:
        model: Trained classifier
        vectorizer: TF-IDF vectorizer
        model_path (str): Path to save model
        vectorizer_path (str): Path to save vectorizer
    """
    print(f"\nSaving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Saving vectorizer to {vectorizer_path}...")
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("Model and vectorizer saved successfully!")


def main():
    """
    Main training pipeline.
    """
    print("="*60)
    print("RESTAURANT SENTIMENT ANALYSIS - MODEL TRAINING")
    print("="*60)
    
    # Check if data file exists
    if not os.path.exists(DATA_PATH):
        print(f"\nError: Dataset not found at {DATA_PATH}")
        print("Please ensure the CSV file is in the data/ directory.")
        return
    
    # Load dataset
    df = load_dataset(DATA_PATH)
    
    # Identify text and rating columns (handle various naming conventions)
    text_col = None
    rating_col = None
    
    for col in df.columns:
        col_lower = col.lower()
        if 'text' in col_lower or 'review' in col_lower:
            text_col = col
        if 'star' in col_lower or 'rating' in col_lower or 'score' in col_lower:
            rating_col = col
    
    if not text_col or not rating_col:
        print(f"Error: Could not identify text or rating columns.")
        print(f"Available columns: {df.columns.tolist()}")
        return
    
    print(f"Using text column: '{text_col}'")
    print(f"Using rating column: '{rating_col}'")
    
    # Create sentiment labels
    df = create_sentiment_labels(df, rating_col)
    
    # Preprocess dataset
    df = preprocess_dataset(df, text_col)
    
    # Prepare training and test sets
    print("\nPreparing training and test sets...")
    X = df['processed_text'].tolist()
    y = df['sentiment'].tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Build and train model
    vectorizer, model = build_and_train_model(X_train, y_train)
    
    # Evaluate model
    evaluate_model(vectorizer, model, X_test, y_test)
    
    # Save model and vectorizer
    save_model_and_vectorizer(model, vectorizer, MODEL_PATH, VECTORIZER_PATH)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)


if __name__ == '__main__':
    main()
