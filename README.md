<div align="center">

# ⚡ J.A.R.V.I.S
### Just A Rather Very Intelligent System

![Python](https://img.shields.io/badge/Python-3.11+-00e5ff?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-GUI-00ffcc?style=for-the-badge&logo=qt&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-ffd700?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0088cc?style=for-the-badge&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-00e5ff?style=for-the-badge)

**A cinematic AI desktop assistant inspired by Iron Man's JARVIS.**
**Runs 100% locally on your PC using Ollama — no cloud, no subscriptions.**

</div>

---

## Preview

> Rotating HUD interface · Voice input · Real-time system stats · Live APIs

```
[JARVIS] Hello Boss. All systems online. How can I assist you today?
[YOU]    what is the bitcoin price
[JARVIS] Bitcoin is currently at USD 67,420 | INR 56,23,450
[YOU]    create a file on desktop named project-ideas
[JARVIS] Done Boss. Created project-ideas.txt on your Desktop.
[YOU]    who is APJ Abdul Kalam
[JARVIS] APJ Abdul Kalam was an Indian aerospace scientist who served as the 11th President of India.
```

---

## Features

| Category | What JARVIS Can Do |
|---|---|
| **AI Chat** | Natural conversation using local Ollama models |
| **Voice** | Speak to JARVIS, hear responses via TTS |
| **Desktop Control** | Create files, folders, open apps on Windows |
| **Weather** | Live weather for your city |
| **News** | Latest tech headlines via NewsAPI |
| **Crypto** | Live Bitcoin, Ethereum, and top coin prices |
| **Wikipedia** | Instant knowledge lookup |
| **Currency** | Real-time exchange rates (USD, INR, EUR, etc.) |
| **NASA** | Astronomy Picture of the Day |
| **GitHub** | Look up any GitHub profile |
| **IP Info** | Your public IP and location |
| **System Stats** | Live CPU, RAM, Battery, Network |
| **Projects** | Generate Java, Python, C, C++ project templates |
| **Memory** | Remembers preferences across sessions |

---

## Project Structure

```
jarvis/
├── jarvis.py               # Entry point
├── jarvis_gui.py           # Cinematic PySide6 HUD
├── jarvis_tts.py           # Text-to-speech
├── START_JARVIS.bat        # One-click launcher (starts Ollama + JARVIS)
├── CREATE_SHORTCUT.bat     # Creates Desktop shortcut
├── requirements.txt
├── .env                    # Your API keys (not in git)
├── .env.example            # Template
│
├── api/
│   ├── weather.py          # OpenWeatherMap
│   ├── news.py             # NewsAPI
│   └── extras.py           # Crypto, Wikipedia, NASA, IP, Currency, GitHub
│
├── brain/
│   ├── core.py             # Central brain controller
│   ├── input_processor.py  # Voice + text processing
│   ├── planner.py          # LLM task planner
│   ├── router.py           # Routes to tools or LLM
│   └── executor.py         # Executes task plans
│
├── memory/
│   ├── memory_db.py        # SQLite memory system
│   └── jarvis_memory.db    # Auto-created
│
├── models/
│   └── llm_interface.py    # Ollama API calls
│
└── tools/
    ├── system_tools.py     # CPU, RAM, battery, network
    ├── search_tools.py     # File search and reading
    ├── project_tools.py    # Project generators
    └── windows_tools.py    # Desktop file and app control
```

---

## Installation

### Requirements
- Windows 10 or 11
- Python 3.11 or newer
- [Ollama](https://ollama.com) installed

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/jarvis-ai.git
cd jarvis-ai
```

### Step 2 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Install Ollama models
```bash
ollama pull phi3
ollama pull qwen2.5-coder:7b
```

### Step 4 — Set up your API keys
```bash
copy .env.example .env
```
Open `.env` and fill in your keys (see API Keys section below).

### Step 5 — Create Desktop shortcut (one time only)
```
Double-click CREATE_SHORTCUT.bat
```

### Step 6 — Launch JARVIS
```
Double-click the JARVIS shortcut on your Desktop
```
That is it. JARVIS starts Ollama automatically every time.

---

## API Keys

All APIs have free tiers. No credit card required.

| API | Get Key | Free Limit |
|---|---|---|
| OpenWeatherMap | [openweathermap.org/api](https://openweathermap.org/api) | 1000 calls/day |
| NewsAPI | [newsapi.org](https://newsapi.org) | 100 calls/day |
| NASA | [api.nasa.gov](https://api.nasa.gov) | Unlimited |
| GitHub | [github.com/settings/tokens](https://github.com/settings/tokens) | 5000/hour |

Crypto, Wikipedia, IP info, Currency, and Jokes work with **no API key at all**.

---

## Usage Examples

Just type or speak naturally:

```
weather                          → Live weather for your city
bitcoin price                    → Current BTC price in USD and INR
top crypto                       → Top 5 coins by market cap
who is Elon Musk                 → Wikipedia summary
tell me a joke                   → Programming joke
NASA picture today               → Astronomy picture of the day
my ip address                    → Your public IP and location
USD to INR                       → Live exchange rate
latest tech news                 → Top 5 headlines
system status                    → CPU, RAM, battery info
create file on desktop named X   → Creates X.txt on Desktop
create folder named Projects     → Creates folder on Desktop
open notepad                     → Opens Notepad
open calculator                  → Opens Calculator
write a Python function for X    → AI generates code
```

---

## Configuration

Edit your `.env` file:

```env
OPENWEATHER_API_KEY=your_key
NEWS_API_KEY=your_key
DEFAULT_CITY=Pune
OLLAMA_BASE_URL=http://localhost:11434
REASONING_MODEL=phi3
CODING_MODEL=qwen2.5-coder:7b
NASA_KEY=DEMO_KEY
GITHUB_USERNAME=your_github_username
WAKE_WORD=jarvis
```

---

## Voice Mode

Click the **VOICE** button or say the wake word. JARVIS will:
1. Listen for your command
2. Process it
3. Speak the response out loud

---

## Built With

- [PySide6](https://doc.qt.io/qtforpython/) — Desktop GUI
- [Ollama](https://ollama.com) — Local AI models
- [phi3](https://ollama.com/library/phi3) — Fast reasoning model
- [qwen2.5-coder](https://ollama.com/library/qwen2.5-coder) — Coding model
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Voice input
- [pyttsx3](https://pypi.org/project/pyttsx3/) — Text to speech
- [SQLite](https://www.sqlite.org/) — Memory storage

---

## Made By

**Prahlad** — Computer Engineering Student, Pune, India

---

<div align="center">
<i>All systems online. How can I assist you today, Boss?</i>
</div>
