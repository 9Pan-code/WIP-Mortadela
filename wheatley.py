import subprocess
import sounddevice
import re
import pyttsx3
import os
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import time

print("MORTADELA OPERATIVA")

Time_Voice = 4.5
FS = 16000
count = 0
tts = pyttsx3.init()
tts.setProperty("rate", 180)
tts.setProperty("volume", 1.5)

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

apps = {
    "notas": "notepad.exe",
    "calculadora": "calc.exe",
    "explorador": "explorer.exe",
    "spotify": r"C:\Users\Pan9\AppData\Roaming\Spotify\Spotify.exe",
    "discord": r"C:\Users\Pan9\AppData\Local\Discord\app-1.0.9244\Discord.exe",
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "new vegas": r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\FalloutNV.exe",
    "neo vegas": r"C:\Program Files (x86)\Steam\steamapps\common\Fallout New Vegas\FalloutNV.exe",
    "ultrakill": r"C:\Program Files (x86)\Steam\steamapps\common\ULTRAKILL\ULTRAKILL.exe",
    "ultra": r"C:\Program Files (x86)\Steam\steamapps\common\ULTRAKILL\ULTRAKILL.exe",
}

processes = {
    "notas": "notepad.exe",
    "calculadora": "calc.exe",
    "explorador": "explorer.exe",
    "spotify": "Spotify.exe",
    "discord": "Discord.exe",
    "steam": "steam.exe",
    "new vegas": "FalloutNV.exe",
    "neo vegas": "FalloutNV.exe",
    "ultrakill": "ULTRAKILL.exe",
    "ultra": "ULTRAKILL.exe",
}

def listen():
    print("\n MORTADELA esta escuchando...")
    audio = sounddevice.rec(
        int(Time_Voice * FS),
        samplerate=FS,
        channels=1,
        dtype="int16"
    )
    sounddevice.wait()
    write("audio.wav", FS, audio)

def recognise():
    segments, info = model.transcribe(
        "audio.wav",
        language="es"
    )
    text = ""
    for segment in segments:
        text += segment.text

    return text.lower().strip()

def speak(text):
    print("Mortadela", text)
    tts.say(text)
    tts.runAndWait()

def execute(command):
    command = command.lower()
    command = re.sub(r"[^\w\s]", "", command)
    command = command.strip()
    
    print("Comando:", command)

    if "abre" in command:
        app = command.replace("abre ", "").strip()
        for name, route in apps.items():
            if name in app:
                subprocess.Popen(route)
                speak(f"Abriendo {name}")
        return
    speak("No conozco esa aplicación.")
    
    if "cierra" in command or "fierra" in command:
        app = command.replace("cierra", "").replace("fierra", "").strip()
        for process_name, process in processes.items():
            if process_name in app:
                result = subprocess.run(
                    f'taskkill /f /im "{process}"',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    speak(f"Cerrando {process_name}")
                else:
                    print(result.stderr)
            return
    speak("No conozco esa aplicación.")
    
    if "tiempo" or "hora" in command:
        speak(f"{time.now()}")
    
while True:
    if count >= 3:
        count = 0
        os.system("cls") 
    listen()
    text = recognise()
    execute(text)
    count += 1