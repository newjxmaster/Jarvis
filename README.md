# J.A.R.V.I.S.

# Installation
### 1. Clone this repo
[`https://github.com/Years96/Jarvis.git`] (If you want to clone the original version from Years)
(https://github.com/newjxmaster/Jarvis.git) (If you want to clone my updated version)

### 2. Create a conda environment
```
conda create --name jarvis -y python=3.8
conda activate jarvis
python -m pip install --upgrade pip

```

### 3. Install dependencies
```
#ffplay" tool, which is a part of the "ffmpeg" suite of video and audio processing tools, isn't found on your system. The "elevenlabs" library is trying to use this tool to play the generated audio.
You need to install ffmpeg, which includes ffplay.
If you don't have Homebrew, you can install it by following the instructions on its website: https://brew.sh/

#macOS
pip install SpeechRecognition openai elevenlabs
brew install flac
brew install ffmpeg

```

### 4. Install the requirements
`pip install -r requirements.txt`

### 5. Using Jarvis
Fill in your keys for the OpenAI API and Elevenlabs API in the first few lines of 'jarvis.py'  
Run the program  
`python jarvis.py` (In VSCode just click the run button)
