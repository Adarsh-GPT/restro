"""
Text Preprocessing Module for Sentiment Analysis
==================================================
Handles cleaning and preprocessing of restaurant reviews for both training and prediction.
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()

# Important: Remove negation words from stopwords for sentiment analysis
# Words like 'not', 'no', 'nor', 'neither' are critical for detecting negative sentiment
negation_words = {'not', 'no', 'nor', 'neither', 'never', 'nobody', 'nothing', 'nowhere', 
                  'noone', 'haven', 'hasn', 'aren', 'wasn', 'weren', 'won', 'wouldn', 
                  'shan', 'shouldn', 'couldn', 'mustn', 'mightn', 'don', 'didn', 'doesn',
                  'isn', 'ain', 'doesn'}

# Get English stopwords and remove negation words
all_stopwords = set(stopwords.words('english'))
stop_words = all_stopwords - negation_words


def remove_html_tags(text):
    """
    Remove HTML tags from text.
    
    Args:
        text (str): Text containing potential HTML tags
        
    Returns:
        str: Text without HTML tags
    """
    html_pattern = re.compile(r'<.*?>')
    return html_pattern.sub(r'', text)


def remove_urls(text):
    """
    Remove URLs from text.
    
    Args:
        text (str): Text containing potential URLs
        
    Returns:
        str: Text without URLs
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def convert_to_lowercase(text):
    """
    Convert text to lowercase.
    
    Args:
        text (str): Text to convert
        
    Returns:
        str: Lowercase text
    """
    return text.lower()


def remove_punctuation_numbers(text):
    """
    Remove punctuation and numbers from text.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Text without punctuation and numbers
    """
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def tokenize_text(text):
    """
    Tokenize text into words.
    
    Args:
        text (str): Text to tokenize
        
    Returns:
        list: List of tokens (words)
    """
    return nltk.word_tokenize(text)


def remove_stopwords(tokens):
    """
    Remove stopwords from tokenized text.
    
    Args:
        tokens (list): List of tokens
        
    Returns:
        list: Tokens with stopwords removed
    """
    return [token for token in tokens if token not in stop_words]


def lemmatize_tokens(tokens):
    """
    Apply lemmatization to tokens.
    
    Args:
        tokens (list): List of tokens
        
    Returns:
        list: Lemmatized tokens
    """
    return [lemmatizer.lemmatize(token) for token in tokens]


def preprocess_text(text):
    """
    Complete preprocessing pipeline for text.
    
    Steps:
    1. Remove HTML tags
    2. Remove URLs
    3. Convert to lowercase
    4. Remove punctuation and numbers
    5. Tokenize
    6. Remove stopwords
    7. Lemmatize
    8. Reconstruct cleaned text
    
    Args:
        text (str): Raw text to preprocess
        
    Returns:
        str: Cleaned and preprocessed text
    """
    # Remove HTML tags
    text = remove_html_tags(text)
    
    # Remove URLs
    text = remove_urls(text)
    
    # Convert to lowercase
    text = convert_to_lowercase(text)
    
    # Remove punctuation and numbers
    text = remove_punctuation_numbers(text)
    
    # Extra spaces cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize
    tokens = tokenize_text(text)
    
    # Remove stopwords
    tokens = remove_stopwords(tokens)
    
    # Lemmatize
    tokens = lemmatize_tokens(tokens)
    
    # Reconstruct cleaned text
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text
