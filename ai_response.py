#takes in a conversation and returns text and an audio file to be played
import tempfile
import openai
import simpleaudio as sa
from google.cloud import texttospeech



# takes in a conversation and returns a response from GPT-3
def generate_gpt_response(conversation):
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation
    )
    gpt3_response = res['choices'][0]['message']['content'].strip()

    return gpt3_response

# takes in a string and returns a path to a wav file
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


# plays the audio file and waits for it to finish
def play_audio_file(path_to_audio_file):
    # play the wav object and wait for it to finish
    wav_obj = sa.WaveObject.from_wave_file(path_to_audio_file)
    wav_obj.play().wait_done()


# takes in a conversation and returns text and an audio file to be played
def create_and_play_ai_response(conversation):
    # Generate a response from GPT-3
    gpt3_response = generate_gpt_response(conversation)

    # Convert the GPT-3 response to audio
    path_to_audio_file = text_to_speech(gpt3_response)

    # Play the audio file
    play_audio_file(path_to_audio_file)

    return gpt3_response, path_to_audio_file
