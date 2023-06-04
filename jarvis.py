# Import necessary libraries
import speech_recognition as sr
import openai
from elevenlabs import generate, play

r = sr.Recognizer()
mic = sr.Microphone()

conversation = [
    {"role": "system", "content": "Your name is Maat and your purpose is to be an Human like assistant"},
]

assistant_name = "maat"
activated = False

while True:
    with mic as source:
        # 1. Adjust for ambient noise
        r.adjust_for_ambient_noise(source, duration=1)

        # 2. Set a higher energy threshold
        r.energy_threshold = 3000

        # 3. Set a dynamic energy threshold
        r.dynamic_energy_threshold = True

        print("Talk now")
        audio = r.listen(source)

    try:
        # 4. Specify the language
        word = r.recognize_google(audio, language="en-US").lower()

        if assistant_name in word:
            activated = True
            word = word.replace(assistant_name, '').strip()

        if activated:
            conversation.append({"role": "user", "content": word})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            message = response["choices"][0]["message"]["content"]
            conversation.append({"role": "assistant", "content": message})
            audio = generate(
                text=message[:333],
                voice="Bella",
                model='eleven_multilingual_v1',
                api_key=elevenLabsAPIKey
            )
            play(audio)

            if "stop" in word:
                print("Stopping the program...")
                break

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        audio = generate(
            text="I'm sorry, I couldn't understand that. Could you please speak more clearly or loudly?",
            voice="Bella",
            model='eleven_multilingual_v1',
            api_key=elevenLabsAPIKey
        )
        play(audio)

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
