# Fabric Gradio
This app provides a simple web interface for testing [fabric](https://github.com/danielmiessler/fabric) patterns.

![Screen Recording](https://github.com/zgngr/fabric-gradio/blob/main/ss-1.png?raw=true)
![Screen Recording](https://github.com/zgngr/fabric-gradio/blob/main/ss-2.png?raw=true)

## Requirements
Define at least one of supported providers in your environment.

```
OPENAI_API_KEY=YOUR_KEY_GOES_HERE
GROQ_API_KEY=YOUR_KEY_GOES_HERE
SELF_HOST_URL=YOUR_URL_GOES_HERE
```

## Running app locally
Running app locally - (Python VENV recommended)
```
pip install -r requirements.txt
python app.py
```

Browse http://127.0.0.1:7860/
