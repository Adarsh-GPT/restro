# Quick Start Guide - Restaurant Sentiment Analysis

## ⚡ 5-Minute Setup

### Terminal 1: Train Model & Run Backend

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR: source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Train the model (5-10 minutes)
python train_model.py

# Start Flask server
python app.py

# Expected output:
# Starting Flask server on http://localhost:5000
```

### Terminal 2: Start Frontend

```bash
# Navigate to frontend (from new terminal)
cd frontend

# Install Node dependencies
npm install

# Start React server
npm start

# Opens automatically at http://localhost:3000
```

---

## 🎯 What to Expect

### After Training Completes:
- Two new files created: `sentiment_model.pkl` and `vectorizer.pkl`
- Accuracy between 75-85% (depends on dataset quality)
- Ready for predictions

### Flask Server Running:
- API available at http://localhost:5000
- Health check: http://localhost:5000/health
- Test endpoint: POST to http://localhost:5000/predict

### React App Running:
- Frontend available at http://localhost:3000
- Clean UI with input box for reviews
- Click "Predict Sentiment" to get results

---

## 📝 Sample Test Reviews

Try these reviews to test the system:

**Positive Reviews:**
- "Amazing food! Best restaurant in the city. Highly recommend!"
- "Excellent service, beautiful ambiance, delicious dishes. Will definitely come back."
- "The pasta was perfect, staff was friendly. Had a wonderful evening!"

**Negative Reviews:**
- "Terrible experience. Cold food, rude staff, overpriced. Never coming back."
- "Worst restaurant ever. Dirty place, awful service, inedible food."
- "Disappointed. Long wait, mediocre food, terrible customer service."

---

## ✅ Verification Checklist

- [ ] Yelp CSV is in `backend/data/` folder
- [ ] Both terminals are open and running without errors
- [ ] Flask backend console shows "Running on http://localhost:5000"
- [ ] React frontend opened in browser
- [ ] Can type in review text box
- [ ] "Predict Sentiment" button works
- [ ] Results display with sentiment and confidence

---

## 🛑 Common Issues

| Problem | Solution |
|---------|----------|
| "No module named 'flask'" | Run `pip install -r requirements.txt` |
| "Model not found" error | Run `python train_model.py` in backend folder |
| Frontend won't connect | Ensure Flask is running on port 5000 |
| Port 5000 already in use | Kill Flask: `Ctrl+C`, wait 5 seconds, restart |
| Port 3000 already in use | Kill React: `Ctrl+C`, wait 5 seconds, restart |

---

## 📞 Next Steps

1. Modify reviews and observe sentiment changes
2. Check backend logs to understand predictions
3. Review the full README.md for detailed documentation
4. Explore the code in `preprocess.py` to understand NLP
5. Check Flask `app.py` for API implementation

---

Enjoy analyzing restaurant reviews! 🍽️
