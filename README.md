# Review Text Classifier

A sentiment analysis project that classifies restaurant reviews as positive or negative using machine learning and natural language processing techniques.

## Description

This project implements a text classification model that can analyze restaurant reviews and determine their sentiment polarity (positive or negative). It uses NLP techniques for text preprocessing and machine learning algorithms for classification.

## How to Run

### Prerequisites
- Python 3.8+
- pip
- Jupyter Notebook (optional, for running the analysis notebook)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/bethe19/review_text_classifier.git
cd review_text_classifier
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. To start the API server:
```bash
python run_api.py
```

The API will be available at `http://localhost:5000`

2. To run the Jupyter notebook for analysis:
```bash
jupyter notebook nlp-sentimental-analysis.ipynb
```

3. To run tests:
```bash
python test_api.py
```

## Project Structure

- `api/` - API endpoints for predictions
- `frontend/` - Web interface
- `models/` - Trained model files
- `training/` - Training data and scripts
- `Restaurant_Reviews.tsv` - Training dataset
- `nlp-sentimental-analysis.ipynb` - Analysis notebook
- `run_api.py` - Entry point for the API server
- `test_api.py` - Test cases for the API
