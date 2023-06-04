import speech_recognition as sr
import openai
from elevenlabs import generate, play

openai.api_key = 'Your OpenAi Api Key Here'
elevenLabsAPIKey = 'ElevenLabs Api Key Here

r = sr.Recognizer()
mic = sr.Microphone()

conversation = [
    {"role": "system", "content": "Your name is Bella and your purpose is to be a human-like assistant. The user's name is {user_name}."},
]

assistant_name = "bella"
activated = False

def play_greeting():
    greeting = "Hi, I am Bella. And you?"
    audio = generate(
        text=greeting,
        voice="Bella",
        model='eleven_multilingual_v1',
        api_key=elevenLabsAPIKey
    )
    play(audio)

def play_how_can_i_help():
    message = "How can I help you?"
    audio = generate(
        text=message,
        voice="Bella",
        model='eleven_multilingual_v1',
        api_key=elevenLabsAPIKey
    )
    play(audio)

def ask_for_name():
    play_greeting()
    print("Please say your name")
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 3000
        r.dynamic_energy_threshold = True
        audio = r.listen(source)

    try:
        name = r.recognize_google(audio, language="en-US").lower()
        return name
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def execute_task(task):
    if task == "open notepad":
        subprocess.run(["notepad.exe"])
    elif task == "type hello":
        pyautogui.typewrite("Hello")
    elif "search for" in task:
        search_query = task.replace("search for", "").strip()
        # Perform a search using the search_query
    # Add more tasks here

user_name = None
while user_name is None:
    user_name = ask_for_name()

conversation[0]["content"] = conversation[0]["content"].format(user_name=user_name)

play_how_can_i_help()

while True:
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 3000
        r.dynamic_energy_threshold = True
        print("Talk now")
        audio = r.listen(source)

    try:
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

            execute_task(message)

            for i in range(0, len(message), 5000):
                audio = generate(
                    text=message[i:i+5000],
                    voice="Bella",
                    model='eleven_multilingual_v1',
                    api_key=elevenLabsAPIKey
                )
                play(audio)

    except sr.UnknownValueError:
        if activated:
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
