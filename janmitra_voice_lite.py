"""
JanMitra AI - Voice Module LITE (Hindi + English)  |  pure Python libraries, no Ollama, no local AI server
=====================================================================================================
Pipeline:  speech -> text -> reply -> speech

  * Speech-to-text : SpeechRecognition (Google's free web recognizer)   [optional offline: faster-whisper]
  * Reply          : built-in bilingual knowledge base (schemes, helplines, complaints)
                     -> optionally Gemini API if you set GEMINI_API_KEY (your project already uses Gemini)
                     -> or plug in your own function / database lookup
  * Text-to-speech : gTTS (online)                                     [offline fallback: pyttsx3]

Works on any machine that can `pip install` the libraries below. Needs internet for the default engines.

SETUP
  pip install SpeechRecognition gTTS pygame sounddevice numpy requests av pyttsx3
  (web API only: pip install fastapi uvicorn python-multipart)
  (optional offline speech recognition: pip install faster-whisper, then set STT_ENGINE=whisper)

RUN
  python janmitra_voice_lite.py                     # talk with the microphone (auto Hindi/English)
  python janmitra_voice_lite.py --lang hi           # force Hindi (more reliable than auto)
  python janmitra_voice_lite.py --text              # type instead of speaking; reply is still spoken
  python janmitra_voice_lite.py --file clip.wav     # process an audio file (wav/mp3/webm/ogg...)
  uvicorn janmitra_voice_lite:app --port 8001       # web API for the frontend (docs at /docs)

USE FROM OTHER CODE
  from janmitra_voice_lite import VoiceAssistant
  bot = VoiceAssistant(brain=my_function, extra_knowledge=rows_from_db, on_interaction=save_to_db)
  result = bot.process_audio("clip.wav", session_id="user123")

HOOKS (all optional, nothing needs a backend until you connect it)
  brain(text, lang, history) -> str | None    your own reply logic (DB search, Gemini, scheme matcher...).
                                              Return None to fall through to the built-in answers.
  extra_knowledge = [{"kw": [...], "en": "...", "hi": "..."}]   add entries, e.g. loaded from MongoDB
  on_interaction(result, session_id)          called after every turn, e.g. save chat history
"""
import argparse
import base64
import difflib
import io
import logging
import os
import re
import tempfile
from dataclasses import dataclass
from typing import Callable, List, Optional

import numpy as np
import requests

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
logger = logging.getLogger("janmitra.voice")


# =============================================================================
# CONFIG
# =============================================================================
@dataclass
class Config:
    supported_languages: tuple = ("hi", "en")
    default_language: str = "en"

    # Speech-to-text engine: "google" (default, no download) or "whisper" (offline, needs faster-whisper)
    stt_engine: str = os.getenv("STT_ENGINE", "google")
    whisper_model: str = os.getenv("WHISPER_MODEL", "small")

    # Text-to-speech engine: "gtts" (online, natural voice) or "pyttsx3" (offline)
    tts_engine: str = os.getenv("TTS_ENGINE", "gtts")

    # Optional Gemini brain (used only when GEMINI_API_KEY is set). Free keys: aistudio.google.com
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")  # change to a current model if needed
    system_prompt: str = (
        "You are JanMitra AI, a friendly voice assistant for Indian citizens. You help with government "
        "schemes, public services and civic issues. Your answers are read aloud, so keep them to 1-3 short "
        "sentences in simple spoken language, with no markdown, lists, emojis or links. "
        "If unsure about a scheme's details, say so honestly instead of guessing."
    )
    max_history_turns: int = 6

    # Microphone (CLI only)
    sample_rate: int = 16000
    max_record_seconds: int = 20
    silence_seconds: float = 1.5
    silence_threshold: float = 0.01   # raise if your room is noisy


LANG_RULES = {
    "hi": "The user is speaking Hindi. Reply ONLY in Hindi using Devanagari script.",
    "en": "The user is speaking English. Reply ONLY in simple English.",
}

_DEVANAGARI = re.compile(r"[\u0900-\u097F]")
_EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")


