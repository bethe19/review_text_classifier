from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
from pathlib import Path
try:
    from api.utils import preprocess_text
except ImportError:
    from utils import preprocess_text

app = FastAPI(
    title="Sentiment Analysis API",
    description="REST API for restaurant review sentiment analysis using MultinomialNB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

project_root = Path(__file__).parent.parent
model_path = project_root / "models" / "sentiment_model.pkl"
vectorizer_path = project_root / "models" / "count_vectorizer.pkl"

model = None
vectorizer = None

def load_model():
    global model, vectorizer
    
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Please run training/train_model.py first."
        )
    
    if not vectorizer_path.exists():
        raise FileNotFoundError(
            f"Vectorizer not found at {vectorizer_path}. Please run training/train_model.py first."
        )
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    print("Model and vectorizer loaded successfully!")

@app.on_event("startup")
async def startup_event():
    load_model()

class ReviewRequest(BaseModel):
    review: str

class SentimentResponse(BaseModel):
    review: str
    sentiment: str
    confidence: float
    prediction: int

@app.get("/")
async def root():
    return {
        "message": "Sentiment Analysis API",
        "status": "running",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None
    }

@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(request: ReviewRequest):
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Please ensure the model files exist."
        )
    
    if not request.review or not request.review.strip():
        raise HTTPException(
            status_code=400,
            detail="Review text cannot be empty"
        )
    
    try:
        processed_review = preprocess_text(request.review)
        review_vector = vectorizer.transform([processed_review]).toarray()
        prediction = model.predict(review_vector)[0]
        probabilities = model.predict_proba(review_vector)[0]
        confidence = float(max(probabilities))
        sentiment = "positive" if prediction == 1 else "negative"
        
        return SentimentResponse(
            review=request.review,
            sentiment=sentiment,
            confidence=confidence,
            prediction=int(prediction)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during prediction: {str(e)}"
        )

@app.post("/predict/batch")
async def predict_batch(reviews: list[str]):
    if model is None or vectorizer is None:
        raise HTTPException(
            status_code=500,
            detail="Model not loaded. Please ensure the model files exist."
        )
    
    if not reviews:
        raise HTTPException(
            status_code=400,
            detail="Reviews list cannot be empty"
        )
    
    try:
        results = []
        
        for review_text in reviews:
            if not review_text or not review_text.strip():
                results.append({
                    "review": review_text,
                    "error": "Empty review text"
                })
                continue
            
            processed_review = preprocess_text(review_text)
            review_vector = vectorizer.transform([processed_review]).toarray()
            prediction = model.predict(review_vector)[0]
            probabilities = model.predict_proba(review_vector)[0]
            confidence = float(max(probabilities))
            sentiment = "positive" if prediction == 1 else "negative"
            
            results.append({
                "review": review_text,
                "sentiment": sentiment,
                "confidence": confidence,
                "prediction": int(prediction)
            })
        
        return {"results": results, "total": len(results)}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during batch prediction: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

