
# FastAPI AI Demo App

## Overview

This project is a collection of FastAPI microservices that showcase modern Natural Language Processing (NLP) capabilities using Hugging Face Transformers. It provides:

- **Real-time text generation** (with and without streaming)
- **Sentiment analysis** for user-provided text
- **Multiple API endpoints** for different use cases and integration styles
- **Docker support** for easy deployment

The project is ideal for:
- Building AI-powered chatbots or assistants
- Integrating real-time text generation into web apps (via SSE)
- Running batch or single-shot text generation
- Performing sentiment analysis on user input or documents
- Learning and experimenting with FastAPI and Hugging Face models

## In-Depth Features

### 1. Text Generation (GPT-2)
- **Streaming (SSE) Endpoints:**
  - `/sse_app.py` and `/sse_app_demo.py` provide endpoints that stream generated text tokens as they are produced, using Server-Sent Events (SSE). This enables real-time updates for chatbots, live editors, or dashboards.
  - `/predict` (POST, sse_app.py): Accepts a prompt and streams back generated text incrementally.
  - `/generate` (POST, sse_app_demo.py): Similar streaming endpoint for demo purposes.
- **Non-Streaming Endpoint:**
  - `/non_sse_app.py` provides a standard POST endpoint (`/predict`) that returns the full generated text in one response, suitable for batch or synchronous use cases.

### 2. Sentiment Analysis (DistilBERT)
- `/main.py` exposes a `/predict` POST endpoint that takes user text and returns the sentiment label (e.g., POSITIVE/NEGATIVE) and confidence score. Useful for feedback analysis, moderation, or analytics.

### 3. API Design
- All endpoints use FastAPI for automatic OpenAPI docs and easy integration.
- CORS is enabled for all apps, allowing use from browser-based frontends or external services.

### 4. Deployment & Extensibility
- The included Dockerfile allows you to containerize any of the apps for production or cloud deployment.
- Easily swap out models (e.g., use a different Hugging Face model) by changing the model name in the code.

### 5. Example Use Cases
- **Live AI writing assistant**: Use the SSE endpoints to power a collaborative or interactive writing tool.
- **Chatbot backend**: Integrate the text generation API with a chat UI for real-time conversations.
- **Feedback analysis**: Use the sentiment analysis endpoint to process and score user feedback or social media posts.

---

## Features

- **Text Generation (Streaming & Non-Streaming):**
  - `/sse_app.py`: FastAPI app with Server-Sent Events (SSE) for real-time text generation using GPT-2.
  - `/sse_app_demo.py`: Alternate SSE streaming demo for text generation.
  - `/non_sse_app.py`: Standard (non-streaming) text generation endpoint.
- **Sentiment Analysis:**
  - `/main.py`: FastAPI app for sentiment analysis using DistilBERT.
- **Docker Support:**
  - Dockerfile provided for easy containerization.
- **CORS Enabled:**
  - All APIs allow cross-origin requests for easy frontend integration.

## Requirements

- Python 3.11 (or compatible)
- See `requirements.txt` for Python dependencies:
  - fastapi
  - uvicorn
  - transformers
  - torch
  - numpy

## Getting Started

### 1. Clone the repository
```sh
git clone https://github.com/yourusername/fass-demo-app.git
cd fass-demo-app
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```

### 3. Run an app
- **Sentiment Analysis:**
  ```sh
  uvicorn main:app --reload
  ```
- **Text Generation (SSE):**
  ```sh
  uvicorn sse_app:app --reload
  # or
  uvicorn sse_app_demo:app --reload
  ```
- **Text Generation (Non-SSE):**
  ```sh
  uvicorn non_sse_app:app --reload
  ```

### 4. Using Docker
Build and run the container:
```sh
docker build -t fass-demo-app .
docker run -p 8000:8000 fass-demo-app
```

## API Endpoints

- `POST /predict` (main.py, non_sse_app.py, sse_app.py):
  - Input: `{ "text": "your input" }` or query params
  - Output: Sentiment or generated text
- `POST /generate` (sse_app_demo.py):
  - Input: prompt and max_length as query params
  - Output: Streaming text generation


## Example Usage

- Use Postman or curl to interact with the endpoints.
- For streaming endpoints, use a client that supports Server-Sent Events (SSE).

---

## API Request/Response Examples

### 1. Sentiment Analysis (`main.py`)

**Request:**
```http
POST /predict
Content-Type: application/json

{
  "text": "I love this product!"
}
```
**Response:**
```json
{
  "sentiment": "POSITIVE",
  "confidence": 0.9998
}
```

**Request:**
```http
POST /predict
Content-Type: application/json

{
  "text": "This is terrible."
}
```
**Response:**
```json
{
  "sentiment": "NEGATIVE",
  "confidence": 0.9981
}
```

### 2. Text Generation (Non-Streaming, `non_sse_app.py`)

**Request:**
```http
POST /predict
Content-Type: application/json

{
  "text": "Once upon a time,"
}
```
**Response:**
```json
{
  "generated_text": "Once upon a time, there was a little girl who lived in a village near the forest."
}
```

**Request:**
```http
POST /predict
Content-Type: application/json

{
  "text": "The future of AI is"
}
```
**Response:**
```json
{
  "generated_text": "The future of AI is bright, with new advancements happening every day."
}
```

### 3. Text Generation (Streaming, `sse_app.py` or `sse_app_demo.py`)

**Request:**
```http
POST /predict?prompt=Hello%20world!&max_length=20
```
**Response (SSE stream):**
```
event: start
data: {"status": "Gnerating text...", "prompt": "Hello world!", "max_length": 20, "note": "Actual Streaming Version"}

event: update
data: {"generated_text": "Hello world! This is", "token_count": 1}

event: update
data: {"generated_text": "Hello world! This is a test", "token_count": 2}

... (more updates) ...

event: done
data: {"generated_text": "Hello world! This is a test of the streaming API.", "token_count": 8}

```

**Request:**
```http
POST /generate?prompt=FastAPI%20is%20&max_length=15
```
**Response (SSE stream):**
```
event: start
data: {"status": "Generating text...", "prompt": "FastAPI is ", "max_length": 15}

event: generated
data: {"generated_text": "FastAPI is a modern web framework"}

event: generated
data: {"generated_text": "FastAPI is a modern web framework for building APIs"}

... (more updates) ...

```

## License

[Apache 2.0](LICENSE)  

## Author

- [Rahul Chotaliya](https://github.com/Rahul-Chotaliya)

---

> **Note:**
> - The default models are GPT-2 for text generation and DistilBERT for sentiment analysis. You can change the model names in the code as needed.
> - For GPU support, ensure your environment is properly configured for PyTorch.
