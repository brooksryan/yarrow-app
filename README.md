# Conversational AI Assistant

This is a conversational AI assistant built using Google's Text-to-Speech, Speech-to-Text, and OpenAI's GPT-4 models. It can be used to simulate different interaction scenarios such as job interviews or negotiation exercises.

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/your_username/Conversational_AI_Assistant.git
cd Conversational_AI_Assistant
```
2. **Install the necessary Python packages. It's recommended to do this in a Python virtual environment.**
```bash
pip install -r requirements.txt
``` 
You will also need to install some additional software dependencies:

PortAudio: This is used by PyAudio, which is required to access the microphone. You can install it using the following command:

On Ubuntu:
bash
Copy code
sudo apt-get install portaudio19-dev
On macOS:
bash
Copy code
brew install portaudio
ffmpeg: This is required for the audio processing. You can install it using the following command:

On Ubuntu:
bash
Copy code
sudo apt-get install ffmpeg
On macOS:
bash
Copy code
brew install ffmpeg
You need to set up your environment variables for the application to work. This includes your Coqui API token, Google Cloud API token, and OpenAI API token.

Create a .env file in your project directory and add the following lines (replace <YOUR_TOKEN> with your actual tokens):

bash
Copy code
COQUI_API_TOKEN=<YOUR_COQUI_API_TOKEN>
GOOGLE_API_TOKEN=<YOUR_GOOGLE_API_TOKEN>
OPENAI_API_TOKEN=<YOUR_OPENAI_API_TOKEN>
You can now run the assistant:

bash
Copy code
python main.py
Usage
Once you run the assistant, it will prompt you with a message indicating that it's ready to start. The assistant will then provide a situation and personas for the interaction. You will interact with the assistant verbally, and it will respond in kind.

If the assistant doesn't understand your response, it may ask you to repeat or rephrase your input.
