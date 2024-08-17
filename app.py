import gradio as gr
import os
import yt

from pydub import AudioSegment
from functools import lru_cache
from utils import count_lines_and_words, diff_texts, SEMANTIC_LEVELS, README
from prompts import SPEECH_IMPROVEMENT_PROMPT, SEMANTIC_ZOOM_PROMPT
from patterns import Patterns

from ai.llm.llmproviderfactory import LLMProviderFactory
from ai.stt.sttproviderfactory import STTProviderFactory
from ai.llm.openaiprovider import OpenAIProvider as  OpenAIProviderLLM
from ai.stt.openaiprovider import OpenAIProvider as OpenAIProviderSTT
from ai.llm.selfhostprovider import SelfHostProvider
from ai.llm.groqprovider import GroqProvider

# CONSTANTS
OPEN_AI = "OpenAI"
OPEN_AI_WHISPER = "Whisper"
GOOGLE = "Google"
MISTRAL = "Mistral"
GROQ = "Groq"
ANTHROPIC = "Anthropic"
SELF_HOSTED = "Self Hosted"

from dotenv import load_dotenv
load_dotenv()

llmfactory = LLMProviderFactory()
sttfactory = STTProviderFactory()

if os.getenv("OPENAI_API_KEY"):
  llmfactory.register_provider(OPEN_AI, OpenAIProviderLLM(os.getenv("OPENAI_API_KEY")))
  sttfactory.register_provider(OPEN_AI_WHISPER, OpenAIProviderSTT(os.getenv("OPENAI_API_KEY")))

if os.getenv("GROQ_API_KEY"):
  llmfactory.register_provider(GROQ, GroqProvider(os.getenv("GROQ_API_KEY")))

if os.getenv("SELF_HOST_URL"):
  llmfactory.register_provider(SELF_HOSTED, SelfHostProvider(os.getenv("SELF_HOST_URL")))
  
if len(llmfactory.get_registered_providers()) == 0:
  raise gr.Error("No provider registered. Please provide at least one provider.")

@lru_cache(maxsize=100)
def improve_speech(transcript, provider, model, top_p, temperature): 
  provider = llmfactory.get_provider(provider)
  system_message = {"role": "system", "content": SPEECH_IMPROVEMENT_PROMPT}
  user_message = {"role": "user", "content": transcript}
  messages = [system_message, user_message]
  
  return provider.generate_text(model, messages, top_p, temperature)

async def summarize_text(text, zoom_level, provider, model, top_p, temperature):
  if not text:
     raise gr.Info("Type something!")
   
  provider = llmfactory.get_provider(provider)
  system_message = {"role": "system", "content": SEMANTIC_ZOOM_PROMPT}
  user_message = {"role": "user", "content": "SUMMARY LEVEL: " + str(zoom_level) + "\n" + text}
  messages = [system_message, user_message]
  
  response = ""
  async for chunk in provider.generate_text_async(model, messages, top_p, temperature):
      response += chunk
      yield response

def recognize_speech(audio):
  if not audio:
    raise gr.Error("Missing record!")
  
  audio_segment = AudioSegment.from_file(audio)
  duration_seconds = len(audio_segment) / 1000
  
  if duration_seconds > 30 :
    raise gr.Error( "Audio input should not be longer than 30 seconds.")
  
  provider = sttfactory.get_provider(OPEN_AI_WHISPER)
  return provider.transcribe("whisper-1", audio)

async def run_prompt(provider, model, prompt, input, top_p, temperature):
  if not input:
    raise gr.Info("Type something!")
    
  system_prompt, user_prompt = Patterns().get_prompt(prompt)
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt + "\n" + input}
  ]
  
  provider = llmfactory.get_provider(provider)
  
  response = ""
  async for chunk in provider.generate_text_async(model, messages, top_p, temperature):
    response += chunk
    yield response
  
########################## UI

def provider_changed(provider):
  models = llmfactory.get_provider(provider).list_models()
  return { model: gr.Dropdown(choices=models, interactive=True, label="Model", value=models[0]), main_col: gr.Column(visible=True) }
  
def model_changed(model):
  return model
    
def zoom_level_changed(zoom_level):
  return gr.Slider(1, 5, value=zoom_level, label=SEMANTIC_LEVELS[zoom_level], info="", interactive=True, step=1)

def input_text_changed(text):
  lines_count, workds_count = count_lines_and_words(text)
  return gr.Textbox(lines=4, value=text, info=f'{lines_count} lines | {workds_count} words')
  
def transcribe_youtube(url):
  return yt.YT().get_transcript(url)
  
with gr.Blocks() as ui:
  
  with gr.Row():
    with gr.Column():
      providers = llmfactory.get_registered_providers()
      provider = gr.Radio(providers, label= "Provider")
      model = gr.Dropdown(choices=None, interactive=True, label="Model")
    
    with gr.Column():
      temperature = gr.Slider(0.0, 1.0, value=0.5, label="Temperature", interactive=True, step=0.1, info="Controls the randomness of the model. Lower values make the model more deterministic.")
      top_p = gr.Slider(0.0, 1.0, value=0.5, label="Top P", interactive=True, step=0.1, info="Controls the diversity of the model. Lower values make the model more deterministic.")
    
  with gr.Tabs(visible=False) as main_col:
        
    with gr.TabItem("Prompts"):
      with gr.Column():
        prompt = gr.Dropdown(choices=Patterns().get_prompt_list(), interactive=True, label="Prompt")
        input_prompt = gr.Textbox(label="Text:", lines=4)
        button_prompt = gr.Button("Run")
        output_prompt = gr.Markdown(label="Output:")
    
    with gr.TabItem("Youtube Transcription"):
      with gr.Column():
        input_youtube = gr.Textbox(label="Youtube link:", lines=1)
        button_youtube = gr.Button("Transcribe")
        output_youtube = gr.Textbox(label="Transcript:", lines=4)
        
           
  # provider/model events
  provider.change(provider_changed, inputs=[provider], outputs=[model, main_col])
  model.change(model_changed, inputs=[model], outputs=[model])
    
  # youtube events
  button_youtube.click(transcribe_youtube, inputs=[input_youtube], outputs=[output_youtube])
  output_youtube.blur(input_text_changed, inputs=[output_youtube], outputs=[output_youtube])
  
  # prompt events
  button_prompt.click(run_prompt, inputs=[provider, model, prompt, input_prompt, top_p, temperature], outputs=[output_prompt])
  input_prompt.blur(input_text_changed, inputs=[input_prompt], outputs=[input_prompt])
  
ui.queue(max_size=10)
ui.launch()