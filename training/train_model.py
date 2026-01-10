import pandas as pd
import re
import nltk
import pickle
import json
import datetime
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, 
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def preprocess_text(text):
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    review = [ps.stem(word) for word in review if word not in set(all_stopwords)]
    review = ' '.join(review)
    return review

def train_model():
    project_root = Path(__file__).parent.parent
    
    dataset_path = project_root / "Restaurant_Reviews.tsv"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    
    print("Loading dataset...")
    dataset = pd.read_csv(dataset_path, delimiter='\t', quoting=3)
    
    print("Preprocessing texts...")
    corpus = []
    for i in range(len(dataset)):
        review = preprocess_text(dataset['Review'][i])
        corpus.append(review)
    
    print("Creating TF-IDF Vectorizer with n-grams...")
    cv = TfidfVectorizer(max_features=1500, ngram_range=(1, 2))
    X = cv.fit_transform(corpus).toarray()
    Y = dataset.iloc[:, -1].values
    
    print("Splitting dataset...")
    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.25, random_state=0,         stratify=Y
    )
    
    print("Performing hyperparameter tuning...")
    param_grid = {
        'alpha': [0.1, 0.5, 1.0, 2.0]
    }
    grid_search = GridSearchCV(
        MultinomialNB(), 
        param_grid, 
        cv=StratifiedKFold(n_splits=5), 
        scoring='f1',
        n_jobs=-1
    )
    grid_search.fit(x_train, y_train)
    model = grid_search.best_estimator_
    
    print(f"Best alpha parameter: {grid_search.best_params_['alpha']}")
    
    print("Performing cross-validation...")
    cv_scores = cross_val_score(
        model, X, Y, 
        cv=StratifiedKFold(n_splits=5), 
        scoring='f1'
    )
    print(f"Cross-validation F1 scores: {cv_scores}")
    print(f"Mean CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    print("\nEvaluating model on test set...")
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"\n=== Model Performance ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    print(f"\nConfusion Matrix:\n{cm}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    models_dir = project_root / "models"
    models_dir.mkdir(exist_ok=True)
    
    print("\nSaving model and vectorizer...")
    model_path = models_dir / "sentiment_model.pkl"
    vectorizer_path = models_dir / "count_vectorizer.pkl"
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(cv, f)
    
    model_info = {
        'version': '2.0.0',
        'trained_date': datetime.datetime.now().isoformat(),
        'algorithm': 'MultinomialNB',
        'vectorizer': 'TfidfVectorizer',
        'max_features': 1500,
        'ngram_range': [1, 2],
        'best_alpha': grid_search.best_params_['alpha'],
        'metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'cv_f1_mean': float(cv_scores.mean()),
            'cv_f1_std': float(cv_scores.std()),
            'confusion_matrix': cm.tolist()
        }
    }
    
    metrics_path = models_dir / "model_metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"Model saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    print(f"Metrics saved to: {metrics_path}")
    print("\nTraining completed successfully!")

if __name__ == "__main__":
    train_model()

