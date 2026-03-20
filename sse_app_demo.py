from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, HTMLResponse
from transformers import pipeline, TextIteratorStreamer
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread    
import asyncio
import json

app = FastAPI(title="SSE Text Generation API")
MODEL_NAME = "gpt2"

#Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)   

#loading text generation model
print(f"Loading model {MODEL_NAME}...")
text_generator = pipeline("text-generation", model=MODEL_NAME, device=1)
print("Model loaded successfully.")

def sse_format(data:dict,event:str=None) -> str:
    """Format for SSE Data"""
    
    message = ""
    if event:
        message += f"event: {event}\n"
    message += f"data: {json.dumps(data)}\n\n"
    return message  

@app.post("/generate")
async def generate_stream(
    prompt: str = Query(..., description="Input text prompt for generation"),
    max_length: int = Query(50, description="Maximum length of generated text")
):
    "Stream Text endpoints works with Postmans="
    async def generate():
        yield sse_format({"status":"Generating text...","prompt": prompt, "max_length": max_length}, event="start")
        
        #create streamer
        streamer = TextIteratorStreamer(text_generator.tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        #Generated Streming Parameters
        generation_kwargs = dict(
            max_new_tokens=max_length,
            do_sample=True,
            streamer=streamer,
            temperature=0.7)
        
        thread  = Thread(target=text_generator.model.generate, kwargs={**text_generator.tokenizer(prompt, return_tensors="pt",padding=True), **generation_kwargs})
        thread.start()
        
        for generated_text in streamer:
            yield sse_format({"generated_text": generated_text}, event="generated")
    
    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    print("Starting SSE Text Generation API on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)