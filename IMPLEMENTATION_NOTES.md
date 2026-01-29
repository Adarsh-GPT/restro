# Restaurant Sentiment Analysis - Implementation Notes

## 📋 Important Notes for Project Setup

### Dataset File
The dataset `Yelp Restaurant Reviews.csv` should be in **`backend/data/`** directory.

**Expected CSV Format:**
```
text,stars
"Great food and excellent service!",5
"Terrible experience. Very disappointed.",1
"Decent place, nothing special.",3
"Absolutely amazing! Will come back!",5
"Worst restaurant ever.",2
```

**Required Columns:**
- **text** (or: review, comment, content) - Customer review text
- **stars** (or: rating, score, review_rating) - Numeric rating (1-5)

The script will automatically detect these columns regardless of name variation.

### Data Processing in train_model.py
1. Reviews with rating 4-5 → **Positive (1)**
2. Reviews with rating 1-2 → **Negative (0)**
3. Reviews with rating 3 → **Ignored** (neutral, excluded from training)

### Preprocessing Steps (in order)
1. HTML tag removal
2. URL removal  
3. Lowercase conversion
4. Punctuation & number removal
5. Tokenization
6. Stopword removal
7. Lemmatization
8. Text reconstruction

---

## 🔧 Environment Configuration

### Python Virtual Environment
```bash
# Create
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate (any OS)
deactivate
```

### Required Python Version
- Minimum: Python 3.8
- Recommended: Python 3.9 or 3.10

### Check Installation
```bash
python --version        # Should be 3.8+
pip --version          # Should exist
pip list               # Shows installed packages
```

---

## 🚀 Model Training Guide

### Before Training
- CSV file in `backend/data/` folder
- Python venv activated
- Dependencies installed with `pip install -r requirements.txt`

### Training Command
```bash
python train_model.py
```

### Training Stages (in order)
1. **Load Dataset** - Reads CSV file
2. **Create Labels** - Converts ratings to sentiment
3. **Preprocess** - Cleans all review text
4. **Split Data** - 80% train, 20% test
5. **Vectorize** - Converts text to TF-IDF features
6. **Train Model** - Fits Naive Bayes classifier
7. **Evaluate** - Tests model performance
8. **Save** - Exports `sentiment_model.pkl` and `vectorizer.pkl`

### Expected Output Files
- `sentiment_model.pkl` (~1-5 MB)
- `vectorizer.pkl` (~2-10 MB)

### Expected Performance Metrics
- Accuracy: 75-85%
- Precision: 75-85%
- Recall: 75-85%
- F1-Score: 0.75-0.85

### Training Time
- Small dataset (< 5000 rows): 2-5 minutes
- Medium dataset (5000-20000 rows): 5-15 minutes
- Large dataset (> 20000 rows): 15-30 minutes

---

## 🌐 Flask API Guide

### Starting the Server
```bash
# Must be in backend directory with venv activated
python app.py

# Expected output:
# ============================================================
# RESTAURANT SENTIMENT ANALYSIS - FLASK API
# ============================================================
# Loading model and vectorizer...
# Model loaded from sentiment_model.pkl
# Vectorizer loaded from vectorizer.pkl
# Model loaded successfully!
# Starting Flask server on http://localhost:5000
# Press Ctrl+C to stop the server.
```

### API Base URL
```
http://localhost:5000
```

### Available Endpoints

#### GET /
Info about the API
```bash
curl http://localhost:5000/
```

#### GET /health
Check if model is loaded
```bash
curl http://localhost:5000/health
```

#### POST /predict
Predict sentiment for one review
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"review":"Amazing food!"}'
```

#### POST /batch_predict
Predict sentiment for multiple reviews
```bash
curl -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{"reviews":["Good food","Bad service"]}'
```

### Expected Response Format
```json
{
  "original_review": "The food was great!",
  "processed_review": "food great",
  "sentiment": "Positive",
  "confidence": 0.8765,
  "raw_prediction": 1,
  "probabilities": {
    "negative": 0.1235,
    "positive": 0.8765
  }
}
```

---

## ⚛️ React Frontend Guide

### Starting the Development Server
```bash
# From frontend directory
npm start

# Expected: Browser opens to http://localhost:3000
# Watch mode: Changes auto-refresh in browser
```

### Build for Production
```bash
# From frontend directory
npm build

# Creates optimized production build in build/ folder
```

### Component Flow
1. User enters review in textarea
2. Click "Predict Sentiment" button
3. App sends POST to `http://localhost:5000/predict`
4. Flask processes and returns prediction
5. App displays result with confidence and probability bars

### Environment Variables
Create `.env` in frontend folder (optional):
```
REACT_APP_API_URL=http://localhost:5000
```

---

## 🔗 Communication Between Frontend and Backend

### How It Works
1. React sends HTTP POST request with review text
2. Flask receives request, preprocesses review
3. Model makes prediction
4. Flask returns JSON response
5. React displays results

### CORS Configuration
- Enabled in Flask: `CORS(app)`
- Frontend proxy: Configured in `package.json`
- No authentication required (development mode)

### Troubleshooting Connection Issues

**Issue**: "Cannot connect to backend"
**Solution**: 
1. Ensure Flask running on port 5000
2. Check `http://localhost:5000/health` in browser
3. Look for CORS errors in browser console
4. Verify firewall allows port 5000

