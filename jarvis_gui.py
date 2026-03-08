"""
jarvis_gui.py - COMPLETE REWRITE
Fixes: Hello Boss on open, TTS speaks all text,
       left/right chat bubbles, no special characters.
"""
import sys, os, math, threading, re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QScrollArea,
    QSizePolicy,
)
from PySide6.QtCore  import Qt, QTimer, QThread, Signal, QRectF
from PySide6.QtGui   import (
    QColor, QPainter, QPen, QBrush, QTextCursor, QPalette,
    QLinearGradient, QRadialGradient, QFont, QPixmap,
)
import base64

BG    = "#050912"
BG2   = "#080f1e"
CYAN  = "#00e5ff"
CYAN2 = "#0088cc"
CYAN3 = "#00ffcc"
GOLD  = "#ffd700"
DIM   = "#1a3050"
TEXT  = "#c8e8ff"
TDIM  = "#3a6080"

HUD_B64 = "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"


def clean_text(text: str) -> str:
    """Strip all markdown and special symbols from text."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]*`', '', text)
    # Remove markdown symbols one by one
    for ch in ['*', '#', '_', '`', '\\', '|', '^', '~', '[', ']', '{', '}', '<', '>', '@']:
        text = text.replace(ch, '')
    # Clean up extra blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ── Rotating HUD background ───────────────────────────────────
class HudBg(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._angle = 0.0
        self._angle2 = 0.0
        self._pulse = 0.0
        self._pdir  = 1
        img_data = base64.b64decode(HUD_B64)
        self._pix = QPixmap()
        self._pix.loadFromData(img_data)
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(30)

    def _tick(self):
        self._angle  = (self._angle  + 0.35) % 360
        self._angle2 = (self._angle2 - 0.18) % 360
        self._pulse += 0.04 * self._pdir
        if self._pulse >= 1 or self._pulse <= 0:
            self._pdir *= -1
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        w, h = self.width(), self.height()
        cx, cy = w//2, h//2
        grad = QRadialGradient(cx, cy, max(w,h)*0.7)
        grad.setColorAt(0, QColor(8,20,45,255))
        grad.setColorAt(1, QColor(5,9,18,255))
        p.fillRect(self.rect(), grad)
        if not self._pix.isNull():
            sz = int(min(w,h)*0.72)
            sc = self._pix.scaled(sz, sz, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            p.save(); p.translate(cx,cy); p.rotate(self._angle)
            p.setOpacity((140+50*self._pulse)/255)
            p.drawPixmap(-sz//2,-sz//2,sc); p.restore()
            sz2 = int(sz*0.70)
            sc2 = self._pix.scaled(sz2,sz2,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            p.save(); p.translate(cx,cy); p.rotate(self._angle2)
            p.setOpacity(0.28); p.drawPixmap(-sz2//2,-sz2//2,sc2); p.restore()
        p.setOpacity(0.035)
        pen = QPen(QColor(0,200,255)); pen.setWidth(1); p.setPen(pen)
        for y in range(0,h,4): p.drawLine(0,y,w,y)
        vig = QRadialGradient(cx,cy,max(w,h)*0.55)
        vig.setColorAt(0,QColor(0,0,0,0)); vig.setColorAt(1,QColor(0,0,0,200))
        p.setOpacity(1.0); p.fillRect(self.rect(),vig); p.end()


# ── Logo ──────────────────────────────────────────────────────
class Logo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52,52)
        self._a = 0.0
        t = QTimer(self); t.timeout.connect(self._tick); t.start(30)

    def _tick(self):
        self._a = (self._a+1.2)%360; self.update()

    def paintEvent(self, e):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        cx,cy,r = 26,26,22
        p.save(); p.translate(cx,cy); p.rotate(self._a)
        pen=QPen(QColor(CYAN),2); pen.setDashPattern([3,3]); p.setPen(pen)
        p.drawEllipse(QRectF(-r,-r,r*2,r*2)); p.restore()
        p.save(); p.translate(cx,cy); p.rotate(-self._a*1.5)
        pen2=QPen(QColor(CYAN3),1); pen2.setDashPattern([2,5]); p.setPen(pen2)
        p.drawEllipse(QRectF(-r*.65,-r*.65,r*1.3,r*1.3)); p.restore()
        g=QRadialGradient(cx,cy,10)
        g.setColorAt(0,QColor(0,229,255,220)); g.setColorAt(1,QColor(0,136,204,0))
        p.setBrush(QBrush(g)); p.setPen(Qt.NoPen)
        p.drawEllipse(QRectF(cx-10,cy-10,20,20))
        p.setPen(QPen(QColor("#ffffff"),2))
        p.setFont(QFont("Consolas",12,QFont.Bold))
        p.drawText(QRectF(0,0,52,52),Qt.AlignCenter,"J"); p.end()


# ── Wave ──────────────────────────────────────────────────────
class Wave(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.active = False
        self._ph = 0.0
        t=QTimer(self); t.timeout.connect(self._tick); t.start(35)

    def _tick(self):
        if self.active: self._ph+=0.20; self.update()

    def set_active(self,v): self.active=v; self.update()

    def paintEvent(self,e):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(),QColor(0,0,0,0))
        w,h=self.width(),self.height(); cy=h//2
        if not self.active:
            p.setPen(QPen(QColor(TDIM),1)); p.drawLine(20,cy,w-20,cy)
            p.end(); return
        for amp,spd,col,wid in [(12,1.0,CYAN,2),(6,1.7,CYAN3,1)]:
            p.setPen(QPen(QColor(col),wid))
            px,py=0,cy
            for x in range(0,w,3):
                y=int(cy+amp*math.sin(x/w*4*math.pi+self._ph*spd))
                if x>0: p.drawLine(px,py,x,y)
                px,py=x,y
        p.end()


# ── Glow line ─────────────────────────────────────────────────
class GlowLine(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent); self.setFixedHeight(2)
    def paintEvent(self,e):
        p=QPainter(self)
        g=QLinearGradient(0,0,self.width(),0)
        g.setColorAt(0,QColor(0,0,0,0)); g.setColorAt(0.3,QColor(CYAN))
        g.setColorAt(0.7,QColor(CYAN3)); g.setColorAt(1,QColor(0,0,0,0))
        p.fillRect(self.rect(),g); p.end()


# ── Chat bubble ───────────────────────────────────────────────
class ChatBubble(QWidget):
    def __init__(self, sender: str, text: str, is_jarvis: bool, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.PlainText)
        label.setMaximumWidth(520)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        if is_jarvis:
            label.setStyleSheet(f"""
                QLabel {{
                    background: rgba(0,60,100,200);
                    color: {TEXT};
                    border: 1px solid {CYAN2};
                    border-radius: 12px;
                    border-top-left-radius: 2px;
                    padding: 10px 14px;
                    font-size: 12px;
                    font-family: Consolas;
                }}
            """)
            name = QLabel("JARVIS")
            name.setStyleSheet(f"color:{CYAN}; font-size:9px; font-weight:bold; letter-spacing:2px; background:transparent;")
            col = QVBoxLayout()
            col.setSpacing(2)
            col.addWidget(name)
            col.addWidget(label)
            layout.addLayout(col)
            layout.addStretch()
        else:
            label.setStyleSheet(f"""
                QLabel {{
                    background: rgba(180,130,0,160);
                    color: #ffffff;
                    border: 1px solid {GOLD};
                    border-radius: 12px;
                    border-top-right-radius: 2px;
                    padding: 10px 14px;
                    font-size: 12px;
                    font-family: Consolas;
                }}
            """)
            name = QLabel("YOU")
            name.setAlignment(Qt.AlignRight)
            name.setStyleSheet(f"color:{GOLD}; font-size:9px; font-weight:bold; letter-spacing:2px; background:transparent;")
            col = QVBoxLayout()
            col.setSpacing(2)
            col.addWidget(name)
            col.addWidget(label)
            col.setAlignment(Qt.AlignRight)
            layout.addStretch()
            layout.addLayout(col)


# ── Chat area with bubbles ────────────────────────────────────
class ChatArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet(f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{ background:{BG2}; width:5px; border-radius:2px; }}
            QScrollBar::handle:vertical {{ background:{DIM}; border-radius:2px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
        """)
        self._container = QWidget()
        self._container.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(4, 8, 4, 8)
        self._layout.setSpacing(6)
        self._layout.addStretch()
        self.setWidget(self._container)

    def add_message(self, sender: str, text: str, is_jarvis: bool):
        text = clean_text(text)
        bubble = ChatBubble(sender, text, is_jarvis)
        self._layout.insertWidget(self._layout.count()-1, bubble)
        QTimer.singleShot(50, lambda: self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        ))


