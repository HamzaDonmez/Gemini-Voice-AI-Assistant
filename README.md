 # Voice AI Assistant with Mood Detection # 

This project is a **Python-based voice and text AI assistant**.  
It can recognize speech, take manual input, detect your mood, and generate answers with the **Google Gemini API**.  
The assistant also keeps a **conversation log** and tries to adapt its tone based on how you feel.  

---

## Features ##
**Voice input** with hotkey (F7)
**Manual input** with hotkey (F8)
**Mood detection** (happy, sad, angry, calm, surprised, flirty, gamer, neutral)
**Google search integration**
 Saves all conversations into `conversation_log.txt`

---
## Installation ##

1. Clone the repository:  
   ```bash
   git clone https://github.com/HamzaDonmez/voice-ai-assistant.git
   cd voice-ai-assistant


2.- Install requirements:  
```bash
 pip install -r requirements.txt
```

3.-  Open the file FinalVer.py and add your Google API Key:
4. 
```bash
client = genai.Client(api_key="Your_Api_Key")
```
 ##USAGE:##

- Run the program:
```bash
python FinalVer.py
```

-  **Voice Input**  
  Hotkey: `F7` → Activates microphone listening (`listen_and_recognize()` in code).

-  **Manual Input**  
  Hotkey: `F8` → Lets you type directly (`manual_input()` in code).
  
- The assistant will answer back and log everything.


-  **Web Search**  
  If user says "Google", "search", or "on internet", it performs a Google search  
  (handled by `parse_intent()` and `webbrowser.open()`).

-  **Mood Detection**  
  Detects emotions from text: angry, sad, happy, calm, surprised, flirty, gamer, neutral.  
  (`detect_mood()` function decides based on keywords).  
  Example: Saying "I’m sad" sets mood = `"sad"`.

-  **Conversation Logging**  
  All dialogues are saved in `conversation_log.txt`.  
  (`append_log()` and `ensure_log_file()` functions handle this).

-  **Media Control** *(via keyboard events)*  
  Assistant can pause or play media with system hotkeys.  
  For example, sending `keyboard.send("play/pause media")` inside intent handling.  
  (You can expand `parse_intent()` to map words like "pause music" or "resume music").

-  **Volume Control**  
  Can adjust volume by percentage when instructed.  
  Example: "Set volume to 30%" → triggers system volume command (implemented in your OS section).  
  In code, you’d extend `parse_intent()` to detect "volume" + `%` and call system command.

-  **AI-Powered Responses**  
  Uses Google Gemini API (`get_ai_response()`) to generate contextual replies.  
  Takes mood + last 15 conversation lines into account.  

-  **Interrupt & Exit**  
  Stop the program anytime with `Ctrl+C`. (`KeyboardInterrupt` handling inside `main()` and `processing_loop()`).

The project uses:  

speechrecognition  

keyboard  

google-generativeai  

pyaudio  


- Feel free to fork, open issues, or improve the code. Any suggestions are welcome!

📌 Author

### Created by [Hamza Dönmez](https://github.com/HamzaDonmez) ###
