from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, HTMLResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline,TextIteratorStreamer
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import asyncio
import json

app = FastAPI(title="SSE Text Generation API- Actual Streaming Version")
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
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)
print("Model loaded successfully.")

def sse_format(data:dict,event:str=None) -> str:
    """Format for SSE Data"""
    
    message = ""
    if event:
        message += f"event: {event}\n"
    message += f"data: {json.dumps(data)}\n\n"
    return message

@app.post("/predict")
async def generate_stream(
    prompt: str = Query(..., description="Input text prompt for generation"),
    max_length: int = Query(50, description="Maximum length of generated text")
):
    "Stream Text endpoints works with Postmans="
    async def generate():
        yield sse_format({"status":"Gnerating text...","prompt": prompt, "max_length": max_length,"note":"Actual Streaming Version"}, event="start")
        
        #Tokenize Inputs
        inputs = tokenizer(prompt, return_tensors="pt",padding=True)
        
        #create streamer
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        #Generated Streming Parameters
        generation_kwargs = dict(
            **inputs,
            max_new_tokens=max_length,
            do_sample=True,
            streamer=streamer,
            temperature=0.7)
        
        thread  = Thread(target=model.generate, kwargs=generation_kwargs)
        thread.start()
        
        token_count = 0
        full_text = prompt
        
        for token_text in streamer:
            if token_text:
                full_text += token_text
                token_count += 1
                yield sse_format({"generated_text": full_text, "token_count": token_count}, event="update")
                await asyncio.sleep(0.1)
        
        thread.join()
        yield sse_format({"generated_text": full_text, "token_count": token_count}, event="done")
        
        return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache", 
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"
                }
            )
        
        
        
@app.get("/",response_class=HTMLResponse)
async def demo_page():
    html_content = """
    <html>
        <head>
            <title>SSE Text Generation Demo</title>
        </head>
        <body>
            <h1>SSE Text Generation API - Actual Streaming Version</h1>
            <p>Use the /predict endpoint to generate text with streaming updates.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)