# ── Brain + TTS threads ───────────────────────────────────────
class BrainThread(QThread):
    done = Signal(str)
    def __init__(self, brain, text):
        super().__init__()
        self.brain = brain; self.text = text
    def run(self):
        self.done.emit(self.brain.process(self.text))


class TTSThread(QThread):
    def __init__(self, tts, text):
        super().__init__()
        self.tts = tts; self.text = text
    def run(self):
        if self.tts and self.tts.available:
            self.tts.speak(clean_text(self.text), blocking=True)


class PreloadThread(QThread):
    weather_ready = Signal(str)
    def run(self):
        try:
            from api.weather import format_weather
            self.weather_ready.emit(format_weather())
        except Exception as e:
            self.weather_ready.emit(f"Weather unavailable")


# ── Stat card ─────────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, icon, label, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba(0,40,80,180);
                border: 1px solid {DIM};
                border-radius: 8px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10,7,10,7); lay.setSpacing(1)
        top = QHBoxLayout()
        ico = QLabel(icon)
        ico.setStyleSheet(f"color:{CYAN}; font-size:12px; background:transparent; border:none;")
        lbl = QLabel(label.upper())
        lbl.setStyleSheet(f"color:{TDIM}; font-size:8px; letter-spacing:2px; background:transparent; border:none;")
        top.addWidget(ico); top.addWidget(lbl); top.addStretch()
        lay.addLayout(top)
        self.val = QLabel("Loading...")
        self.val.setStyleSheet(f"color:{TEXT}; font-size:10px; font-weight:bold; background:transparent; border:none;")
        lay.addWidget(self.val)

    def set_value(self, t): self.val.setText(t)


