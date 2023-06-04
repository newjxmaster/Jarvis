# Import necessary libraries
import speech_recognition as sr
import openai
from elevenlabs import generate, play

# Set the API keys for OpenAI and ElevenLabs
openai.api_key = 'Your OpenAi Api Key Here'
elevenLabsAPIKey = 'Your ElevenLabs Api Key Here'

# Instantiate the recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Initiate a conversation with the system's initial message
conversation = [
    {"role": "system", "content": "Your name is Jarvis and your purpose is to be an AI assistant"},
]

# Set the name of the assistant
assistant_name = "jarvis"

# The while loop will run indefinitely until you manually stop the program.
while True:
    # Use the microphone as the source for input audio
    with mic as source:
        # Adjust the recognizer sensitivity to ambient noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        # Prompt the user to speak
        print("Talk now")
        # Record the audio
        audio = r.listen(source)
    try:
        # Attempt to convert the audio into text using Google Speech Recognition
        word = r.recognize_google(audio).lower()

        # Check if the assistant's name is in the recognized speech
        if assistant_name in word:
            # Remove the assistant's name from the recognized speech
            word = word.replace(assistant_name, '').strip()

            # Add it to the conversation
            conversation.append({"role": "user", "content": word})
            # Use OpenAI's chat model to generate a response to the conversation so far
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            # Extract the response message from the API response
            message = response["choices"][0]["message"]["content"]
            # Add the AI's response to the conversation
            conversation.append({"role": "assistant", "content": message})
            # Use Eleven Labs to generate an audio message from the AI's response
            audio = generate(
                text=message[:333],
                voice="Bella",
                model='eleven_multilingual_v1',
                api_key=elevenLabsAPIKey
            )
            # Play the generated audio
            play(audio)

            # Termination condition
            if "stop" in word:
                print("Stopping the program...")
                break

    # If Google Speech Recognition could not understand the audio, handle the error
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        # Generate an audio message asking the user to speak more clearly or loudly
        audio = generate(
            text="I'm sorry, I couldn't understand that. Could you please speak more clearly or loudly?",
            voice="Bella",
            model='eleven_multilingual_v1',
            api_key=elevenLabsAPIKey
        )
        play(audio)
    # If there was an error in the request to Google Speech Recognition, handle the error
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
