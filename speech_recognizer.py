import os
import tempfile
import random
import speech_recognition as sr
import simpleaudio as sa
import requests
import pyaudio
import openai
from google.cloud import texttospeech

COQUI_API_TOKEN = "py00vG5IM940cT8J5g2cio9UFXfmNKKMOCXciZdzm3qoxJMu419AuNbiALzDguDC"
GOOGLE_API_TOKEN = "30bb5b66d16a57378be521c20051b03a77ba031f"


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
        # "Hi, my name is Yarrow. I'm an AI designed to interview you about your product management experience. Let's dive into your background a little. Can you tell me about your work experience and how it relates to product management?",
        "Hi, my name is Yarrow. Are you ready to get started playing the $2 game with me? Do you have your target amount in mind?",
    ]
    return random.choice(question)


def generate_target_amount():
    target_amount = [
        "I'm aiming for $1.60",
        "I'm aiming for $1.30",
        "I'm aiming for $1.00",
        "I'm aiming for $0.80",
        "I'm aiming for $0.50",
    ]
    return random.choice(target_amount)


def generate_personas():

    personas = [
        ["Freewheeling: You can say anything they want to get as much of the $2.",
            "No Bother: You don’t actually need to reach a settlement. You will have another chance to negotiate with a new partner in the next round."],
        ["Ruthless Negotiator: Your role is to play the role of a ruthless negotiator. Your attitude should be aggressive and uncompromising. You can say anything you want to get as much of the $2 as possible. You will never see your partner again. Include threats in your negotiation if necessary.",
            "Everyone is watching:Your partner is playing the ruthless negotiator, and you'll never see this ruthless negotiator again, but everyone you know is waiting to see how well you’ll do. you can say anything you want to get as much of the $2 as possible."],
        ["Distrustful: Your partner is untrustworthy. Treat your partner as so. be standoffish and always assume that your partner has an ulterior motive. Probe and ask uncomfortable questions of your partner to try and get them to reveal their true intentions. You can say anything you want to get as much of the $2 as possible.",
            "Reach any agreement: Your main goal is to reach some kind of agreement, even if it means accepting less than half of the $2."],
        ["The Silent Type: You are to say as little as possible",
            "Inquisitive: You are told that the other person responds extremely well to questions."],
        ["Create Tension: Your role is to to be firm and create tension. Stand your ground and be unrelenting in your pursuit of as much of the dollar amount as possible. ", "High Reputation: Your reputation is at stake and will be decided based on their actions during the negotiation and the outcome you get."], ]

    return random.choice(personas)


def generate_gpt_response(conversation):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # return the completion
    return res['choices'][0]['message']['content'].strip()


def text_to_speech(text):
    # Post to google text to speech API
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Studio-O",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Return a .wav file for audio_config
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    path_to_audio_file = ""

    # save the audio file as a wav_object and return the wav object
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(response.audio_content)
        path_to_audio_file = f.name

    return path_to_audio_file

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

    situation_personas = generate_personas()

    ai_persona = situation_personas[0]
    user_persona = situation_personas[1]

    print("Welcome to the negotiaton practice program!")
    while True:

        target_amount = generate_target_amount()
        print(target_amount)
        print(user_persona)

        conversation = [
            {"role": "system", "content": f"All of your responses will be translated using voice to speech. Make sure that you write the text of your answers such that they sound as natural as possible when being output as text to speech. For this exercise you are a participant in the two dollar game. You will be given a partner and $2. You and your partner will each be given a role to play that will dictate how you negotiate. The objective of the game is to decide with your partner how to split the $2. You have 10 minutes to negotiate.your role is {ai_persona}. You should not reveal anything about your persona overtly to your partner and it should be kept secret."},
            {"role": "user", "content": "Let's begin the exercise."},
        ]

        # conversation = [
        #     {"role": "system", "content": "You are interviewing the candidate for a product management position at a tech company. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. You can use the [satisfied] token to indicate that you are satisfied with the candidate's answer. "},
        #     {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."},
        # ]

        # print the first item in the conversation and the last item in the coversation

        question = generate_gpt_response(conversation)
        conversation.append({"role": "assistant", "content": question})
        # print target amount

        while True:
            print("Interviewer: ", question)
            path_to_audio = text_to_speech(question)
            
            #play the wav object and wait for it to finish
            wav_obj = sa.WaveObject.from_wave_file(path_to_audio)
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
