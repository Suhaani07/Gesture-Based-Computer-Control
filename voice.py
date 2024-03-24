import speech_recognition as sr
r = sr.Recognizer()
t = sr.Recognizer()
text=""
subtext=""
with sr.Microphone() as source:
    print("Listening")
    audio_text = r.listen(source)
    try:
        text=r.recognize_google(audio_text)
        print("Trigger word detected: "+text)
        if(text=="listen"):
            print("Listening")
            audio_text = r.listen(source)
            try:
                subtext=r.recognize_google(audio_text)
                if(subtext=="Mouse click"):
                    print(subtext+"ed")
            except:
                print("Sorry, I did not get that")
    except:
         print("Sorry, I did not get that")