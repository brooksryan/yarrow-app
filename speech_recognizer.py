import os
import io
import tempfile
import random
import speech_recognition as sr
from gtts import gTTS
import simpleaudio as sa
from pydub import AudioSegment
import openai
import pyaudio

def transcribe_speech():
    r = sr.Recognizer() # initialize recognizer
    with sr.Microphone() as source: # microphone as source
        print("Please say something...") # message to the user
        audio = r.listen(source) # listen for the first phrase and extract it into audio data
    try:
        text = r.recognize_google(audio) # recognize speech using Google Speech Recognition
        print(f"You said: {text}") 
        return text
    except:
        print("Sorry, I didn't catch that. Please try again.")
        return None


def generate_question():
    question = [
        "Where do you see yourself in five years?",
        "What are your strengths and weaknesses?",
    ]
    return random.choice(question)

def generate_gpt_response(conversation):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation
        )
    
    return res['choices'][0]['message']['content'].strip() # return the completion

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        temp_path = f"{fp.name}.mp3"
        tts.save(temp_path)

        # Convert the MP3 file to WAV
        mp3_audio = AudioSegment.from_mp3(temp_path)
        with tempfile.NamedTemporaryFile(delete=True) as wav_fp:
            temp_wav_path = f"{wav_fp.name}.wav"
            mp3_audio.export(temp_wav_path, format="wav")

            # Load the WAV audio file
            with open(temp_wav_path, 'rb') as f:
                audio_data = f.read()

            # Play the WAV audio file
            wave_obj = sa.WaveObject.from_wave_file(io.BytesIO(audio_data))
            play_obj = wave_obj.play()
            play_obj.wait_done()

            os.remove(temp_wav_path)

        os.remove(temp_path)

def show_active_microphone():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    default_device_index = p.get_default_input_device_info()["index"]

    print("\nAvailable audio input devices:")
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get("name")
        device_index = device_info.get("index")

        if device_info.get("maxInputChannels") > 0:  # This is an input device
            if device_index == default_device_index:
                print(f"* Device {i}: {device_name} (default)")
            else:
                print(f"  Device {i}: {device_name}")

    p.terminate()

def main():
    print("Welcome to the Job Interview Practice Program!")
    while True:
        conversation = [
            {"role": "system", "content": "You are interviewing the candidate for a product management position at a tech company. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. You can use the [satisfied] token to indicate that you are satisfied with the candidate's answer."},
            {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."},
        ]

        #print the first item in the conversation and the last item in the coversation

        question = generate_question()
        conversation.append({"role": "assistant", "content": question})

        while True:
            print("Interviewer: ", question)
            text_to_speech(question)
            response = transcribe_speech()

            if response is None:
                continue

            conversation.append({"role": "user", "content": response})

            # Generate response from GPT
            gpt_response = generate_gpt_response(conversation)

            if "[satisfied]" in gpt_response:
                gpt_response = gpt_response.replace("[satisfied]", "").strip()
                break

            conversation.append({"role": "assistant", "content": gpt_response})    
            question = gpt_response
            print(conversation)

        print("Interviewer: ", gpt_response)
        text_to_speech(gpt_response)

        # You can add more logic here to evaluate the user's response or give feedback.

if __name__ == "__main__":
    show_active_microphone()
    main()