---

## 🧪 Testing the System

### Test 1: Model Training
```bash
cd backend
python train_model.py
# Check for: "TRAINING COMPLETE!" message
# Check for: sentiment_model.pkl and vectorizer.pkl files
```

### Test 2: Flask API
```bash
# In browser
http://localhost:5000/health

# Expected: {"status": "healthy", "model_loaded": true}
```

### Test 3: Prediction
```powershell
# In PowerShell
$body = @{review="Best restaurant ever!"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:5000/predict -Method Post -Body $body -Headers @{"Content-Type"="application/json"}

# Expected: JSON with sentiment "Positive" and high confidence
```

### Test 4: React Frontend
1. Open http://localhost:3000
2. Type: "Great food!"
3. Click "Predict Sentiment"
4. See result: "Positive" with green badge

---

## 📦 Dependency Management

### Python Packages (backend/requirements.txt)
```
Flask==2.3.3              # Web framework
Flask-CORS==4.0.0        # CORS support
pandas==2.0.3            # Data manipulation
numpy==1.24.3            # Numerical computing
scikit-learn==1.3.0      # Machine learning
nltk==3.8.1              # NLP library
```

### Node Packages (frontend/package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",        // UI framework
    "react-dom": "^18.2.0",    // DOM rendering
    "axios": "^1.4.0",         // HTTP client
    "react-scripts": "5.0.1"   // Build tools
  }
}
```

---

## 🔐 Security Notes

### Development Mode (Current Setup)
- Debug mode enabled (Flask)
- CORS allows all origins
- No authentication
- Suitable for: Learning, development, testing

### Production Deployment
- Disable debug mode
- Restrict CORS origins
- Add authentication if needed
- Use production server (gunicorn, etc.)
- Add HTTPS/SSL
- Validate all inputs

---

## 📊 Model Parameters

### TF-IDF Vectorizer
```python
TfidfVectorizer(
    max_features=5000,      # Keep top 5000 terms
    min_df=2,               # Term must appear in 2+ docs
    max_df=0.95,            # Remove if in 95%+ of docs
    ngram_range=(1, 2),     # Use 1-2 word sequences
    stop_words='english'    # Remove English stopwords
)
```

### Naive Bayes Classifier
```python
MultinomialNB()            # Default parameters
```

### Train-Test Split
```python
train_test_split(
    X, y,
    test_size=0.2,         # 20% for testing
    random_state=42,       # Reproducible results
    stratify=y             # Balanced split
)
```

---

## 🎯 Performance Optimization Tips

### Model Training
- Reduce `max_features` if memory limited
- Increase `min_df` to ignore rare words
- Use subset of data for testing

### API Performance
- Add caching for frequent predictions
- Use batch predictions for multiple reviews
- Optimize preprocessing pipeline

### Frontend Performance
- Minimize re-renders with React.memo
- Lazy load components
- Cache API responses

---

## 📝 Code Structure

### Backend Organization
```
backend/
├── app.py               # API endpoints (100+ lines)
├── train_model.py       # Training pipeline (200+ lines)
├── preprocess.py        # Text cleaning (150+ lines)
├── requirements.txt     # Dependencies
└── .env                 # Configuration
```

### Frontend Organization
```
frontend/
├── src/
│   ├── App.js           # Main component (150+ lines)
│   ├── App.css          # Styling (350+ lines)
│   ├── index.js         # Entry point (10 lines)
│   └── index.css        # Global styles (50 lines)
└── public/
    └── index.html       # HTML template
```

---

## 🐛 Common Error Messages

### "FileNotFoundError: Yelp Restaurant Reviews.csv"
**Cause**: CSV not in `backend/data/` folder
**Fix**: Copy CSV to backend/data/

### "ModuleNotFoundError: No module named 'flask'"
**Cause**: Dependencies not installed
**Fix**: Run `pip install -r requirements.txt`

### "Model not loaded" error
**Cause**: Model files not found
**Fix**: Run `python train_model.py` first

### "Cannot GET http://localhost:3000"
**Cause**: React not running
**Fix**: Run `npm start` in frontend folder

### "Connection refused localhost:5000"
**Cause**: Flask not running
**Fix**: Run `python app.py` in backend folder

---

## ✨ Project Highlights

✓ **Complete NLP Pipeline** - 8-step preprocessing
✓ **ML Model** - Naive Bayes with TF-IDF
✓ **REST API** - Production-ready Flask endpoints
✓ **React UI** - Modern responsive frontend
✓ **Documentation** - 500+ lines of guides
✓ **Error Handling** - Comprehensive checks
✓ **Code Quality** - Professional standards
✓ **Academic Ready** - Suitable for TY projects

---

## 📞 Quick Reference

### First Time?
1. Read: SETUP.md or QUICKSTART.md
2. Copy: CSV to backend/data/
3. Run: python train_model.py
4. Run: python app.py
5. Run: npm start

### Familiar Already?
1. `cd backend && python train_model.py`
2. `python app.py`
3. `cd ../frontend && npm start`

### Just Testing?
1. Use sample reviews in QUICKSTART.md
2. Watch terminal output for debugging
3. Check browser console for errors

---

Last Updated: January 9, 2026
Status: Ready for Use ✅

