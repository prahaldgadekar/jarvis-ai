"""
brain/input_processor.py - FAST VERSION
Voice: ambient noise calibrated once at startup, not every press.
"""

import speech_recognition as sr


# ── Spell Correction ─────────────────────────────────────────
def correct_spelling(text: str) -> str:
    try:
        from textblob import TextBlob
        return str(TextBlob(text).correct())
    except Exception:
        return text


# ── Voice Input ───────────────────────────────────────────────
class VoiceInput:
    """
    Calibrates microphone ONCE on creation, then listens fast.
    Create one instance and reuse it — don't create a new one each time.
    """
    _calibrated_threshold = None   # Class-level cache

    def __init__(self, language: str = "en-IN"):
        self.recognizer = sr.Recognizer()
        self.language   = language
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.6   # Stop listening 0.6s after speech ends (default 0.8)
        self.recognizer.phrase_threshold = 0.2

        # Use cached threshold if already calibrated
        if VoiceInput._calibrated_threshold is not None:
            self.recognizer.energy_threshold = VoiceInput._calibrated_threshold
        else:
            self._calibrate()

    def _calibrate(self):
        """Calibrate ambient noise once and cache it."""
        try:
            with sr.Microphone() as source:
                print("[Voice] Calibrating microphone (one time)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)  # 0.3s not 1s
                VoiceInput._calibrated_threshold = self.recognizer.energy_threshold
                print(f"[Voice] Calibrated. Threshold: {VoiceInput._calibrated_threshold:.0f}")
        except Exception as e:
            print(f"[Voice] Calibration failed: {e}")
            self.recognizer.energy_threshold = 300

    def listen_once(self, timeout: int = 6, phrase_limit: int = 12) -> str:
        with sr.Microphone() as source:
            print("[Voice] Listening...")
            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
                text = self.recognizer.recognize_google(audio, language=self.language)
                print(f"[Voice] Recognized: {text}")
                return text
            except sr.WaitTimeoutError:
                print("[Voice] No speech detected.")
                return ""
            except sr.UnknownValueError:
                print("[Voice] Could not understand.")
                return ""
            except sr.RequestError as e:
                print(f"[Voice] API error: {e}")
                return ""

    def listen_for_wake_word(self, wake_word: str = "jarvis") -> bool:
        text = self.listen_once(timeout=3, phrase_limit=5)
        return wake_word.lower() in text.lower()


# ── Command Classifier ────────────────────────────────────────
COMMAND_KEYWORDS = {
    "weather":   ["weather", "temperature", "forecast", "rain", "sunny", "humidity", "hot", "cold"],
    "news":      ["news", "headlines", "latest news", "today's news", "what's happening"],
    "system":    ["cpu", "ram", "memory", "battery", "disk", "system status", "storage", "performance"],
    "file":      ["find file", "search file", "open file", "read file", "where is", "locate"],
    "project":   ["create project", "new project", "make project", "generate project"],
    "code":      ["write code", "generate code", "create function", "implement", "debug", "fix code", "program"],
    "chat":      ["who are you", "what can you do", "hello", "hi", "hey", "how are you", "good morning", "good night"],
    "memory":    ["remember", "forget", "my preference", "i prefer", "i like", "save this"],
    "open_app":  ["open", "launch", "start app", "run app"],
    "calculate": ["calculate", "what is", "how much", "solve", "math", "plus", "minus", "multiply"],
}


def classify_command(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in COMMAND_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return category
    return "general"


def process_text_input(raw_text: str) -> dict:
    corrected = correct_spelling(raw_text.strip())
    intent    = classify_command(corrected)
    return {
        "original":  raw_text,
        "corrected": corrected,
        "intent":    intent,
    }