import { useState,useRef } from "react";
import {
  ArrowLeft,
  Bot,
  Check,
  Languages,
  Mic,
  Volume2,
} from "lucide-react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";


function VoiceAssistant() {
  const [language, setLanguage] = useState("English");
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const recognitionRef = useRef(null);
  const [processing, setProcessing] = useState(false);
  const [speechError, setSpeechError] = useState("");
  const languages = [
  { name: "English", code: "en-IN", available: true },
  { name: "हिंदी", code: "hi-IN", available: false },
  { name: "मराठी", code: "mr-IN", available: false },
];

  const startListening = () => {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert(
      "Speech recognition is not supported in this browser. Please try Google Chrome."
    );
    return;
  }

  if (listening) {
    recognitionRef.current?.stop();
    setListening(false);
    return;
  }

  const recognition = new SpeechRecognition();

  const languageCode =
    language === "हिंदी"
      ? "hi-IN"
      : language === "मराठी"
      ? "mr-IN"
      : "en-IN";

  recognition.lang = languageCode;
  recognition.interimResults = false;
  recognition.continuous = false;

  recognition.onstart = () => {
    setListening(true);
    setTranscript("");
    setResponse("");
    setProcessing(true);
  };
recognition.onresult = (event) => {
  const text = event.results[0][0].transcript;

  setTranscript(text);
let responseText = "";

const lowerText = text.toLowerCase();

if (
  lowerText.includes("scheme") ||
  lowerText.includes("yojana") ||
  lowerText.includes("योजना")
) {
  responseText =
    language === "हिंदी"
      ? "मैं आपको सरकारी योजनाओं के बारे में जानकारी देने में मदद कर सकता हूँ। पात्रता और आवश्यक दस्तावेज़ योजना के अनुसार अलग-अलग हो सकते हैं।"
      : language === "मराठी"
      ? "मी तुम्हाला सरकारी योजनांबद्दल माहिती देण्यास मदत करू शकतो. पात्रता आणि आवश्यक कागदपत्रे योजनेनुसार वेगवेगळी असू शकतात."
      : "I can help you find government schemes. Eligibility and required documents may vary depending on the scheme.";
} else if (
  lowerText.includes("pothole") ||
  lowerText.includes("road") ||
  lowerText.includes("गड्ढा") ||
  lowerText.includes("सड़क")
) {
  responseText =
    language === "हिंदी"
      ? "आप Report Civic Issue सेवा का उपयोग करके सड़क या गड्ढे की शिकायत दर्ज कर सकते हैं।"
      : language === "मराठी"
      ? "तुम्ही Report Civic Issue सेवेद्वारे रस्ता किंवा खड्ड्याची तक्रार नोंदवू शकता."
      : "You can report a pothole or road problem using the Report Civic Issue service.";
} else {
  responseText =
    language === "हिंदी"
      ? "मैं सरकारी योजनाओं, नागरिक सेवाओं और शिकायतों के बारे में आपकी मदद कर सकता हूँ।"
      : language === "मराठी"
      ? "मी सरकारी योजना, नागरिक सेवा आणि तक्रारींबद्दल तुम्हाला मदत करू शकतो."
      : "I can help you with government schemes, citizen services and civic complaints.";
}
  
  setResponse(responseText);
  setProcessing(false);
};
  

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    setListening(false);
  };

  recognition.onend = () => {
    setListening(false);
  };

  recognitionRef.current = recognition;
  recognition.start();
};

  return (

    <div className="voice-page">
      <Navbar />
      <div className="voice-container">

        {/* Back */}

        <Link to="/dashboard" className="back-link">
          <ArrowLeft size={17} />
          Back to Dashboard
        </Link>

        {/* Header */}

        <div className="voice-header">

          <div className="module-icon">
            <Languages size={28} />
          </div>

          <div>
            <div className="section-label">
              MULTILINGUAL VOICE
            </div>

            <h1>Talk to JanMitra.</h1>

            <p>
              Speak naturally in your preferred language and
              receive simple citizen assistance.
            </p>
          </div>

        </div>

        {/* Language Selection */}

        <div className="language-section">

          <div className="voice-section-title">
            <Languages size={19} />
            <div>
              <h2>Choose your language</h2>
              <p>Select the language you want to use.</p>
            </div>
          </div>

          <div className="language-options">

            {languages.map((item) => (
              <button
                key={item.code}
                className={
                  language === item.name
                    ? "language-option active"
                    : "language-option"
                }
                onClick={() => {
                  setLanguage(item.name);
                  setTranscript("");
                  setResponse("");
                  setSpeechError("");
                }}
              >
                {language === item.name && <Check size={16} />}
                {item.name||item.code}
              </button>
            ))}

          </div>

        </div>

        {/* Voice Interface */}

        <div className="voice-interface">

          <div className="voice-bot">

            <div className="voice-bot-icon">
              <Bot size={30} />
            </div>

            <h2>
  {listening
    ? "JanMitra is listening..."
    : processing
    ? "JanMitra is thinking..."
    : "How can I help you?"}
</h2>

            <p>
              {listening
                ? "Speak clearly and tell JanMitra what you need."
                : processing
                ? "Preparing a helpful response..."
                : `Language: ${language}`}
            </p>

          </div>

          <button
            className={
              listening
                ? "voice-mic listening"
                : "voice-mic"
            }
            onClick={startListening}
          >
            <Mic size={34} />
          </button>
        <div className="voice-status">
  {listening
    ? "Listening... Tap mic to stop"
    : processing
    ? "Preparing your response..."
    : response
    ? "Response ready"
    : "Tap the microphone to speak"}
</div>
          

        </div>

        {/* Transcript */}

        {transcript && (
          <div className="voice-result">

            <div className="result-heading">
              <Mic size={17} />
              <strong>You said</strong>
            </div>

            <p>{transcript}</p>

          </div>
        )}

        {/* Response */}

        {response && (
          <div className="voice-result assistant-result">

            <div className="result-heading">
              <Bot size={17} />
              <strong>JanMitra AI</strong>
            </div>

            <p>{response}</p>
            {speechError && (
  <div className="speech-error">
    {speechError}
  </div>
)}
            <div className="response-ready">
  <Check size={14} />
  Response ready
</div>
            

           <button
  className="speak-response"
  
  onClick={() => {
  if (!("speechSynthesis" in window)) {
    alert("Speech synthesis is not supported in this browser.");
    return;
  }

  const langCode =
    language === "हिंदी"
      ? "hi-IN"
      : language === "मराठी"
      ? "mr-IN"
      : "en-IN";

  const voices = window.speechSynthesis.getVoices();

  const matchingVoice = voices.find(
    (voice) =>
      voice.lang.toLowerCase() === langCode.toLowerCase()
  );

  if (!matchingVoice) {
  setSpeechError(
    `${language} voice is not available on this device/browser.`
  );
  return;
}

  const speech = new SpeechSynthesisUtterance(response);

  speech.lang = langCode;
  speech.voice = matchingVoice;

  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(speech);
}}
>
  <Volume2 size={17} />
  Listen to response
</button>

          </div>
        )}

        {/* Accessibility note */}

        <div className="voice-note">
          <Languages size={16} />

          <span>
            JanMitra is designed to support multilingual and
            voice-based citizen interaction. Additional languages
            and real speech processing will be integrated with
            the backend.
          </span>

        </div>

      </div>

    </div>
  );
}

export default VoiceAssistant;