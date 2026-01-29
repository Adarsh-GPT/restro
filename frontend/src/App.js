import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [review, setReview] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [probabilities, setProbabilities] = useState(null);

  const API_BASE_URL = 'http://localhost:5000';

  const handlePredict = async (e) => {
    e.preventDefault();

    if (review.trim().length === 0) {
      setError('Please enter a review text');
      return;
    }

    setLoading(true);
    setError(null);
    setSentiment(null);
    setConfidence(null);
    setProbabilities(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, {
        review: review,
      });

      const data = response.data;
      setSentiment(data.sentiment);
      setConfidence(data.confidence);
      setProbabilities(data.probabilities);
    } catch (err) {
      if (err.response) {
        setError(
          err.response.data.message ||
          'Error connecting to backend. Make sure the Flask server is running on localhost:5000'
        );
      } else if (err.message === 'Network Error') {
        setError('Network Error: Cannot connect to backend. Make sure Flask server is running on http://localhost:5000');
      } else {
        setError(err.message || 'An error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setReview('');
    setSentiment(null);
    setConfidence(null);
    setProbabilities(null);
    setError(null);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🍴 Restaurant Sentiment Analyzer</h1>
        <p>Analyze the sentiment of Yelp-style restaurant reviews</p>
      </header>

      <main className="main-content">
        <div className="card input-card">
          <form onSubmit={handlePredict}>
            <div className="form-group">
              <label htmlFor="review">Enter Your Review:</label>
              <textarea
                id="review"
                value={review}
                onChange={(e) => setReview(e.target.value)}
                placeholder="Write your honest restaurant review here... (e.g., 'The food was amazing! Great service and friendly staff. Highly recommend!')"
                rows="8"
                disabled={loading}
              />
            </div>

            <div className="button-group">
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Analyzing...' : 'Predict Sentiment'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={handleClear}
                disabled={loading}
              >
                Clear
              </button>
            </div>
          </form>
        </div>

        {error && (
          <div className="card error-card">
            <h3>⚠️ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {sentiment && (
          <div className={`card result-card ${sentiment.toLowerCase()}`}>
            <h2>Prediction Result</h2>
            
            <div className="sentiment-display">
              <div className={`sentiment-badge ${sentiment.toLowerCase()}`}>
                {sentiment === 'Positive' ? '😊 POSITIVE' : '😞 NEGATIVE'}
              </div>
            </div>

            <div className="metrics">
              <div className="metric">
                <span className="metric-label">Confidence Score:</span>
                <span className="metric-value">{(confidence * 100).toFixed(2)}%</span>
              </div>

              {probabilities && (
                <>
                  <div className="probability-bar">
                    <label>Negative Probability</label>
                    <div className="bar-container">
                      <div 
                        className="bar negative-bar"
                        style={{ width: `${probabilities.negative * 100}%` }}
                      >
                        {(probabilities.negative * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>

                  <div className="probability-bar">
                    <label>Positive Probability</label>
                    <div className="bar-container">
                      <div 
                        className="bar positive-bar"
                        style={{ width: `${probabilities.positive * 100}%` }}
                      >
                        {(probabilities.positive * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>

            <button 
              className="btn btn-secondary"
              onClick={handleClear}
            >
              Analyze Another Review
            </button>
          </div>
        )}

        {loading && (
          <div className="card loading-card">
            <p>Analyzing your review... This may take a moment.</p>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Restaurant Sentiment Analysis | Yelp Reviews Dataset | Naive Bayes Classifier</p>
      </footer>
    </div>
  );
}

export default App;
