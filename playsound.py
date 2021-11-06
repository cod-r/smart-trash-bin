import simpleaudio as sa
import speech_recognition as sr

# sudo apt-get install libasound2-dev
# venv/bin/pip3 install simpleaudio


# venv/bin/pip3 install SpeechRecognition
# sudo apt-get install python3-pyaudio
# sudo apt install portaudio19-dev
# pip3 install pyaudio

filename = 'gunoi1.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing

r = sr.Microphone.list_microphone_names()
# r.recognize_sphinx()