# =============================================================================
# BUILT-IN KNOWLEDGE BASE  (add or edit entries freely; "w" = priority weight)
#   Matching: Latin keywords match whole words (typos tolerated), Devanagari keywords match as substrings.
# =============================================================================
KB = [
    {"id": "greeting", "w": 0.6,
     "kw": ["hello", "hi", "hey", "namaste", "namaskar", "good morning", "good evening", "नमस्ते", "नमस्कार", "हेलो", "हैलो"],
     "en": "Hello! I am JanMitra AI. I can help you with government schemes, helpline numbers and reporting civic problems. What would you like to know?",
     "hi": "नमस्ते! मैं जनमित्र AI हूँ। मैं सरकारी योजनाओं, हेल्पलाइन नंबर और नागरिक समस्याओं की शिकायत में आपकी मदद कर सकता हूँ। आप क्या जानना चाहेंगे?"},
    {"id": "how_are_you", "w": 1.0,
     "kw": ["how are you", "कैसे हैं", "कैसे हो", "आप कैसे"],
     "en": "I am doing well, thank you! How can I help you today?",
     "hi": "मैं ठीक हूँ, धन्यवाद! बताइए, मैं आपकी क्या मदद कर सकता हूँ?"},
    {"id": "thanks", "w": 0.6,
     "kw": ["thanks", "thank you", "thank", "धन्यवाद", "शुक्रिया"],
     "en": "You are welcome! Let me know if you need anything else.",
     "hi": "आपका स्वागत है! और कुछ जानना हो तो बताइए।"},
    {"id": "bye", "w": 0.6,
     "kw": ["bye", "goodbye", "see you", "अलविदा", "बाय"],
     "en": "Goodbye! Take care.",
     "hi": "अलविदा! अपना ध्यान रखिए।"},
    {"id": "capabilities", "w": 0.8,
     "kw": ["what can you do", "who are you", "help me", "help", "आप क्या कर सकते", "आप कौन", "कौन हो", "मदद"],
     "en": "I am JanMitra AI. I can tell you about government schemes, share emergency and helpline numbers, and guide you to report civic problems like potholes or garbage.",
     "hi": "मैं जनमित्र AI हूँ। मैं सरकारी योजनाओं की जानकारी दे सकता हूँ, आपातकालीन और हेल्पलाइन नंबर बता सकता हूँ, और गड्ढे या कचरे जैसी नागरिक समस्याओं की शिकायत में मार्गदर्शन कर सकता हूँ।"},
    {"id": "schemes", "w": 0.7,
     "kw": ["scheme", "yojana", "eligible", "eligibility", "benefit", "योजना", "योजनाएं", "योजनाओं", "पात्र", "लाभ"],
     "en": "I can guide you to schemes for students, farmers, women, senior citizens, health, housing and small businesses. Tell me about yourself, for example, I am a student, or I am a farmer, and I will suggest schemes.",
     "hi": "मैं छात्रों, किसानों, महिलाओं, बुजुर्गों, स्वास्थ्य, आवास और छोटे व्यापार की योजनाओं में आपकी मदद कर सकता हूँ। अपने बारे में बताइए, जैसे मैं छात्र हूँ या मैं किसान हूँ, और मैं योजनाएं सुझाऊँगा।"},
    {"id": "scholarship", "w": 1.0,
     "kw": ["scholarship", "student", "chhatravriti", "education", "college", "छात्रवृत्ति", "छात्र", "विद्यार्थी", "स्कॉलरशिप", "पढ़ाई", "शिक्षा"],
     "en": "Students can apply for central and state scholarships on the National Scholarship Portal at scholarships.gov.in. Eligibility depends on your course, category and family income. Keep your Aadhaar, marksheets, income certificate and bank details ready.",
     "hi": "छात्र राष्ट्रीय छात्रवृत्ति पोर्टल scholarships.gov.in पर केंद्र और राज्य सरकार की छात्रवृत्तियों के लिए आवेदन कर सकते हैं। पात्रता आपके कोर्स, श्रेणी और पारिवारिक आय पर निर्भर करती है। आधार, मार्कशीट, आय प्रमाण पत्र और बैंक खाते की जानकारी तैयार रखें।"},
    {"id": "farmer", "w": 1.0,
     "kw": ["kisan", "farmer", "farming", "agriculture", "pm kisan", "किसान", "खेती", "कृषि"],
     "en": "Under PM-KISAN, eligible farmer families get 6,000 rupees a year in three installments of 2,000 rupees, sent directly to their bank account. You can register at pmkisan.gov.in or at your nearest Common Service Centre.",
     "hi": "पीएम किसान योजना में पात्र किसान परिवारों को साल में 6,000 रुपये मिलते हैं, जो 2,000 रुपये की तीन किस्तों में सीधे बैंक खाते में आते हैं। आप pmkisan.gov.in पर या नज़दीकी कॉमन सर्विस सेंटर पर पंजीकरण करा सकते हैं।"},
    {"id": "health", "w": 1.0,
     "kw": ["ayushman", "health insurance", "hospital", "health card", "golden card", "treatment", "आयुष्मान", "अस्पताल", "स्वास्थ्य बीमा", "इलाज"],
     "en": "Ayushman Bharat PM-JAY gives eligible families health cover of up to 5 lakh rupees per year for hospital treatment. Check your eligibility at mera.pmjay.gov.in, call the helpline 14555, or visit the Ayushman Mitra desk at an empanelled hospital.",
     "hi": "आयुष्मान भारत पीएम-जेएवाई में पात्र परिवारों को अस्पताल में इलाज के लिए हर साल 5 लाख रुपये तक का स्वास्थ्य कवर मिलता है। पात्रता mera.pmjay.gov.in पर देखें, हेल्पलाइन 14555 पर कॉल करें, या सूचीबद्ध अस्पताल के आयुष्मान मित्र डेस्क पर जाएं।"},
    {"id": "housing", "w": 1.0,
     "kw": ["awas", "housing", "pmay", "house", "आवास", "मकान", "घर बनाने"],
     "en": "Pradhan Mantri Awas Yojana helps eligible families build or buy a pucca house, with separate schemes for urban and rural areas. Apply through your local municipal office, gram panchayat, or a Common Service Centre.",
     "hi": "प्रधानमंत्री आवास योजना पात्र परिवारों को पक्का घर बनाने या खरीदने में मदद करती है, शहरी और ग्रामीण क्षेत्रों के लिए अलग योजनाएं हैं। आप नगर निगम कार्यालय, ग्राम पंचायत या कॉमन सर्विस सेंटर के जरिए आवेदन कर सकते हैं।"},
    {"id": "lpg", "w": 1.0,
     "kw": ["ujjwala", "lpg", "gas cylinder", "gas connection", "उज्ज्वला", "उज्जवला", "सिलेंडर", "गैस"],
     "en": "Under the Ujjwala Yojana, women from eligible poor households can get an LPG gas connection with financial help from the government. Apply through your nearest LPG distributor with your Aadhaar and ration card.",
     "hi": "उज्ज्वला योजना में पात्र गरीब परिवारों की महिलाओं को सरकारी आर्थिक सहायता के साथ एलपीजी गैस कनेक्शन मिलता है। आधार और राशन कार्ड के साथ अपने नज़दीकी एलपीजी वितरक के पास आवेदन करें।"},
    {"id": "ration", "w": 1.0,
     "kw": ["ration", "ration card", "pds", "fair price", "राशन"],
     "en": "A ration card lets eligible families buy subsidised food grains from fair price shops. You can apply on your state food and civil supplies website, or at your nearest ration office or Common Service Centre.",
     "hi": "राशन कार्ड से पात्र परिवार उचित मूल्य की दुकान से रियायती अनाज खरीद सकते हैं। आप अपने राज्य के खाद्य एवं नागरिक आपूर्ति विभाग की वेबसाइट, नज़दीकी राशन कार्यालय या कॉमन सर्विस सेंटर पर आवेदन कर सकते हैं।"},
    {"id": "aadhaar", "w": 1.0,
     "kw": ["aadhaar", "aadhar", "uidai", "आधार"],
     "en": "For Aadhaar enrolment or updates, visit an Aadhaar centre or the UIDAI website at uidai.gov.in. The Aadhaar helpline number is 1947.",
     "hi": "आधार नामांकन या अपडेट के लिए किसी आधार केंद्र पर जाएं या uidai.gov.in वेबसाइट देखें। आधार हेल्पलाइन नंबर 1947 है।"},
    {"id": "pension", "w": 1.0,
     "kw": ["pension", "old age", "widow", "senior citizen", "elderly", "पेंशन", "वृद्धावस्था", "विधवा", "बुजुर्ग", "वरिष्ठ नागरिक"],
     "en": "Old age, widow and disability pensions are given under national and state schemes to eligible people. Apply through your gram panchayat, ward office or the state social welfare department with your Aadhaar, age proof, income proof and bank details.",
     "hi": "पात्र लोगों को राष्ट्रीय और राज्य योजनाओं के तहत वृद्धावस्था, विधवा और दिव्यांग पेंशन मिलती है। आधार, आयु प्रमाण, आय प्रमाण और बैंक विवरण के साथ ग्राम पंचायत, वार्ड कार्यालय या राज्य के समाज कल्याण विभाग में आवेदन करें।"},
    {"id": "bank", "w": 1.0,
     "kw": ["jan dhan", "jandhan", "bank account", "zero balance", "जन धन", "जनधन", "बैंक खाता", "खाता खुलवाना"],
     "en": "Under Pradhan Mantri Jan Dhan Yojana you can open a zero-balance bank account with a RuPay debit card and accident insurance cover. Visit any nearby bank branch or bank mitra with your Aadhaar.",
     "hi": "प्रधानमंत्री जन धन योजना में आप जीरो बैलेंस बैंक खाता खुलवा सकते हैं, जिसके साथ रुपे डेबिट कार्ड और दुर्घटना बीमा कवर मिलता है। आधार के साथ किसी भी नज़दीकी बैंक शाखा या बैंक मित्र के पास जाएं।"},
    {"id": "loan", "w": 1.0,
     "kw": ["mudra", "loan", "business", "startup", "self employment", "मुद्रा", "लोन", "ऋण", "कर्ज", "व्यापार", "कारोबार"],
     "en": "The MUDRA Yojana gives loans of up to 10 lakh rupees to small businesses, without collateral. You can apply at any bank or microfinance institution.",
     "hi": "मुद्रा योजना में छोटे व्यवसायों को बिना गारंटी के 10 लाख रुपये तक का लोन मिलता है। आप किसी भी बैंक या माइक्रोफाइनेंस संस्था में आवेदन कर सकते हैं।"},
    {"id": "skill", "w": 1.0,
     "kw": ["skill", "job", "jobs", "training", "employment", "rozgar", "कौशल", "नौकरी", "रोजगार", "प्रशिक्षण"],
     "en": "Skill India offers free short-term training courses with certificates under the Pradhan Mantri Kaushal Vikas Yojana. Visit skillindiadigital.gov.in or your nearest training centre, and check the National Career Service portal for job listings.",
     "hi": "स्किल इंडिया प्रधानमंत्री कौशल विकास योजना के तहत प्रमाणपत्र के साथ मुफ्त अल्पकालिक प्रशिक्षण देता है। skillindiadigital.gov.in या नज़दीकी प्रशिक्षण केंद्र पर जाएं, और नौकरियों के लिए नेशनल करियर सर्विस पोर्टल देखें।"},
    {"id": "women", "w": 1.0,
     "kw": ["women", "woman", "girl", "daughter", "mahila", "महिला", "महिलाओं", "बेटी", "लड़की"],
     "en": "Women can benefit from schemes like Ujjwala for LPG, Sukanya Samriddhi for a girl child's savings, and Mudra loans for business. For help or safety, call the women helpline 181.",
     "hi": "महिलाएं उज्ज्वला योजना, बेटी के लिए सुकन्या समृद्धि बचत योजना और व्यापार के लिए मुद्रा लोन जैसी योजनाओं का लाभ ले सकती हैं। मदद या सुरक्षा के लिए महिला हेल्पलाइन 181 पर कॉल करें।"},
    {"id": "complaint", "w": 1.2,
     "kw": ["complaint", "complain", "pothole", "garbage", "street light", "streetlight", "drain", "water supply", "report issue", "sewage",
            "शिकायत", "गड्ढा", "गड्ढे", "कचरा", "सड़क", "नाली", "स्ट्रीट लाइट", "पानी की समस्या"],
     "en": "You can report a civic problem like a pothole, garbage, a broken streetlight or a water leak using the Report Issue option in JanMitra. Take a photo, add the location and a short description, and you will get a complaint number to track it.",
     "hi": "आप जनमित्र में रिपोर्ट इश्यू विकल्प से गड्ढे, कचरे, खराब स्ट्रीट लाइट या पानी के रिसाव जैसी समस्या की शिकायत कर सकते हैं। फोटो लें, स्थान और छोटा विवरण जोड़ें, और ट्रैक करने के लिए आपको शिकायत नंबर मिलेगा।"},
    {"id": "emergency", "w": 1.2,
     "kw": ["emergency", "helpline", "police", "ambulance", "fire", "cyber", "fraud", "childline", "आपातकाल", "इमरजेंसी", "पुलिस", "एम्बुलेंस", "एंबुलेंस", "हेल्पलाइन", "साइबर", "धोखाधड़ी"],
     "en": "For any emergency, dial 112. Police is 100, ambulance is 108, fire is 101, women helpline is 181, child helpline is 1098, and for cyber fraud call 1930.",
     "hi": "किसी भी आपात स्थिति में 112 डायल करें। पुलिस 100, एम्बुलेंस 108, अग्निशमन 101, महिला हेल्पलाइन 181, चाइल्डलाइन 1098, और साइबर धोखाधड़ी के लिए 1930 पर कॉल करें।"},
]

