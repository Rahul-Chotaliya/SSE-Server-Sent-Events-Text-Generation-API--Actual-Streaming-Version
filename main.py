from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel


app = FastAPI()

#loading Model
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

class TextRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: TextRequest):
    result = classifier(request.text)
    return {"sentiment": result[0]['label'], "confidence": result[0]['score']}
