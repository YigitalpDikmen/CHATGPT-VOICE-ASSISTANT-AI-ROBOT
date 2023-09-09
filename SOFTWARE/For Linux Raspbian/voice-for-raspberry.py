#----------------------------START--------------------------
import os #For getting the path.
import time #For waiting.
import speech_recognition as sr #For trigger the program.
from google.cloud import texttospeech #For voice Output
import openai #For ChatGpt and Whisper
import pyaudio #For voice record
from pydub import AudioSegment #For getting the duration of sound files.
import numpy as np #For voice record contiunity
#import pygetwindow #For minimize the media player window
#--------------------------- RECORD --------------------------
import sounddevice as sd #For voice record
import soundfile as sf #For voice record
#--------------------------- RECORD --------------------------
#--------------------------- FOR PI --------------------------
import wave
import alsaaudio
#--------------------------- FOR PI --------------------------
#--------------------------- FOR PI2 --------------------------
# Ses kaydı için parametreler
CHUNK = 1024
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # Sessizlik eşiği (ses seviyesi)
SILENT_TIME_THRESHOLD = 4  # Sessizlik süresi eşiği (saniye)
#sudo apt install mpg321 #ses oynatmak için bunu kurmalısınız.
#for speak raspberry pi
#--------------------------- FOR PI2 --------------------------
#--------------------------- FOR PI3 --------------------------
import board
import neopixel
pixel_number = 12
#D21 Yani GPIO21 Yani Fiziksel 40. pin
pixels = neopixel.NeoPixel(board.D21,pixel_number)
#pixels.fill((0,0,0)) #tüm pikselleri tek seferde aynı renk yapar.
#Düzen - RGB Şeklinde:
#pixels[x] = (255, 0, 0) - Tamamen Kırmızı
#pixels[x] = (0, 255, 0) - Tamamen Yesil
#pixels[x] = (0, 0, 255) - Tamamen Mavi
#pixels[x] = (255, 0, 255) - Tamamen Mor
#pixels[x] = (0, 255, 255) - Tamamen Turkuaz
#pixels[x] = (255, 255, 0) - Tamamen Sarı
#pixels[x] = (0, 0, 0) - Renk Kapalı
#pixels[x] = (255, 255, 255) - Tamamen Beyaz
"""  
for x in range(0,6,+1):
    pixels[x] = (255, 0, 0)
"""
"""
The audio jack channels (left and right) are provided by 
PWM driven GPIO (channel 0 by GPIO 12 or 18, and channel 1 by GPIO 13 or 19).
So if you connect appropriate circuitry to those GPIO you will get audio.
See BCM2835 ARM Peripherals for details on the GPIO and PWM peripheral.
Yani 3.5mm Hoparlör Jakı bu pinlere bağlı, o yüzden bu pinlerden led sürme.
Ledi D21 - GPIO21 (Fiziksel olarak 40.Pin) Pininden Sür. O zaman sorun yaşamazsın.
"""
#--------------------------- FOR PI3 --------------------------
#--------------------------- FOR PI4 --------------------------
import os
#os.system('sudo python /home/minikod/Desktop/red.py')
#parametre = "mavi"
#os.system("sudo python colors.py {}".format(parametre))
#--------------------------- FOR PI4 --------------------------
#https://www.gyan.dev/ffmpeg/builds/ - ffmpeg-git-full.7z - C:\ffmpeg\bin 
#Kullanıcı ve Sistem için Path değişkenine bu yol dahil edilmelidir.
#--------------------------- KEYS ----------------------------
# Set OpenAI API key
openai.api_key = "YOUR OPENAI API KEY"

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR GOOGLE JSON FILE NAME"

# Initialize Whisper model
whisper_model = "whisper-1"

