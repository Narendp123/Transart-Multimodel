!pip install gradio
!pip install groq

import torch
import gradio as gr
from transformers import pipeline, GPTNeoForCausalLM, GPT2Tokenizer
import requests
from PIL import Image
import io

# Model and device configuration for Whisper
MODEL_NAME = "openai/whisper-large-v3"
BATCH_SIZE = 8
device = 0 if torch.cuda.is_available() else "cpu"

# Initialize Whisper pipeline
pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

# Define translation function
def translate(inputs, task):
    if inputs is None:
        raise gr.Error("No audio file submitted! Please upload or record an audio file before submitting your request.")
    result = pipe(inputs, batch_size=BATCH_SIZE, generate_kwargs={"task": task}, return_timestamps=True)
    return result["text"]

# API details for image generation
API_URL = "https://api-inference.huggingface.co/models/XLabs-AI/flux-RealismLora"
headers = {"Authorization": "Bearer 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"}  # Replace with your Hugging Face token

# Define image generation function
def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))
    return image

# Initialize GPT-Neo model and tokenizer
text_model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
text_tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")

# Define text generation function
def generate_text(prompt, temperature=0.9, max_length=100):
    inputs = text_tokenizer(prompt, return_tensors="pt")
    gen_tokens = text_model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        do_sample=True,
        temperature=temperature,
        max_length=max_length,
        pad_token_id=text_tokenizer.eos_token_id,
    )
    gen_text = text_tokenizer.decode(gen_tokens[0], skip_special_tokens=True)
    return gen_text

# Gradio app with multiple functionalities in tabs
with gr.Blocks() as demo:
    with gr.Tab("Microphone Translation"):
        gr.Markdown("Audio Translation")
        mic_input = gr.Audio(sources="microphone", type="filepath", label="Microphone Input")
        mic_task = gr.Radio(["translate"], label="Task", value="translate")
        mic_output = gr.Textbox(label="Translated Text")
        gr.Button("Submit").click(translate, inputs=[mic_input, mic_task], outputs=mic_output)
        gr.Markdown("Image Generation ")
        img_output = gr.Image(label="Generated Image")
        gr.Button("Generate").click(generate_image, inputs=mic_output, outputs=img_output)
        gr.Markdown(" Text Generaion")

    with gr.Tab("File Upload Translation"):
        gr.Markdown("File Translation")
        file_input = gr.Audio(sources="upload", type="filepath", label="Upload Audio File")
        file_task = gr.Radio(["translate"], label="Task", value="translate")
        file_output = gr.Textbox(label="Translated Text")
        gr.Button("Submit").click(translate, inputs=[file_input, file_task], outputs=file_output)
        gr.Markdown(" Image Generation")
        img_output = gr.Image(label="Generated Image")
        gr.Button("Generate").click(generate_image, inputs=file_output, outputs=img_output)
# Launch the app
demo.launch()
