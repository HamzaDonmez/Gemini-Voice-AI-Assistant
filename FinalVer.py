import speech_recognition as sr
import keyboard
import webbrowser
from google import genai
import os
import sys
import time
import threading
import subprocess
from queue import Queue
from datetime import datetime

# --------------------------------------------------------------------------
# GEMINI API Key
# --------------------------------------------------------------------------
try:
    client = genai.Client(api_key="Your_Api_Key")
except Exception as e:
    print(f"Error: Cannot connect Google API: {e}")
    client = None

listening_lock = threading.Lock()

LOG_FILE = "conversation_log.txt"
mood = "neutral"


def ensure_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=== Conversation Log ===\n")


def append_log(role, text):
    ensure_log_file()
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {role}: {text}\n")
    except Exception as e:
        print(f"Logging error: {e}")


def get_recent_log_lines(limit=15):
    ensure_log_file()
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines = [l.strip() for l in lines if not l.startswith("===")]
        return lines[-limit:]
    except Exception:
        return []


# MOOD DETECTION 
def detect_mood(user_text):
    lower = user_text.lower()

    if any(word in lower for word in ["stupid", "idiot", "hate", "angry", "mad", "damn"]):
        return "angry"
    elif any(word in lower for word in ["sad", "cry", "lonely", "depressed", "bad", "bored"]):
        return "sad"
    elif any(word in lower for word in ["thanks", "great", "perfect", "love it", "super", "very good", "well done"]):
        return "happy"
    elif any(word in lower for word in ["calm", "relaxed", "peace", "silent", "rest"]):
        return "calm"
    elif any(word in lower for word in ["how so", "what", "can't believe", "really?"]):
        return "surprised"
    elif any(word in lower for word in ["love", "my darling", "kiss", "sweet", "so beautiful"]):
        return "flirty"
    elif any(word in lower for word in ["game", "fps", "battle", "rank", "noob", "loser"]):
        return "gamer"
    else:
        return "neutral"


def format_assistant_name():
    return "\033[1m\033[95mV: \033[0m"


#INTENT PARSER 
def parse_intent(text):
    lower = text.lower()

    if "google" in lower or "search" in lower or "on internet" in lower:
        query = lower.replace("google", "").replace("search", "").replace("on internet", "").strip()
        return ("web_search", query)

    return ("other", text)


#  AI RESPONSE 
def get_ai_response(user_text):
    global mood
    if not client:
        return "Cannot reply due to API connection error."

    try:
        personality_prompt = (
            #"You can customize your AI personality here."
        )

        recent_log = get_recent_log_lines(15)
        history_text = "\n".join(recent_log)

        print("\n--- Sent history to API ---")
        print(history_text)
        print("---------------------------\n")

        safe_user_text = user_text.encode("utf-8", "ignore").decode("utf-8")
        safe_history = history_text.encode("utf-8", "ignore").decode("utf-8")

        full_prompt = (
            f"{personality_prompt}\n"
            f"Current mood: {mood}. "
            f"Adapt responses according to this mood.\n"
            f"Conversation history:\n{safe_history}\n\n"
            f"User's new input: {safe_user_text}"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=full_prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in Gemini request: {e}")
        return "Hmm, something went wrong."


# SPEECH RECOGNITION
def listen_and_recognize(queue: Queue):
    if not listening_lock.acquire(blocking=False):
        print("Already listening.")
        return

    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\nListening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        text = None
        try:
            text = r.recognize_google(audio, language="tr-TR")
        except sr.UnknownValueError:
            try:
                text = r.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                raise

        if text:
            print("You said:", text)
            append_log("User", text)
            queue.put(('text', text))

    except Exception as e:
        print(f"Listening error: {e}")
        queue.put(('msg', "Error while listening."))
    finally:
        listening_lock.release()


def manual_input(queue: Queue):
    try:
        sys.stdin.flush()
        text = input("\nType your input: ").strip()
        if text:
            append_log("User", text)
            queue.put(('text', text))
    except Exception as e:
        print(f"Manual input error: {e}")


def processing_loop(queue: Queue):
    print("Ready. Press F7 (voice) or F8 (manual).")

    while True:
        try:
            item = queue.get()
            if item is None:
                break

            ttype, payload = item
            if ttype == 'msg':
                print(payload)
                continue

            if ttype == 'text':
                text = payload.strip()

                global mood
                mood = detect_mood(text)

                intent, content = parse_intent(text)

                if intent == "open_app":
                    found = try_open_exe(content)
                    if found:
                        reply = f"Opening {content}..."
                    else:
                        reply = f"Sorry, I couldn't find anything named '{content}'."
                    print(f"{format_assistant_name()}: {reply}")
                    append_log("Assistant", reply)
                    continue

                elif intent == "web_search":
                    if content:
                        reply = f"Searching {content} on Google..."
                        webbrowser.open(f"https://www.google.com/search?q={content}")
                    else:
                        reply = "What exactly should I Google?"
                    print(f"{format_assistant_name()}: {reply}")
                    append_log("Assistant", reply)
                    continue

                print(f"{format_assistant_name()} is thinking...")
                answer = get_ai_response(text)
                print(f"{format_assistant_name()}: {answer}")
                append_log("Assistant", answer)

                for i in range(5, 0, -1):
                    sys.stdout.write(f"\rWaiting for next command: {i} seconds...")
                    sys.stdout.flush()
                    time.sleep(1)
                sys.stdout.write("\r" + " " * 50 + "\r")
                sys.stdout.flush()
                print("Ready. Press F7 or F8.")

        except KeyboardInterrupt:
            print("Stopped by user.")
            break


def main():
    if not client:
        print("Program terminated: No API client.")
        return

    print("Started. F7 (voice), F8 (manual). Ctrl+C to exit.")

    q = Queue()
    keyboard.add_hotkey('F7', lambda: threading.Thread(target=listen_and_recognize, args=(q,), daemon=True).start())
    keyboard.add_hotkey('F8', lambda: threading.Thread(target=manual_input, args=(q,), daemon=True).start())

    try:
        processing_loop(q)
    except KeyboardInterrupt:
        print("Program shutting down...")
    finally:
        q.put(None)


if __name__ == "__main__":
    main()
