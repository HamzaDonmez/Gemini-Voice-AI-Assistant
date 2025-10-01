# Voice AI Assistant with Mood Detection

This project is a **Python-based voice and text AI assistant**.  
It can recognize speech, take manual input, detect your mood, and generate answers with the **Google Gemini API**.  
The assistant also keeps a **conversation log** and tries to adapt its tone based on how you feel.  

---

## Features
**Voice input** with hotkey (F7)
**Manual input** with hotkey (F8)
**Mood detection** (happy, sad, angry, calm, surprised, flirty, gamer, neutral)
**Google search integration**
 Saves all conversations into `conversation_log.txt`

---
Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HamzaDonmez/voice-ai-assistant.git
   cd voice-ai-assistant


2. Install requirements:
```bash
 pip install -r requirements.txt
```

3. Open the file FinalVer.py and add your Google API Key:
```bash
client = genai.Client(api_key="Your_Api_Key")
```
 USAGE:

Run the program:
```bash
python FinalVer.py
```

Press F7 → Speak through your microphone.
Press F8 → Type manually.
The assistant will answer back and log everything.


The project uses:

speechrecognition
keyboard
google-generativeai
pyaudio

Feel free to fork, open issues, or improve the code. Any suggestions are welcome!

📌 Author

Created by Hamza Dönmez