NOT_UNDERSTOOD = {
    "en": "Sorry, I did not understand that. You can ask me about government schemes, scholarships, health cover, pensions, helpline numbers, or how to report a civic problem.",
    "hi": "क्षमा करें, मैं समझ नहीं पाया। आप मुझसे सरकारी योजनाओं, छात्रवृत्ति, स्वास्थ्य बीमा, पेंशन, हेल्पलाइन नंबर या नागरिक शिकायत के बारे में पूछ सकते हैं।",
}


# =============================================================================
# HELPERS
# =============================================================================
def detect_language(text: str, default: str = "en") -> str:
    """Hindi if the text is mostly Devanagari script, otherwise English."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return default
    return "hi" if len(_DEVANAGARI.findall(text)) / len(letters) > 0.3 else "en"


def clean_for_speech(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text)
    text = _EMOJI.sub("", text)
    text = re.sub(r"[*_`#>~|]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def to_pcm16(audio, rate: int = 16000) -> bytes:
    """
    Convert any audio input into raw 16-bit mono PCM at `rate` Hz.
    Accepts: numpy float array, file path, bytes, or file-like object (wav/mp3/webm/ogg/m4a... needs `av`).
    """
    if isinstance(audio, np.ndarray):
        return (np.clip(audio, -1, 1) * 32767).astype("<i2").tobytes()
    if isinstance(audio, (bytes, bytearray)):
        audio = io.BytesIO(audio)

    try:
        import av
    except ImportError:  # without `av` only 16 kHz mono 16-bit WAV files can be read
        import wave

        with wave.open(audio, "rb") as w:
            if (w.getframerate(), w.getnchannels(), w.getsampwidth()) != (rate, 1, 2):
                raise RuntimeError("Install the 'av' package (pip install av) to read this audio format.")
            return w.readframes(w.getnframes())

    out = []

    def collect(frames):
        if frames is None:
            return
        for f in frames if isinstance(frames, list) else [frames]:
            out.append(f.to_ndarray().tobytes())

    container = av.open(audio)
    resampler = av.AudioResampler(format="s16", layout="mono", rate=rate)
    for frame in container.decode(audio=0):
        collect(resampler.resample(frame))
    try:
        collect(resampler.resample(None))  # flush
    except Exception:
        pass
    container.close()
    return b"".join(out)


# =============================================================================
# SPEECH-TO-TEXT
# =============================================================================
class SpeechToText:
    _GOOGLE_CODES = {"hi": "hi-IN", "en": "en-IN"}

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._whisper = None

    def transcribe(self, audio, language: str = "auto"):
        """Returns (text, language). language: "auto" | "hi" | "en" (fixed is more reliable than auto)."""
        pcm = to_pcm16(audio, self.cfg.sample_rate)
        if len(pcm) < 3200:  # under 0.1 s of audio
            return "", self.cfg.default_language
        if self.cfg.stt_engine == "whisper":
            return self._whisper_stt(pcm, language)
        return self._google_stt(pcm, language)

    def _google_stt(self, pcm: bytes, language: str):
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        data = sr.AudioData(pcm, self.cfg.sample_rate, 2)
        candidates = [language] if language in self._GOOGLE_CODES else ["en"]

        best_score, best_text, best_lang = -1.0, "", self.cfg.default_language
        for lang in candidates:
            try:
                res = recognizer.recognize_google(data, language=self._GOOGLE_CODES[lang], show_all=True)
            except sr.RequestError as e:
                raise RuntimeError("Speech recognition service unreachable. Check your internet connection.") from e
            alts = res.get("alternative") if isinstance(res, dict) else None
            if not alts:
                continue
            text = (alts[0].get("transcript") or "").strip()
            if not text:
                continue
            score = float(alts[0].get("confidence", 0.5))
            if (lang == "hi") == (detect_language(text) == "hi"):  # script matches the language tried
                score += 0.1
            if score > best_score:
                best_score, best_text, best_lang = score, text, lang
        return best_text, best_lang

    def _whisper_stt(self, pcm: bytes, language: str):
        if self._whisper is None:
            from faster_whisper import WhisperModel

            self._whisper = WhisperModel(self.cfg.whisper_model, device="cpu", compute_type="int8")
        model, supported = self._whisper, self.cfg.supported_languages
        samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0

        segments, info = model.transcribe(samples, language=language if language in supported else None,
                                          beam_size=5, vad_filter=True)
        lang = info.language
        if lang not in supported:  # force a choice between Hindi and English
            probs = dict(getattr(info, "all_language_probs", None) or [])
            lang = max(supported, key=lambda l: probs.get(l, 0.0)) if any(probs.get(l) for l in supported) \
                else self.cfg.default_language
            segments, info = model.transcribe(samples, language=lang, beam_size=5, vad_filter=True)
        return " ".join(s.text.strip() for s in segments).strip(), lang


# =============================================================================
# BRAIN: knowledge-base matcher (+ optional Gemini)
# =============================================================================
def _has_keyword(text: str, tokens: List[str], kw: str) -> float:
    """Return match strength (0 = no match)."""
    kw = kw.lower()
    if _DEVANAGARI.search(kw):
        return 1.0 if kw in text else 0.0
    if re.search(r"\b" + re.escape(kw) + r"s?\b", text):
        return 1.0 + 0.5 * (len(kw.split()) - 1)  # multi-word phrases count more
    if " " not in kw and len(kw) >= 5 and difflib.get_close_matches(kw, tokens, n=1, cutoff=0.85):
        return 0.6  # tolerate small speech-recognition spelling errors
    return 0.0


def match_knowledge(text: str, lang: str, entries: List[dict]) -> Optional[str]:
    """Return the best-matching answer in the user's language, or None."""
    t = text.lower()
    tokens = re.findall(r"[a-z]+", t)
    best_score, best = 0.0, None
    for entry in entries:
        score = sum(_has_keyword(t, tokens, kw) for kw in entry["kw"]) * entry.get("w", 1.0)
        if score > best_score:
            best_score, best = score, entry
    if best is None:
        return None
    return best.get(lang) or best.get("en")


