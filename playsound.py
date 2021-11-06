import simpleaudio as sa
import speech_recognition as sr

# sudo apt-get install libasound2-dev
# venv/bin/pip3 install simpleaudio


# venv/bin/pip3 install SpeechRecognition
# sudo apt-get install python3-pyaudio
# sudo apt-get install portaudio19-dev
# pip3 install pyaudio


# sudo apt-get install swig pulseaudio libpulse-dev
# pip3 install --upgrade pip setuptools wheel
# pip3 install --upgrade pocketsphinx
# sudo apt-get install flac


filename = 'gunoi1.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing

r = sr.Recognizer()

print(sr.Microphone.list_microphone_names())
mic = sr.Microphone()
with mic as source:
    r.adjust_for_ambient_noise(source)
    print("listening")
    audio = r.record(source=source, duration=4)
    print("listened")

response = {
    "success": True,
    "error": None,
    "transcription": None
}

try:
    print("transcribing")
    response["transcription"] = r.recognize_google(audio)
    print("transcribed")
except sr.RequestError as re:
    # API was unreachable or unresponsive
    response["success"] = False
    response["error"] = re
except sr.UnknownValueError:
    # speech was unintelligible
    response["error"] = "Unable to recognize speech"

print(response)
# r.recognize_sphinx()
