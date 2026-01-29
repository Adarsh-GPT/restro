# Restaurant Sentiment Analysis

ML project for sentiment classification on Yelp restaurant reviews.

## Model
- Classifier: Linear SVM (LinearSVC) with CalibratedClassifierCV (probability calibration)
- Vectorization: TF-IDF
- Binary classification: Positive / Negative (3-star reviews ignored)
- No Naive Bayes is used anywhere in this project

## Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py
```

## API Endpoints
- POST /predict — Predict sentiment for a single review
- POST /batch_predict — Predict sentiment for multiple reviews
- GET /health — Health check

