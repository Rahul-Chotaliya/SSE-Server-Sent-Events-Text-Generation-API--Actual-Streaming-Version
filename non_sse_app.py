from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

app = FastAPI()

#loading Model
generator = pipeline("text-generation", model="gpt2",device=1)

class TextRequest(BaseModel):
    text: str
    

@app.post("/predict")
def predict(request: TextRequest):
    result = generator(request.text, max_length=50, num_return_sequences=1)
    return {"generated_text": result[0]['generated_text']}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)