# Transart-Multimodel
TransArt: A Multimodal Application for Vernacular Language Translation and Image Synthesis
Overview
This project is a Gradio-based application that processes Tamil audio file or live voice record Tamil audio to multiple AI tasks as mentioned below.

Transcription: Tamil audio → Tamil text
Translation: Tamil text → English text
Image Generation: English text → AI-generated image
Text Generation: English text → Further text generation
Models Used
Task	Model Name	Provider
Transcription	whisper-large-v3	Groq API
Translation	gemma2-9b-it	Groq API
Image Generation	black-forest-labs/FLUX.1-schnell	Hugging Face
Text Generation	deepseek-r1-distill-llama-70b	Groq API
Requirements
gradio
requests
pillow
groq
Secret Variable Setup
You must set up the Groq API key as a secret variable.

Steps to Add Secrets in Hugging Face Spaces
Go to your Hugging Face Space (the project where you're deploying your Gradio app).
Click on the "Settings" tab (inside the Space, not your account settings).
Scroll down to the "Repository Secrets" section.
Click "Add a new secret" and enter: Name: groq_api Value: Your Groq API key
Click "Save".
NOTE: There is no need of Hugging Face Access Token to use the image model as I deployed this Gradio app in the Hugging Face Space itself. If you are going to try this code outside Hugging Face you need to provide access token.

Usage
Run the script "app.py". This will launch a Gradio web interface where user can upload a Tamil audio file or live voice record Tamil audio and receive processed results.

Example Output
Tamil Audio Input: 🎤 (User uploads an audio file or live record)
Transcribed Tamil Text: "தமிழ் உரை"
Translated English Text: "Example Tamil text"
Generated Image: 🖼️ (AI-generated image displayed)
Generated Text: "Information about the text"
