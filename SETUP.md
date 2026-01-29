# Setup Instructions - Restaurant Sentiment Analysis

## 📂 Project Structure Setup

Your project structure should look like this:

```
restaurant-sentiment-analysis/
├── backend/
│   ├── app.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── .env
│   ├── data/
│   │   └── Yelp Restaurant Reviews.csv  ← COPY CSV HERE
│   ├── sentiment_model.pkl  (created after training)
│   └── vectorizer.pkl       (created after training)
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   └── package.json
├── README.md
├── QUICKSTART.md
├── .gitignore
└── Yelp Restaurant Reviews.csv  ← COPY FROM HERE
```

---

## 📋 Dataset Setup

### Important: Copy Dataset to Data Folder

The `Yelp Restaurant Reviews.csv` file is currently in the root directory. You need to copy it to `backend/data/` folder for the training script to find it.

**On Windows (PowerShell):**
```powershell
Copy-Item "Yelp Restaurant Reviews.csv" -Destination "backend\data\"
```

**On Windows (Command Prompt):**
```cmd
copy "Yelp Restaurant Reviews.csv" "backend\data\"
```

**On macOS/Linux:**
```bash
cp "Yelp Restaurant Reviews.csv" backend/data/
```

---

## ✅ Pre-Flight Checklist

Before running the application:

- [ ] `Yelp Restaurant Reviews.csv` is copied to `backend/data/` folder
- [ ] CSV file has at least 2 columns: text/review and stars/rating
- [ ] All Python files are in `backend/` folder
- [ ] All React files are in `frontend/src/` folder
- [ ] `requirements.txt` is in `backend/` folder
- [ ] `package.json` is in `frontend/` folder
- [ ] You have Python 3.8+ installed
- [ ] You have Node.js 14+ and npm installed

**Check Python:**
```bash
python --version
```

**Check Node:**
```bash
node --version
npm --version
```

---

## 🚀 Installation Steps

### Step 1: Backend Setup (Python)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
# From backend directory with venv activated
python train_model.py

# Wait for training to complete (5-15 minutes depending on dataset size)
# Two files will be created:
#   - sentiment_model.pkl
#   - vectorizer.pkl
```

### Step 3: Start Flask Backend

```bash
# From backend directory with venv activated
python app.py

# You should see:
# Starting Flask server on http://localhost:5000
# Keep this terminal open
```

### Step 4: Frontend Setup (Node/React)

```bash
# Open a NEW terminal/PowerShell
# Navigate to frontend
cd frontend

# Install npm dependencies
npm install

# Start React development server
npm start

# Browser will open automatically at http://localhost:3000
```

---

## 🧪 Testing the Setup

### Test Backend

**Option 1: Using PowerShell (cURL equivalent)**

```powershell
$body = @{
    review = "The food was amazing! Great service and friendly staff."
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/predict" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

**Option 2: Using Browser**

Open http://localhost:5000/health in your browser
You should see: `{"status": "healthy", "model_loaded": true, ...}`

### Test Frontend

1. Open http://localhost:3000 in browser
2. You should see the sentiment analyzer UI
3. Enter a sample review
4. Click "Predict Sentiment"
5. Results should appear with confidence score

---

## 🐛 Troubleshooting

### Python Virtual Environment Issues

**Problem:** `python -m venv venv` doesn't work

**Solutions:**
```bash
# Option 1: Use python3
python3 -m venv venv

# Option 2: Use pip's virtualenv
pip install virtualenv
virtualenv venv
```

### Dependencies Installation Fails

**Problem:** `pip install -r requirements.txt` errors

**Solutions:**
```bash
# Update pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install each package separately
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install scikit-learn==1.3.0
pip install nltk==3.8.1
```

### NLTK Data Download Fails

**Problem:** "punkt" or "stopwords" not found errors

**Solution:** Download manually in Python terminal:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Model Training Fails

**Problem:** "Dataset not found" or file reading errors

**Checklist:**
- [ ] CSV file is in `backend/data/` folder
- [ ] CSV filename matches exactly: `Yelp Restaurant Reviews.csv`
- [ ] CSV has proper columns (check header row)
- [ ] CSV is not corrupted
- [ ] Have permission to read the file

### Flask Port Already in Use

**Problem:** "Address already in use" on port 5000

**Solutions:**
```powershell
# Option 1: Stop existing process
Stop-Process -Name python

# Option 2: Use different port (edit app.py last line):
app.run(debug=True, host='localhost', port=5001)
```

### React npm Issues

**Problem:** npm install fails

**Solutions:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## 📊 Expected File Sizes

After completing setup, your folders should contain:

- `backend/data/Yelp Restaurant Reviews.csv` - ~10-50 MB (original dataset)
- `backend/sentiment_model.pkl` - ~1-5 MB (trained model)
- `backend/vectorizer.pkl` - ~2-10 MB (TF-IDF vectorizer)
- `frontend/node_modules/` - ~300-400 MB (after npm install)

---

## 🎯 Quick Reference

### Common Commands

**Backend (Python):**
```bash
cd backend
.\venv\Scripts\Activate.ps1         # Windows activation
pip install -r requirements.txt      # Install dependencies
python train_model.py                # Train model
python app.py                        # Run Flask
deactivate                          # Exit virtual environment
```

**Frontend (Node):**
```bash
cd frontend
npm install                         # Install dependencies
npm start                          # Start development server
npm build                          # Build for production
npm test                           # Run tests
```

---

## ✨ Next Steps

1. Follow the Quick Start Guide (QUICKSTART.md)
2. Read the main README.md for detailed documentation
3. Test with sample reviews
4. Explore the code to understand NLP concepts
5. Modify and experiment as needed

---

**All set! Your full-stack sentiment analyzer is ready to use.** 🚀

For issues, refer to the Troubleshooting section above or check README.md.
