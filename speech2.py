import speech_recognition as sr
r=sr.Recognizer()
with sr.AudioFile('1.wav') as source:
    audio = r.listen(source)
    try:
        text=r.recognize_google(audio)
        print("Working on it")
        print(text)
    except:
        print('Sorry....run again')