"""
brain/core.py - JARVIS Central Brain with all APIs
"""
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from brain.input_processor import process_text_input
from brain.executor        import execute_plan
from memory.memory_db      import save_message, get_recent_messages, initialize_db

FAST_ROUTES = {
    "weather": {"tasks":[{"id":1,"action":"get_weather","description":"weather","params":{}}],"summary":"weather"},
    "news":    {"tasks":[{"id":1,"action":"get_news","description":"news","params":{"category":"technology","count":5}}],"summary":"news"},
    "system":  {"tasks":[{"id":1,"action":"get_system_status","description":"system","params":{}}],"summary":"system"},
    "crypto":  {"tasks":[{"id":1,"action":"get_crypto","description":"crypto","params":{}}],"summary":"crypto"},
    "joke":    {"tasks":[{"id":1,"action":"get_joke","description":"joke","params":{}}],"summary":"joke"},
    "nasa":    {"tasks":[{"id":1,"action":"get_nasa","description":"nasa","params":{}}],"summary":"nasa"},
    "ip":      {"tasks":[{"id":1,"action":"get_ip_info","description":"ip","params":{}}],"summary":"ip"},
    "exchange":{"tasks":[{"id":1,"action":"get_exchange","description":"exchange","params":{}}],"summary":"exchange"},
}

def _llm(prompt, model="reasoning"):
    return {"tasks":[{"id":1,"action":"llm_response","description":prompt,"params":{"prompt":prompt,"model":model}}],"summary":"direct"}

class JarvisBrain:
    def __init__(self):
        initialize_db()
        print("[Brain] Ready.")

    def process(self, raw: str) -> str:
        if not raw.strip():
            return "Please say something Boss."

        processed   = process_text_input(raw)
        text        = processed["corrected"]
        intent      = processed["intent"]
        tl          = text.lower()
        print(f"[Brain] '{text}' | intent:{intent}")
        save_message("user", text)

        # ── Detect intent from keywords ───────────────────────
        plan = None

        # Wikipedia — check first since it needs the search term
        if any(w in tl for w in ["wikipedia","who is","what is","tell me about","explain","definition of"]):
            query = text
            for skip in ["wikipedia","who is","what is","tell me about","explain","definition of"]:
                query = query.lower().replace(skip,"").strip()
            plan = {"tasks":[{"id":1,"action":"wiki_search","description":text,"params":{"query":query}}],"summary":"wiki"}

        # Crypto
        elif any(w in tl for w in ["crypto","bitcoin","ethereum","btc","eth","coin","dogecoin","solana","bnb","xrp","price of"]):
            coin = "bitcoin"
            for c in ["bitcoin","btc","ethereum","eth","dogecoin","doge","solana","bnb","xrp"]:
                if c in tl:
                    coin = c; break
            if "top" in tl or "list" in tl:
                plan = {"tasks":[{"id":1,"action":"get_top_crypto","description":text,"params":{}}],"summary":"crypto"}
            else:
                plan = {"tasks":[{"id":1,"action":"get_crypto","description":text,"params":{"coin":coin}}],"summary":"crypto"}

        # Currency exchange
        elif any(w in tl for w in ["exchange rate","currency","convert","usd to","inr to","dollar","rupee","euro","gbp"]):
            from_c, to_c = "USD", "INR"
            currencies = {"usd":"USD","inr":"INR","eur":"EUR","gbp":"GBP","jpy":"JPY","aud":"AUD"}
            words = tl.split()
            found = [currencies[w] for w in words if w in currencies]
            if len(found) >= 2: from_c, to_c = found[0], found[1]
            elif len(found) == 1: from_c = found[0]
            plan = {"tasks":[{"id":1,"action":"get_exchange","description":text,"params":{"from":from_c,"to":to_c}}],"summary":"exchange"}

        # NASA
        elif any(w in tl for w in ["nasa","space","astronomy","planet","asteroid","picture of the day","apod"]):
            plan = {"tasks":[{"id":1,"action":"get_nasa","description":text,"params":{}}],"summary":"nasa"}

        # Joke
        elif any(w in tl for w in ["joke","funny","laugh","humor","tell me a joke"]):
            plan = {"tasks":[{"id":1,"action":"get_joke","description":text,"params":{}}],"summary":"joke"}

        # IP info
        elif any(w in tl for w in ["my ip","ip address","my location","where am i","internet provider","isp"]):
            plan = {"tasks":[{"id":1,"action":"get_ip_info","description":text,"params":{}}],"summary":"ip"}

        # Weather
        elif any(w in tl for w in ["weather","temperature","rain","humidity","forecast","hot","cold","wind"]):
            plan = FAST_ROUTES["weather"]

        # News
        elif any(w in tl for w in ["news","headline","latest","trending","article"]):
            plan = FAST_ROUTES["news"]

        # System
        elif any(w in tl for w in ["system","cpu","ram","battery","memory","disk","network","ip","status"]):
            plan = FAST_ROUTES["system"]

        # GitHub
        elif any(w in tl for w in ["github","my repos","my profile","repository"]):
            user = os.environ.get("GITHUB_USERNAME","")
            for w in tl.split():
                if w not in ["github","my","repos","profile","repository","show","check"]:
                    user = w; break
            plan = {"tasks":[{"id":1,"action":"get_github","description":text,"params":{"username":user}}],"summary":"github"}

        # Desktop / file actions
        elif any(w in tl for w in ["create file","make file","new file","create a file","make a file"]):
            name = text.lower()
            for skip in ["create file","make file","new file","create a file","make a file","on desktop","named","name","called","as"]:
                name = name.replace(skip,"").strip()
            plan = {"tasks":[{"id":1,"action":"create_desktop_file","description":text,"params":{"filename":name or "newfile"}}],"summary":"file"}

        elif any(w in tl for w in ["create folder","make folder","new folder"]):
            name = text.lower()
            for skip in ["create folder","make folder","new folder","on desktop","named","name","called","as"]:
                name = name.replace(skip,"").strip()
            plan = {"tasks":[{"id":1,"action":"create_desktop_folder","description":text,"params":{"foldername":name or "NewFolder"}}],"summary":"folder"}

        elif any(w in tl for w in ["list desktop","show desktop","what is on desktop","files on desktop"]):
            plan = {"tasks":[{"id":1,"action":"list_desktop","description":text,"params":{}}],"summary":"desktop"}

        elif any(w in tl for w in ["open notepad","open calculator","open paint","open explorer","open chrome","open vscode","open cmd","open eclipse"]):
            app = "notepad"
            for a in ["notepad","calculator","paint","explorer","chrome","vscode","cmd","eclipse"]:
                if a in tl: app=a; break
            plan = {"tasks":[{"id":1,"action":"open_app","description":text,"params":{"app":app}}],"summary":"app"}

        # Code
        elif intent == "code" or any(w in tl for w in ["write code","generate code","function","class","implement","debug","fix code","algorithm"]):
            plan = _llm(text, "coding")

        # Chat / general
        else:
            plan = _llm(text, "reasoning")

        try:
            response = execute_plan(plan)
        except Exception as e:
            response = f"Error: {e}"
            print(f"[Brain] Error: {e}")

        save_message("assistant", response)
        return response

    def get_history(self, limit=20):
        return get_recent_messages(limit=limit)

    def clear_memory(self):
        from memory.memory_db import clear_chat_history
        clear_chat_history()
        return "Memory cleared."