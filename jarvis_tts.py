"""
jarvis_tts.py
-------------
Text-to-Speech output for JARVIS using pyttsx3.
"""

import threading


class JarvisTTS:
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self._configure()
            self.available = True
            print("[TTS] Text-to-speech ready.")
        except Exception as e:
            print(f"[TTS] Not available: {e}")
            self.available = False

    def _configure(self):
        voices = self.engine.getProperty("voices")
        # Try to pick an English voice
        for voice in voices:
            if "english" in voice.name.lower() or "en" in voice.id.lower():
                self.engine.setProperty("voice", voice.id)
                break
        self.engine.setProperty("rate",   160)   # Speed
        self.engine.setProperty("volume", 0.9)   # Volume

    def speak(self, text: str, blocking: bool = False):
        if not self.available:
            return
        # Limit long responses for TTS
        if len(text) > 500:
            text = text[:500] + "... and more."
        if blocking:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            thread = threading.Thread(target=self._speak_thread, args=(text,), daemon=True)
            thread.start()

    def _speak_thread(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def stop(self):
        if self.available:
            try:
                self.engine.stop()
            except Exception:
                pass