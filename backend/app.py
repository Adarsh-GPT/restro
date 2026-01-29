"""
Flask REST API for Restaurant Sentiment Analysis
==================================================
Provides endpoints for sentiment prediction on restaurant reviews.
Uses trained Naive Bayes model with TF-IDF vectorization.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
import json
from preprocess import preprocess_text

# Initialize Flask app
app = Flask(__name__)

# Configure CORS with explicit settings
CORS(app, 
     resources={r"/api/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

# Also enable CORS for root paths
@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Model and vectorizer paths
MODEL_PATH = 'sentiment_model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

# Global variables to store model and vectorizer
model = None
vectorizer = None


def load_model_and_vectorizer():
    """
    Load trained model and vectorizer from pickle files.
    
    Returns:
        tuple: (model, vectorizer) or (None, None) if files not found
    """
    global model, vectorizer
    
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print(f"Warning: Model files not found.")
        print(f"  Expected: {MODEL_PATH}")
        print(f"  Expected: {VECTORIZER_PATH}")
        print("Please run train_model.py first to train the model.")
        return None, None
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print(f"Model loaded from {MODEL_PATH}")
        
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        print(f"Vectorizer loaded from {VECTORIZER_PATH}")
        
        return model, vectorizer
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None, None


@app.route('/', methods=['GET'])
def home():
    """
    Home endpoint - provides API information.
    
    Returns:
        JSON: API information and available endpoints
    """
    return jsonify({
        'message': 'Restaurant Sentiment Analysis API',
        'version': '1.0',
        'status': 'Running',
        'endpoints': {
            'POST /predict': 'Predict sentiment for a review',
            'GET /health': 'Health check'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON: Health status
    """
    model_loaded = model is not None and vectorizer is not None
    return jsonify({
        'status': 'healthy' if model_loaded else 'unhealthy',
        'model_loaded': model_loaded,
        'message': 'Model is ready for predictions' if model_loaded else 'Model not loaded. Please train first.'
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict sentiment for a given review text.
    
    Expected JSON input:
    {
        "review": "review text here"
    }
    
    Returns:
        JSON: {
            "review": "processed review",
            "sentiment": "Positive" or "Negative",
            "confidence": confidence_score,
            "raw_prediction": 0 or 1
        }
    """
    # Check if model is loaded
    if model is None or vectorizer is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'Please train the model first using train_model.py'
        }), 503
    
    # Check if request has JSON data
    if not request.is_json:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Request must be JSON with "review" field'
        }), 400
    
    data = request.get_json()
    
    # Validate input
    if 'review' not in data or not isinstance(data['review'], str):
        return jsonify({
            'error': 'Invalid input',
            'message': 'Please provide a "review" field with text'
        }), 400
    
    review_text = data['review'].strip()
    
    if len(review_text) == 0:
        return jsonify({
            'error': 'Empty review',
            'message': 'Review text cannot be empty'
        }), 400
    
    try:
        # Preprocess the review
        processed_review = preprocess_text(review_text)
        
        # Vectorize the review
        review_vectorized = vectorizer.transform([processed_review])
        
        # Make prediction
        prediction = model.predict(review_vectorized)[0]
        
        # Get prediction probability
        probabilities = model.predict_proba(review_vectorized)[0]
        confidence = float(max(probabilities))
        
        # Convert to sentiment label
        sentiment = 'Positive' if prediction == 1 else 'Negative'
        
        return jsonify({
            'original_review': review_text,
            'processed_review': processed_review,
            'sentiment': sentiment,
            'confidence': round(confidence, 4),
            'raw_prediction': int(prediction),
            'probabilities': {
                'negative': round(float(probabilities[0]), 4),
                'positive': round(float(probabilities[1]), 4)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Prediction error',
            'message': str(e)
        }), 500


@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    """
    Predict sentiment for multiple reviews at once.
    
    Expected JSON input:
    {
        "reviews": ["review1", "review2", ...]
    }
    
    Returns:
        JSON: Array of predictions
    """
    # Check if model is loaded
    if model is None or vectorizer is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'Please train the model first'
        }), 503
    
    # Check if request has JSON data
    if not request.is_json:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Request must be JSON with "reviews" field'
        }), 400
    
    data = request.get_json()
    
    # Validate input
    if 'reviews' not in data or not isinstance(data['reviews'], list):
        return jsonify({
            'error': 'Invalid input',
            'message': 'Please provide a "reviews" field with list of texts'
        }), 400
    
    reviews = data['reviews']
    
    if len(reviews) == 0:
        return jsonify({
            'error': 'Empty reviews list',
            'message': 'Please provide at least one review'
        }), 400
    
    try:
        predictions = []
        
        for review_text in reviews:
            if not isinstance(review_text, str) or len(review_text.strip()) == 0:
                continue
            
            # Preprocess the review
            processed_review = preprocess_text(review_text)
            
            # Vectorize and predict
            review_vectorized = vectorizer.transform([processed_review])
            prediction = model.predict(review_vectorized)[0]
            probabilities = model.predict_proba(review_vectorized)[0]
            confidence = float(max(probabilities))
            sentiment = 'Positive' if prediction == 1 else 'Negative'
            
            predictions.append({
                'original_review': review_text,
                'sentiment': sentiment,
                'confidence': round(confidence, 4),
                'raw_prediction': int(prediction)
            })
        
        return jsonify({
            'count': len(predictions),
            'predictions': predictions
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': 'Batch prediction error',
            'message': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An error occurred on the server'
    }), 500


if __name__ == '__main__':
    print("="*60)
    print("RESTAURANT SENTIMENT ANALYSIS - FLASK API")
    print("="*60)
    
    # Load model and vectorizer
    print("\nLoading model and vectorizer...")
    model, vectorizer = load_model_and_vectorizer()
    
    if model is None or vectorizer is None:
        print("\nWarning: Starting server without trained model.")
        print("The /predict endpoint will return error until model is trained.")
    else:
        print("\nModel loaded successfully!")
    
    # Start Flask server
    print("\nStarting Flask server on http://localhost:5000")
    print("Press Ctrl+C to stop the server.\n")
    
    app.run(debug=True, host='localhost', port=5000)
