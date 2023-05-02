import os
import tempfile
import random
import speech_recognition as sr
import simpleaudio as sa
import requests
import pyaudio
import openai

COQUI_API_TOKEN = "py00vG5IM940cT8J5g2cio9UFXfmNKKMOCXciZdzm3qoxJMu419AuNbiALzDguDC"

def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}") 
        return text
    except:
        print("Sorry, I didn't catch that. Please try again.")
        return None

# Generate a random question for the user
def generate_question():
    question = [
        #"Hi, my name is Yarrow. I'm an AI designed to interview you about your product management experience. Let's dive into your background a little. Can you tell me about your work experience and how it relates to product management?",
        "Hi, my name is Yarrow. I'm an AI designed to interview you about your product management experience. We're going to just get started with a question that will help me better udnerstand your general product management senses. Does that sound good?",
    ]
    return random.choice(question)

def generate_gpt_response(conversation):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = conversation
        )
    
    return res['choices'][0]['message']['content'].strip() # return the completion

def text_to_speech(text):
    text = text[:250]  # Coqui TTS has a 250 character limit
    url = "https://app.coqui.ai/api/v2/samples"
    headers = {
        "Authorization": f"Bearer {COQUI_API_TOKEN}",
        "content-type": "application/json",
    }
    data = {
        "name": "temporary_sample",
        "voice_id": "f05c5b91-7540-4b26-b534-e820d43065d1",
        "text": text,
        "emotion": "Happy",
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if 'audio_url' not in response_json:
        print(f"Error: Coqui API response does not contain 'audio_url':\n{response_json}")
        return None

    audio_url = response_json["audio_url"]
    audio_response = requests.get(audio_url)

    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio_response.content)
        temp_filename = f.name

    wav_obj = sa.WaveObject.from_wave_file(temp_filename)
    os.unlink(temp_filename)  # delete the temporary file after creating the WaveObject

    return wav_obj

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
        
            # write this text in the conversation format:
            # conversation = [ 
            # {"role": "system", "content": One person’s job is to try to negotiate for as much of the $2 as possible.
            # The other people will be told – in secret – to aim for one of the following total amounts, if not more:

            # $00.50
            # $00.80
            # $1.00
            # $1.30
            # $1.60
            # Pairs then have 10 minutes to negotiate. Tell them there will be three total rounds and they’ll have new partners for each one."},

        conversation = [
            {"role": "system", "content": "You are a participant in the two dollar game. The two dollar game has become one of the most popular negotiation exercises and can be a lot of fun for a team of new employees. You will be given a partner and $2. You have to decide with your partner how to split the $2. Your job is to try to negotiate for as much of the $2 as possible. Your partner will be told to aim for one of the following total amounts, if not more:$00.50 $00.80 $1.00 $1.30 $1.60. You will not know the amount your partner is trying to negotiate for. Pairs then have 10 minutes to negotiate. Tell them there will be three total rounds and they’ll have new partners for each one."},
        ]

        
        # conversation = [
        #     {"role": "system", "content": "You are interviewing the candidate for a product management position at a tech company. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. You can use the [satisfied] token to indicate that you are satisfied with the candidate's answer. "},
        #     {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."},
        # ]

        #print the first item in the conversation and the last item in the coversation

        question = generate_question()
        conversation.append({"role": "assistant", "content": question})

        while True:
            print("Interviewer: ", question)
            wav_obj = text_to_speech(question)
            wav_obj.play().wait_done()
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
        wav_obj = text_to_speech(gpt_response)
        wav_obj.play().wait_done()

        # You can add more logic here to evaluate the user's response or give feedback.

if __name__ == "__main__":
    show_active_microphone()
    main()