# ── Main Window ───────────────────────────────────────────────
class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.brain = None
        self.tts   = None
        self._brain_thread = None
        self._tts_threads  = []
        self.setWindowTitle("JARVIS")
        self.setMinimumSize(1050, 700)
        self._style()
        self._build()
        self._clock_timer = QTimer(self)
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start(1000)
        self._tick_clock()
        QTimer.singleShot(100, self._lazy_load)

    def _style(self):
        pal = QPalette()
        pal.setColor(QPalette.Window,     QColor(BG))
        pal.setColor(QPalette.WindowText, QColor(TEXT))
        pal.setColor(QPalette.Base,       QColor(BG2))
        pal.setColor(QPalette.Text,       QColor(TEXT))
        self.setPalette(pal)
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background:{BG}; color:{TEXT};
                font-family:Consolas,'Courier New',monospace; }}
            QLineEdit {{
                background:rgba(0,20,50,200); border:1px solid {CYAN2};
                border-radius:8px; padding:9px 14px; color:{TEXT}; font-size:13px;
            }}
            QLineEdit:focus {{ border:1px solid {CYAN}; }}
        """)

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        self._hud = HudBg(central)
        self._hud.setGeometry(0,0,2000,2000)

        root = QVBoxLayout(central)
        root.setContentsMargins(14,10,14,10)
        root.setSpacing(7)

        # Header
        hdr = QHBoxLayout(); hdr.setSpacing(12)
        hdr.addWidget(Logo())
        tcol = QVBoxLayout(); tcol.setSpacing(0)
        t = QLabel("J.A.R.V.I.S")
        t.setFont(QFont("Consolas",20,QFont.Bold))
        t.setStyleSheet(f"color:{CYAN}; letter-spacing:8px; background:transparent;")
        tcol.addWidget(t)
        s = QLabel("JUST A RATHER VERY INTELLIGENT SYSTEM")
        s.setStyleSheet(f"color:{TDIM}; font-size:8px; letter-spacing:4px; background:transparent;")
        tcol.addWidget(s)
        hdr.addLayout(tcol); hdr.addStretch()
        rcol = QVBoxLayout(); rcol.setAlignment(Qt.AlignRight)
        self.clock_lbl = QLabel()
        self.clock_lbl.setStyleSheet(f"color:{CYAN}; font-size:11px; letter-spacing:2px; background:transparent;")
        self.clock_lbl.setAlignment(Qt.AlignRight)
        rcol.addWidget(self.clock_lbl)
        self.status_dot = QLabel("INITIALIZING")
        self.status_dot.setStyleSheet(f"color:#ffaa00; font-size:9px; letter-spacing:3px; background:transparent;")
        self.status_dot.setAlignment(Qt.AlignRight)
        rcol.addWidget(self.status_dot)
        hdr.addLayout(rcol)
        root.addLayout(hdr)
        root.addWidget(GlowLine())
        self.wave = Wave()
        root.addWidget(self.wave)

        # Content
        content = QHBoxLayout(); content.setSpacing(12)

        # Chat panel
        chat_frame = QFrame()
        chat_frame.setStyleSheet(f"""
            QFrame {{ background:rgba(5,12,30,160); border:1px solid {DIM}; border-radius:10px; }}
        """)
        cfl = QVBoxLayout(chat_frame); cfl.setContentsMargins(0,0,0,0); cfl.setSpacing(0)
        ch_lbl = QLabel("  COMMUNICATION CHANNEL")
        ch_lbl.setStyleSheet(f"""
            color:{TDIM}; font-size:9px; letter-spacing:3px;
            background:rgba(0,40,80,120); border-bottom:1px solid {DIM};
            border-radius:10px 10px 0 0; padding:6px 12px;
        """)
        cfl.addWidget(ch_lbl)
        self.chat_area = ChatArea()
        cfl.addWidget(self.chat_area)
        content.addWidget(chat_frame, stretch=3)

        # Right panel
        right = QVBoxLayout(); right.setSpacing(8)

        def sec(txt):
            l=QLabel(f"  {txt}")
            l.setStyleSheet(f"color:{CYAN}; font-size:9px; letter-spacing:3px; background:transparent;")
            return l

        right.addWidget(sec("SYSTEM METRICS"))
        g1=QHBoxLayout(); g1.setSpacing(6)
        self.cpu_c=StatCard("CPU","cpu"); self.ram_c=StatCard("RAM","ram")
        g1.addWidget(self.cpu_c); g1.addWidget(self.ram_c); right.addLayout(g1)
        g2=QHBoxLayout(); g2.setSpacing(6)
        self.bat_c=StatCard("PWR","power"); self.net_c=StatCard("NET","network")
        g2.addWidget(self.bat_c); g2.addWidget(self.net_c); right.addLayout(g2)

        right.addWidget(sec("ENVIRONMENT"))
        self.weather_lbl=QLabel("Fetching weather...")
        self.weather_lbl.setWordWrap(True)
        self.weather_lbl.setStyleSheet(f"""
            color:{TEXT}; font-size:10px; background:rgba(0,40,80,120);
            border:1px solid {DIM}; border-left:2px solid {CYAN3};
            border-radius:6px; padding:8px 10px;
        """)
        right.addWidget(self.weather_lbl)

        right.addWidget(sec("QUICK ACCESS"))
        for icon,label,cmd in [
            ("W","Weather",   "what is the weather today"),
            ("N","Tech News", "show me latest technology news"),
            ("S","System",    "show system status"),
            ("P","Projects",  "list my projects"),
        ]:
            btn=QPushButton(f"  {icon}  {label}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background:rgba(0,50,100,160); color:{CYAN};
                    border:1px solid {DIM}; border-left:2px solid {CYAN};
                    border-radius:6px; padding:7px 10px;
                    font-size:11px; text-align:left; letter-spacing:1px;
                }}
                QPushButton:hover {{ background:rgba(0,100,180,200); color:#fff; }}
            """)
            btn.clicked.connect(lambda _,c=cmd: self._send(c))
            right.addWidget(btn)

        right.addStretch()
        content.addLayout(right, stretch=1)
        root.addLayout(content, stretch=1)
        root.addWidget(GlowLine())

        # Input row
        inp=QHBoxLayout(); inp.setSpacing(8)
        lbl=QLabel(">");lbl.setStyleSheet(f"color:{CYAN};font-size:14px;background:transparent;")
        inp.addWidget(lbl)
        self.input_field=QLineEdit()
        self.input_field.setPlaceholderText("Enter command or query...")
        self.input_field.returnPressed.connect(self._on_send)
        inp.addWidget(self.input_field)

        for text,slot,style in [
            ("EXECUTE", self._on_send, f"background:{CYAN2};color:#fff;border:none;border-radius:8px;padding:9px 20px;font-weight:bold;font-size:11px;letter-spacing:2px;"),
            ("VOICE",   self._on_voice,f"background:rgba(0,30,60,200);color:{CYAN3};border:1px solid {CYAN3};border-radius:8px;padding:9px 14px;font-size:11px;"),
        ]:
            b=QPushButton(text); b.setStyleSheet(f"QPushButton{{{style}}}"); b.clicked.connect(slot)
            inp.addWidget(b)
            if text=="EXECUTE":
                b.setStyleSheet(f"QPushButton{{{style}}}QPushButton:hover{{background:{CYAN};color:#000;}}")
            if text=="VOICE":
                self.voice_btn=b

        clr=QPushButton("X"); clr.setFixedWidth(36)
        clr.setStyleSheet(f"QPushButton{{background:rgba(40,10,10,200);color:#ff4444;border:1px solid #441111;border-radius:8px;font-size:13px;}}QPushButton:hover{{background:rgba(255,50,50,40);}}")
        clr.clicked.connect(self._clear)
        inp.addWidget(clr)
        root.addLayout(inp)

        self.status_bar=QLabel("INITIALIZING SYSTEMS...")
        self.status_bar.setStyleSheet(f"color:{TDIM};font-size:9px;letter-spacing:2px;background:transparent;")
        root.addWidget(self.status_bar)

        # Stats timer
        self._stats_timer=QTimer(); self._stats_timer.timeout.connect(self._stats); self._stats_timer.start(4000)
        QTimer.singleShot(2500,self._stats)

    def resizeEvent(self,e):
        super().resizeEvent(e); self._hud.setGeometry(0,0,self.width(),self.height())

    def _tick_clock(self):
        self.clock_lbl.setText(datetime.now().strftime("%d.%m.%Y  %H:%M:%S"))

    def _stats(self):
        try:
            from tools.system_tools import get_cpu_usage,get_ram_usage,get_battery_status,get_network_info
            cpu=get_cpu_usage(); ram=get_ram_usage(); bat=get_battery_status(); net=get_network_info()
            self.cpu_c.set_value(f"{cpu['percent']}%  {cpu['cores']} cores")
            self.ram_c.set_value(f"{ram['used_gb']} / {ram['total_gb']} GB")
            self.bat_c.set_value(f"{bat['percent']}% CHARGING" if bat.get('available') and bat.get('plugged_in') else (f"{bat['percent']}%" if bat.get('available') else "DESKTOP"))
            self.net_c.set_value(net.get('local_ip','N/A'))
        except Exception: pass

    # ── Lazy load ─────────────────────────────────────────────
    def _lazy_load(self):
        self.input_field.setEnabled(False)
        self.status_bar.setText("LOADING AI CORE...")

        def _load():
            from brain.core import JarvisBrain
            from jarvis_tts import JarvisTTS
            self.brain = JarvisBrain()
            self.tts   = JarvisTTS()

        threading.Thread(target=_load, daemon=True).start()

        def _check():
            if self.brain is not None:
                self.input_field.setEnabled(True)
                self.status_dot.setText("ONLINE")
                self.status_dot.setStyleSheet(f"color:{CYAN3};font-size:9px;letter-spacing:3px;background:transparent;")
                self.status_bar.setText("ALL SYSTEMS OPERATIONAL")
                # Greeting — say it AND display it
                greeting = "Hello Boss. All systems are online. How can I assist you today?"
                self.chat_area.add_message("JARVIS", greeting, is_jarvis=True)
                self._speak(greeting)
                self._pre=PreloadThread()
                self._pre.weather_ready.connect(lambda t: self.weather_lbl.setText(clean_text(t)))
                self._pre.start()
            else:
                QTimer.singleShot(200, _check)

        QTimer.singleShot(200, _check)

    # ── Speak ─────────────────────────────────────────────────
    def _speak(self, text: str):
        """Speak text in background — never blocks UI."""
        t = TTSThread(self.tts, text)
        self._tts_threads.append(t)
        t.finished.connect(lambda: self._tts_threads.remove(t) if t in self._tts_threads else None)
        t.start()

    # ── Send ──────────────────────────────────────────────────
    def _send(self, text: str):
        self.input_field.setText(text)
        self._on_send()

    def _on_send(self):
        text = self.input_field.text().strip()
        if not text or not self.brain:
            return
        self.input_field.clear()
        self.chat_area.add_message("YOU", text, is_jarvis=False)
        self.wave.set_active(True)
        self.status_bar.setText("PROCESSING...")
        self.status_dot.setText("THINKING")
        self.status_dot.setStyleSheet(f"color:{GOLD};font-size:9px;letter-spacing:3px;background:transparent;")
        self.input_field.setEnabled(False)
        self._brain_thread = BrainThread(self.brain, text)
        self._brain_thread.done.connect(self._on_response)
        self._brain_thread.start()

    def _on_response(self, resp: str):
        self.wave.set_active(False)
        self.chat_area.add_message("JARVIS", resp, is_jarvis=True)
        self.status_bar.setText("READY")
        self.status_dot.setText("ONLINE")
        self.status_dot.setStyleSheet(f"color:{CYAN3};font-size:9px;letter-spacing:3px;background:transparent;")
        self.input_field.setEnabled(True)
        self.input_field.setFocus()
        self._speak(resp)  # Speak every response

    # ── Voice ─────────────────────────────────────────────────
    def _on_voice(self):
        self.voice_btn.setText("LISTENING")
        self.voice_btn.setEnabled(False)
        self.wave.set_active(True)
        self.status_bar.setText("LISTENING... SPEAK NOW")

        def _listen():
            try:
                from brain.input_processor import VoiceInput
                vi=VoiceInput(); text=vi.listen_once(timeout=6,phrase_limit=12)
            except Exception: text=""
            self._voice_result=text
            from PySide6.QtCore import QMetaObject
            QMetaObject.invokeMethod(self,"_on_voice_done",Qt.QueuedConnection)

        threading.Thread(target=_listen,daemon=True).start()

    def _on_voice_done(self):
        text=getattr(self,"_voice_result","")
        self.voice_btn.setText("VOICE"); self.voice_btn.setEnabled(True)
        self.wave.set_active(False)
        if text: self.input_field.setText(text); self._on_send()
        else: self.status_bar.setText("VOICE: NOTHING HEARD. TRY AGAIN")

    # ── Clear ─────────────────────────────────────────────────
    def _clear(self):
        # Remove all bubbles
        layout = self.chat_area._layout
        while layout.count() > 1:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        if self.brain: self.brain.clear_memory()
        self.chat_area.add_message("JARVIS","Memory cleared. Ready for new session Boss.",is_jarvis=True)


# ── Entry ─────────────────────────────────────────────────────
def run_gui():
    app=QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    pal=QPalette()
    pal.setColor(QPalette.Window,QColor(BG)); pal.setColor(QPalette.WindowText,QColor(TEXT))
    pal.setColor(QPalette.Base,QColor(BG2)); pal.setColor(QPalette.Text,QColor(TEXT))
    app.setPalette(pal)
    w=JarvisWindow(); w.show()
    sys.exit(app.exec())

if __name__=="__main__":
    run_gui()