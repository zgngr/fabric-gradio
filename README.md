# Fabric Gradio
This app provides a simple web interface for testing [fabric](https://github.com/danielmiessler/fabric) patterns.

## Requirements
Define at least one of supported providers in your environment.

```
OPENAI_API_KEY=YOUR_KEY_GOES_HERE
GROQ_API_KEY=YOUR_KEY_GOES_HERE
SELF_HOST_URL=YOUR_URL_GOES_HERE
```

## Steps to take for self hosting
1. Download & install [ollama](https://ollama.com/) 
2. After ollama installed you need to download desired model from [model catalogue](https://ollama.com/library). 
```
ollama pull llama3
```
3. Serve model through [ollama's REST API](https://github.com/ollama/ollama?tab=readme-ov-file#rest-api).

```
ollama serve
```
4. Make sure server running on http://localhost:11434
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt":"Why is the sky blue?"
}'
```
5. Set your environment variable 
```
SELF_HOST_URL=http://localhost:11434
```

## Running app locally
Running app locally - (Python VENV recommended)
```
pip install -r requirements.txt
python app.py
```

Browse http://127.0.0.1:7860/