# Initialize ChatGPT model
chatgpt_model = "gpt-3.5-turbo"
#--------------------------- KEYS ---------------------------
#--------------------- GOOGLE VOICE OUTPUT ------------------
# Initialize Google Text-to-Speech client
google_client = texttospeech.TextToSpeechClient()
# Function to speak
def speak(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="tr-TR", ssml_gender=texttospeech.SsmlVoiceGender.MALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = google_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    #os.system("start output.mp3")
    os.system("mpg321 output.mp3")

def process_voice_input():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Processing voice input...")
        text = r.recognize_google(audio, language="tr-TR")
        print("Voice input:", text)
        return text
    except sr.UnknownValueError:
        print("Unable to understand the voice input.")
    except sr.RequestError as e:
        print(f"Error occurred during speech recognition: {e}")
#--------------------- GOOGLE VOICE OUTPUT ------------------
#--------------------  CHATGPT RESPONSE ---------------------
def process_chatgpt_input(input_text):
    response = openai.Completion.create(
        engine=chatgpt_model,
        prompt=input_text,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
        log_level="info"
    )

    return response.choices[0].text.strip()
#--------------------  CHATGPT RESPONSE ----------------------
#------------------------ RECORD1 -----------------------------
""" 
def record_audio(duration, filename):
    print("kayit basladi")
    # Set the sample rate and number of channels
    sample_rate = 44100  # CD quality audio
    channels = 2        # Stereo sound

    # Record audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)

    # Wait until the recording is finished
    sd.wait()

    # Save the recorded audio as an .mp3 file
    sf.write(filename, recording, sample_rate)
    print("kayit bitti")
"""
#------------------------ RECORD1 -----------------------------
#------------------------ RECORD2 -----------------------------
""" 
def record_audio(filename):
    print("Recording started...")
    # Set the sample rate and number of channels
    sample_rate = 44100  # CD quality audio
    channels = 2        # Stereo sound

    # Initialize an empty list to store the recorded frames
    frames = []

    # Start recording audio
    stream = sd.InputStream(samplerate=sample_rate, channels=channels, callback=None, dtype='float32', latency='low')
    stream.start()

    # Set the timeout duration in seconds
    timeout_duration = 2

    # Variables to track the time of the last speech and the timeout
    last_speech_time = time.time()
    timeout = False

    # Loop until a timeout or speech pause occurs
    while not timeout:
        # Read a chunk of audio frames
        chunk, overflow = stream.read(1024)
        frames.append(chunk)

        # Check if there is speech in the current chunk
        if np.max(np.abs(chunk)) > 0.01:
            # Reset the last speech time
            last_speech_time = time.time()

        # Check if the timeout duration has elapsed
        if time.time() - last_speech_time > timeout_duration:
            timeout = True

    # Stop recording audio
    stream.stop()
    stream.close()

    # Convert the recorded frames to a NumPy array
    audio_data = np.concatenate(frames, axis=0)

    # Save the recorded audio as an .mp3 file
    sf.write(filename, audio_data, sample_rate)
    print("Recording finished.")
"""
#------------------------ RECORD2 -----------------------------
#------------------------ RECORD3 PI --------------------------
def record_audio(filename):
    audio = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, device='default',
                          channels=CHANNELS, rate=RATE, format=FORMAT, periodsize=CHUNK)

    print("Ses kaydı başladı. Konuşmayı bitirdiğinizde duracak.")

    frames = []
    silent_start_time = None

    while True:
        # Ses verilerini bir tuple olarak al
        length, data = audio.read()
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Sessizlik eşiğinin altında mı kontrol edelim
        if np.max(np.abs(audio_data)) < THRESHOLD:
            if silent_start_time is None:
                silent_start_time = time.time()
            else:
                # Sessizlik süresini kontrol et
                if time.time() - silent_start_time > SILENT_TIME_THRESHOLD:
                    break
        else:
            silent_start_time = None

        frames.append(data)

    print("Ses kaydı tamamlandı. Kaydedilen veriler işleniyor...")

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 2 bytes for 16-bit format
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Kaydedilen ses dosyası: {filename}")
#------------------------ RECORD3 PI --------------------------
#--------------------------- RECORDX --------------------------
# Specify the duration of the recording (in seconds) for fixed record1
#duration = 5

