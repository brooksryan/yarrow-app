import pyaudio
import speech_recognition as sr


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

def transcribe_speech():

    show_active_microphone()
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