def gemini_reply(cfg: Config, text: str, lang: str, history: list) -> Optional[str]:
    """Optional: used only if GEMINI_API_KEY is set. Returns None if not configured."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    contents = [{"role": "user" if m["role"] == "user" else "model", "parts": [{"text": m["content"]}]}
                for m in history[-2 * cfg.max_history_turns:]]
    contents.append({"role": "user", "parts": [{"text": text}]})
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{cfg.gemini_model}:generateContent",
        headers={"x-goog-api-key": key},
        json={"system_instruction": {"parts": [{"text": cfg.system_prompt + " " + LANG_RULES.get(lang, "")}]},
              "contents": contents},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


# =============================================================================
# TEXT-TO-SPEECH
# =============================================================================
class TextToSpeech:
    def __init__(self, cfg: Config):
        self.cfg = cfg

    def synthesize(self, text: str, lang: str):
        """Returns (audio_bytes, 'mp3' | 'wav')."""
        text = clean_for_speech(text)
        if not text:
            raise ValueError("Nothing to speak.")
        if self.cfg.tts_engine == "pyttsx3":
            return self._pyttsx3(text, lang)
        try:
            return self._gtts(text, lang)
        except Exception as e:  # usually no internet -> offline fallback
            logger.warning("gTTS failed (%s). Falling back to pyttsx3.", e)
            return self._pyttsx3(text, lang)

    def _gtts(self, text, lang):
        from gtts import gTTS

        buf = io.BytesIO()
        gTTS(text=text, lang=lang, tld="co.in" if lang == "en" else "com").write_to_fp(buf)
        return buf.getvalue(), "mp3"

    def _pyttsx3(self, text, lang):
        import pyttsx3

        engine = pyttsx3.init()
        wanted = "hindi" if lang == "hi" else "english"
        for v in engine.getProperty("voices"):
            blob = f"{v.id} {v.name} {getattr(v, 'languages', '')}".lower()
            if wanted in blob or f"{lang}_" in blob or f"{lang}-" in blob:
                engine.setProperty("voice", v.id)
                break
        else:
            if lang == "hi":
                logger.warning("No Hindi voice installed for pyttsx3; use tts_engine='gtts' or install one.")
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        try:
            engine.save_to_file(text, path)
            engine.runAndWait()
            with open(path, "rb") as f:
                return f.read(), "wav"
        finally:
            os.remove(path)


# =============================================================================
# AUDIO I/O (CLI only; a web frontend records and plays audio in the browser)
# =============================================================================
def record_until_silence(cfg: Config):
    """Record from the default mic until the speaker pauses. Returns float32 array or None."""
    import sounddevice as sd

    step = 0.1
    chunk = int(cfg.sample_rate * step)
    frames, silent, started = [], 0, False
    with sd.InputStream(samplerate=cfg.sample_rate, channels=1, dtype="float32", blocksize=chunk) as stream:
        for _ in range(int(cfg.max_record_seconds / step)):
            data, _overflow = stream.read(chunk)
            data = data[:, 0]
            frames.append(data)
            if float(np.sqrt(np.mean(data ** 2))) > cfg.silence_threshold:
                started, silent = True, 0
            elif started:
                silent += 1
                if silent >= int(cfg.silence_seconds / step):
                    break
    return np.concatenate(frames) if started else None


def play_audio(audio_bytes: bytes, fmt: str = "mp3"):
    import pygame

    pygame.mixer.init()
    try:
        pygame.mixer.music.load(io.BytesIO(audio_bytes), fmt)
        pygame.mixer.music.play()
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(10)
    finally:
        pygame.mixer.quit()


# =============================================================================
# VOICE ASSISTANT (the class the rest of the team imports)
# =============================================================================
@dataclass
class VoiceResult:
    user_text: str = ""
    language: str = "en"
    reply_text: str = ""
    reply_language: str = "en"
    audio_bytes: Optional[bytes] = None
    audio_format: str = "mp3"
    source: str = ""              # which brain answered: custom | gemini | knowledge_base | not_understood
    error: Optional[str] = None   # non-fatal problem, e.g. "No speech detected."


class VoiceAssistant:
    def __init__(
        self,
        config: Optional[Config] = None,
        brain: Optional[Callable[[str, str, list], Optional[str]]] = None,
        extra_knowledge: Optional[List[dict]] = None,
        on_interaction: Optional[Callable[[VoiceResult, str], None]] = None,
    ):
        self.cfg = config or Config()
        self.stt = SpeechToText(self.cfg)
        self.tts = TextToSpeech(self.cfg)
        self.brain = brain
        self.knowledge = list(extra_knowledge or []) + KB   # your entries are checked alongside the built-ins
        self.on_interaction = on_interaction
        self._history = {}

    # ---- individual steps ------------------------------------------------
    def speech_to_text(self, audio, language: str = "auto"):
        return self.stt.transcribe(audio, language)

    def generate_reply(self, text: str, lang: str, session_id: str = "default"):
        """Returns (reply_text, source). Order: custom brain -> Gemini (if key set) -> knowledge base."""
        history = self._history.setdefault(session_id, [])
        reply, source = None, ""

        if self.brain:
            try:
                reply, source = self.brain(text, lang, history), "custom"
            except Exception as e:
                logger.warning("custom brain failed: %s", e)
        if not reply:
            try:
                reply, source = gemini_reply(self.cfg, text, lang, history), "gemini"
            except Exception as e:
                logger.warning("Gemini failed, using built-in answers: %s", e)
        if not reply:
            reply, source = match_knowledge(text, lang, self.knowledge), "knowledge_base"
        if not reply:
            reply, source = NOT_UNDERSTOOD.get(lang, NOT_UNDERSTOOD["en"]), "not_understood"

        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": reply})
        limit = 4 * self.cfg.max_history_turns
        if len(history) > limit:
            del history[:-limit]
        return reply, source

    def text_to_speech(self, text: str, lang: str):
        return self.tts.synthesize(text, lang)

    def reset_session(self, session_id: str = "default"):
        self._history.pop(session_id, None)

    # ---- full pipelines --------------------------------------------------
    def process_text(self, text: str, session_id: str = "default", lang: Optional[str] = None) -> VoiceResult:
        """Text in -> reply text + spoken audio out (skips speech-to-text)."""
        result = VoiceResult(user_text=text.strip())
        if not result.user_text:
            result.error = "Empty input."
            return result

        result.language = lang or detect_language(result.user_text, self.cfg.default_language)
        result.reply_text, result.source = self.generate_reply(result.user_text, result.language, session_id)
        result.reply_language = detect_language(result.reply_text, result.language)

        try:
            result.audio_bytes, result.audio_format = self.text_to_speech(result.reply_text, result.reply_language)
        except Exception as e:
            logger.error("TTS failed: %s", e)
            result.error = f"TTS failed: {e}"

        if self.on_interaction:
            try:
                self.on_interaction(result, session_id)
            except Exception as e:
                logger.warning("on_interaction failed: %s", e)
        return result

    def process_audio(self, audio, session_id: str = "default", language: str = "auto") -> VoiceResult:
        """MAIN ENTRY POINT: speech in -> transcript -> reply -> speech out."""
        text, lang = self.speech_to_text(audio, language)
        if not text:
            return VoiceResult(language=lang, error="No speech detected.")
        return self.process_text(text, session_id=session_id, lang=lang)


# =============================================================================
# WEB API (FastAPI), optional. Your backend can do:  app.include_router(create_router(bot))
# =============================================================================
def create_router(assistant: VoiceAssistant):
    from fastapi import APIRouter, File, Form, UploadFile
    from fastapi.concurrency import run_in_threadpool
    from pydantic import BaseModel

    router = APIRouter(prefix="/voice", tags=["voice"])

    def to_json(r: VoiceResult) -> dict:
        return {
            "user_text": r.user_text, "language": r.language,
            "reply_text": r.reply_text, "reply_language": r.reply_language, "source": r.source,
            "audio_base64": base64.b64encode(r.audio_bytes).decode() if r.audio_bytes else None,
            "audio_format": r.audio_format,  # JS: new Audio(`data:audio/${fmt};base64,${b64}`).play()
            "error": r.error,
        }

    class TextIn(BaseModel):
        text: str
        session_id: str = "default"
        language: Optional[str] = None  # "hi" or "en"; auto-detected if omitted

    @router.post("/chat")
    async def voice_chat(file: UploadFile = File(...), session_id: str = Form("default"), language: str = Form("auto")):
        """Upload recorded audio (webm/wav/mp3/ogg) -> transcript + reply text + reply audio."""
        data = await file.read()
        return to_json(await run_in_threadpool(assistant.process_audio, io.BytesIO(data), session_id, language))

    @router.post("/text")
    async def text_chat(body: TextIn):
        return to_json(await run_in_threadpool(assistant.process_text, body.text, body.session_id, body.language))

    @router.post("/transcribe")
    async def transcribe_only(file: UploadFile = File(...), language: str = Form("auto")):
        data = await file.read()
        text, lang = await run_in_threadpool(assistant.speech_to_text, io.BytesIO(data), language)
        return {"text": text, "language": lang}

    @router.post("/speak")
    async def speak_only(body: TextIn):
        audio, fmt = await run_in_threadpool(assistant.text_to_speech, body.text, body.language or "en")
        return {"audio_base64": base64.b64encode(audio).decode(), "audio_format": fmt}

    @router.post("/reset")
    async def reset(session_id: str = "default"):
        assistant.reset_session(session_id)
        return {"ok": True}

    return router


def create_app(assistant: Optional[VoiceAssistant] = None):
    """Standalone test server: uvicorn janmitra_voice_lite:app --port 8001"""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="JanMitra Voice Module")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    app.include_router(create_router(assistant or VoiceAssistant()))
    return app


try:
    app = create_app()
except Exception:  # fastapi / python-multipart not installed: CLI and library use still work
    app = None


# =============================================================================
# CLI
# =============================================================================
def _show_and_speak(result: VoiceResult):
    if result.user_text:
        print(f"\n You   [{result.language}]: {result.user_text}")
    if result.reply_text:
        print(f" Reply [{result.reply_language}] ({result.source}): {result.reply_text}")
    if result.error:
        print(f" (note: {result.error})")
    if result.audio_bytes:
        play_audio(result.audio_bytes, result.audio_format)


def main():
    parser = argparse.ArgumentParser(description="JanMitra AI voice assistant (Hindi + English)")
    parser.add_argument("--text", action="store_true", help="type input instead of using the microphone")
    parser.add_argument("--file", help="path to an audio file to process")
    parser.add_argument("--lang", default="auto", choices=["auto", "hi", "en"], help="speech language (default: auto)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)
    bot = VoiceAssistant()
    mode = "Gemini + built-in answers" if os.getenv("GEMINI_API_KEY") else "built-in answers"
    print(f"JanMitra Voice Assistant ({mode}). Type 'q' or press Ctrl+C to quit.")

    if args.file:
        _show_and_speak(bot.process_audio(args.file, language=args.lang))
        return

    while True:
        try:
            if args.text:
                text = input("\nType: ").strip()
                if text.lower() in ("q", "quit", "exit"):
                    break
                result = bot.process_text(text)
            else:
                cmd = input("\nPress Enter and speak (or 'q' to quit): ").strip().lower()
                if cmd in ("q", "quit", "exit"):
                    break
                print(" Listening... (stop talking to finish)")
                audio = record_until_silence(bot.cfg)
                if audio is None:
                    print(" Didn't hear anything, try again.")
                    continue
                print(" Processing...")
                result = bot.process_audio(audio, language=args.lang)
            _show_and_speak(result)
        except KeyboardInterrupt:
            break
        except Exception as e:  # keep the loop alive on network/mic errors
            print(f" [error] {e}")
    print("\nBye!")


if __name__ == "__main__":
    main()