# Specify the filename for saving the recorded audio
filename = "kaydedilen_ses.wav"
#--------------------------- RECORDX --------------------------
#--------------------------- WAIT -----------------------------
def get_duration(file_path2):
    audio = AudioSegment.from_file(file_path2)
    duration_ms = len(audio)
    duration_sec = duration_ms / 1000
    return duration_sec
#--------------------------- WAIT ----------------------------
#------------------- MAIN LOOP FUNCTION ----------------------
def main():
    while True:

        #Yesil
        os.system("sudo python colors.py {}".format("green"))

        voice_input = process_voice_input()

        if voice_input is None:
            continue  # Skip the rest of the loop and start again

        if "selam" in voice_input.lower():
        #if voice_input.lower() == "selam":

            #Sari
            os.system("sudo python colors.py {}".format("yellow"))

            speak("Merhaba, sizi dinliyorum.")

            # Get the media player window and minimize it
            """ 
            media_player = pygetwindow.getWindowsWithTitle("Medya Oynatıcı")[0]
            time.sleep(1.2)
            media_player.minimize()
            """

            folder_path3 = os.path.dirname(os.path.abspath(__file__))  # Get current folder path
            file_name3 = "output.mp3"  # Specify the file name
            file_path3 = os.path.join(folder_path3, file_name3)  # Construct the file path
            duration3 = get_duration(file_path3)
            print("Duration in seconds:", duration3)

            time.sleep(duration3) # Pause for a moment to avoid capturing immediate voice input 

            #Mavi
            os.system("sudo python colors.py {}".format("blue"))

            print("Processing voice input with Whisper...")

            # Call the function to record and save the audio
            #record_audio(duration, filename)
            record_audio(filename)

            #Gonder
            folder_path = os.path.dirname(os.path.abspath(__file__))  # Get current folder path
            file_name = "kaydedilen_ses.wav"  # Specify the file name
            file_path = os.path.join(folder_path, file_name)  # Construct the file path
            file = open(file_path, "rb")
            
            #file = open("/path/to/file/openai.mp3", "rb")

            #Mor
            os.system("sudo python colors.py {}".format("purple"))

            transcription = openai.Audio.transcribe("whisper-1", file)

            transcription_text = transcription["text"]
            print(transcription_text)

            #Mor
            os.system("sudo python colors.py {}".format("purple"))

            #Beyaz
            os.system("sudo python colors.py {}".format("white"))

            #Mor
            os.system("sudo python colors.py {}".format("purple"))

            #Beyaz
            os.system("sudo python colors.py {}".format("white"))

            #Mor
            os.system("sudo python colors.py {}".format("purple"))

            print("Processing text input with ChatGPT...")

            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": transcription_text}]
            )

            #Kirmizi
            os.system("sudo python colors.py {}".format("red"))

            print("ChatGPT response:")
            response_content = completion["choices"][0]["message"]["content"]
            print(response_content)
            
            speak(response_content)

            # Get the media player window and minimize it
            """ 
            media_player = pygetwindow.getWindowsWithTitle("Medya Oynatıcı")[0]
            time.sleep(1.2)
            media_player.minimize()
            """

            folder_path2 = os.path.dirname(os.path.abspath(__file__))  # Get current folder path
            file_name2 = "output.mp3"  # Specify the file name
            file_path2 = os.path.join(folder_path2, file_name2)  # Construct the file path
            duration2 = get_duration(file_path2)
            print("Duration in seconds:", duration2)

            time.sleep(duration2)
#------------------- MAIN LOOP FUNCTION ----------------------
#------------------- CALL THE MAIN ---------------------------
if __name__ == "__main__":
    main()
#------------------- CALL THE MAIN ---------------------------