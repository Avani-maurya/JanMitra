import { useState ,useRef} from "react";
import {
  ArrowLeft,
  Bot,
  Mic,
  Send,
  Sparkles,
  User,
} from "lucide-react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function Assistant() {
  const [message, setMessage] = useState(""); 

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I'm JanMitra AI. How can I help you today?",
    },
  ]);

  const [language, setLanguage] = useState("English");
  const assistantLanguages = ["English", "हिंदी", "मराठी"];
  const [listening, setListening] = useState(false);

const recognitionRef = useRef(null);
const chatMessagesRef = useRef(null);



  const suggestions = [
    "Which government schemes can I apply for?",
    "How can I report a pothole?",
    "What documents do I need for a government service?",
    "Help me find a nearby essential service.",
  ];
  const [typing, setTyping] = useState(false);

  // --------------------------------
  // SMART ASSISTANT RESPONSE
  // --------------------------------

  const getAssistantResponse = (question) => {
    const text = question.toLowerCase();

    // Hindi language request
    if (
      text.includes("give response in hindi") ||
      text.includes("reply in hindi") ||
      text.includes("answer in hindi") ||
      text.includes("hindi") ||
      text.includes("हिंदी") ||
      text.includes("हिन्दी")
    ) {
      setLanguage("हिंदी");

      return "नमस्ते! मैं जनमित्र AI हूँ। आप मुझसे सरकारी योजनाओं, नागरिक समस्याओं, दस्तावेज़ों और नागरिक सेवाओं के बारे में पूछ सकते हैं।";
    }

    // Hindi government scheme
    if (
      text.includes("scheme") ||
      text.includes("yojana") ||
      text.includes("सरकारी योजना") ||
      text.includes("योजना")
    ) {
      if (language === "हिंदी") {
        return "मैं आपकी सरकारी योजनाएँ खोजने में मदद कर सकता हूँ। आपकी पात्रता जानने के लिए आपकी आय, व्यवसाय और अन्य जानकारी आवश्यक हो सकती है। Government Schemes सेक्शन में जाकर संबंधित योजनाएँ देखें।";
      }

      return "I can help you find government schemes based on your occupation, income and eligibility. Visit the Government Schemes section to check relevant schemes.";
    }

    // Pothole / road complaint
    if (
      text.includes("pothole") ||
      text.includes("road") ||
      text.includes("सड़क") ||
      text.includes("गड्ढा")
    ) {
      if (language === "हिंदी") {
        return "आप JanMitra के Report Civic Issue सेक्शन से सड़क या गड्ढे की शिकायत कर सकते हैं। समस्या का विवरण और स्थान दर्ज करके अपनी शिकायत जमा करें।";
      }

      return "You can report a pothole or road problem using the Report Civic Issue service. Add the issue description and location to submit your report.";
    }

    // Documents
    if (
      text.includes("document") ||
      text.includes("documents") ||
      text.includes("दस्तावेज") ||
      text.includes("कागज")
    ) {
      if (language === "हिंदी") {
        return "आवश्यक दस्तावेज़ सेवा या योजना के अनुसार अलग-अलग हो सकते हैं। आमतौर पर आधार कार्ड, आय प्रमाण पत्र और बैंक खाते की जानकारी मांगी जा सकती है। आधिकारिक आवश्यकताओं की पुष्टि जरूर करें।";
      }

      return "Required documents depend on the government service or scheme. Aadhaar, income proof and bank details are commonly requested, but always verify the official requirements.";
    }

    // Nearby services
    if (
      text.includes("nearby") ||
      text.includes("near me") ||
      text.includes("पास") ||
      text.includes("नजदीक") ||
      text.includes("near")
    ) {
      if (language === "हिंदी") {
        return "मैं आपके आसपास आवश्यक नागरिक सेवाएँ खोजने में मदद कर सकता हूँ। Location-based service search को backend से जोड़ा जाएगा।";
      }

      return "The nearby-service feature can help citizens find essential services based on their location. Location-based search will be connected to the backend in a later stage.";
    }

    // Greeting
    if (
      text.includes("hello") ||
      text.includes("hi") ||
      text.includes("hey") ||
      text.includes("namaste") ||
      text.includes("नमस्ते")
    ) {
      if (language === "हिंदी") {
        return "नमस्ते! मैं जनमित्र AI हूँ। मैं आपको सरकारी योजनाओं, नागरिक समस्याओं, दस्तावेज़ों और नागरिक सेवाओं के बारे में जानकारी देने में मदद कर सकता हूँ।";
      }

      return "Hello! I'm JanMitra AI. You can ask me about government schemes, civic issues, documents or citizen services.";
    }

    // Default response
    if (language === "हिंदी") {
      return "मैं सरकारी योजनाओं, नागरिक शिकायतों, दस्तावेज़ों और नागरिक सेवाओं के बारे में आपकी मदद कर सकता हूँ। कृपया इनमें से किसी विषय के बारे में पूछें।";
    }

    return "I can help with government schemes, civic complaints, documents and citizen services. Please try asking me about one of these.";
  };
  const startVoiceInput = () => {
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

  recognition.lang =
    language === "हिंदी"
      ? "hi-IN"
      : language === "मराठी"
      ? "mr-IN"
      : "en-IN";

  recognition.interimResults = false;
  recognition.continuous = false;

  recognition.onstart = () => {
    setListening(true);
  };

  recognition.onresult = (event) => {
    const spokenText = event.results[0][0].transcript;

    setMessage(spokenText);
    setListening(false);
    sendMessage(spokenText);
  };

  recognition.onerror = () => {
    setListening(false);
  };

  recognition.onend = () => {
    setListening(false);
  };

  recognitionRef.current = recognition;
  recognition.start();
};

  // --------------------------------
  // SEND MESSAGE
  // --------------------------------
const sendMessage = (text = message) => {
  const userMessage = text.trim();

  if (!userMessage || typing) return;

  setTyping(true);

  setMessages((previous) => [
    ...previous,
    { sender: "user", text: userMessage },
  ]);

  setMessage("");

  setTimeout(() => {
    const botResponse = getAssistantResponse(userMessage);

    setMessages((previous) => [
      ...previous,
      { sender: "bot", text: botResponse },
    ]);

    setTyping(false);
  }, 700);
};

  // --------------------------------
  // UI
  // --------------------------------

  return (
    <>
      <Navbar />

      <div className="assistant-page">
        <div className="assistant-page-container">

          {/* Back */}

          <Link to="/dashboard" className="back-link">
            <ArrowLeft size={17} />
            Back to Dashboard
          </Link>

          {/* Header */}

          <div className="assistant-page-header">

            <div className="module-icon">
              <Bot size={28} />
            </div>

            <div>
              <div className="section-label">
                AI CITIZEN ASSISTANT
              </div>

              <h1>Ask JanMitra anything.</h1>

              <p>
                Get simple, conversational guidance for everyday
                citizen needs.
              </p>
            </div>

          </div>

          {/* Chat */}

          <div className="chat-interface">

            {/* Top Bar */}

            <div className="chat-topbar">

              <div className="chat-profile">

                <div className="chat-bot-icon">
                  <Bot size={20} />
                </div>

                <div>
                  <strong>JanMitra AI</strong>

                  <span>
                    <span className="status-dot"></span>
                    Online
                  </span>
                </div>

              </div>
<div className="language-selector">
  <select
    value={language}
    onChange={(e) => {
      setLanguage(e.target.value);
      setMessages([
        {
          sender: "bot",
          text:
            e.target.value === "हिंदी"
              ? "नमस्ते! मैं जनमित्र AI हूँ। मैं आपकी नागरिक सेवाओं में मदद कर सकता हूँ।"
              : e.target.value === "मराठी"
              ? "नमस्कार! मी जनमित्र AI आहे. मी तुम्हाला नागरिक सेवांमध्ये मदत करू शकतो."
              : "Hello! I'm JanMitra AI. How can I help you today?",
        },
      ]);
    }}
  >
    {assistantLanguages.map((item) => (
      <option key={item} value={item}>
        {item}
      </option>
    ))}
  </select>
</div>
              s

            </div>
            <button
  type="button"
  className="clear-chat-button"
  onClick={() => {
    setMessages([
      {
        sender: "bot",
        text:
          language === "हिंदी"
            ? "नमस्ते! मैं जनमित्र AI हूँ। मैं आपकी कैसे मदद कर सकता हूँ?"
            : language === "मराठी"
            ? "नमस्कार! मी जनमित्र AI आहे. मी तुम्हाला कशी मदत करू शकतो?"
            : "Hello! I'm JanMitra AI. How can I help you today?",
      },
    ]);
    setMessage("");
    setTyping(false);
  }}
>
  Clear
</button>

            {/* Messages */}

            <div className="chat-messages">

              {messages.map((item, index) => (
                

                <div
                  key={index}
                  className={`chat-message ${
                    item.sender === "user"
                      ? "chat-user"
                      : "chat-bot"
                  }`}
                >

                  <div className="chat-avatar">

                    {item.sender === "user" ? (
                      <User size={17} />
                    ) : (
                      <Bot size={17} />
                    )}

                  </div>

                  <div className="chat-bubble">
                    {item.text}
                  </div>

                </div>

              ))}

            </div>
            {typing && (
  <div className="chat-message chat-bot">
    <div className="chat-avatar">
      <Bot size={17} />
    </div>

    <div className="chat-bubble typing-bubble">
      JanMitra is thinking...
    </div>
  </div>
)}

            {/* Suggestions */}

           {messages.length === 1 && !typing && (
  <div className="suggestions">
    <div className="suggestions-title">
      <Sparkles size={15} />
      Try asking
    </div>

    <div className="suggestion-list">
      {suggestions.map((suggestion) => (
        <button
          key={suggestion}
          onClick={() => sendMessage(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
  </div>
)}

            {/* Input */}

            <div className="chat-input-area">

              <input
                type="text"
                value={message}
                placeholder="Ask JanMitra anything..."
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    sendMessage();
                  }
                }}
              />

              {/* Voice */}
<button
  className={listening ? "voice-button listening" : "voice-button"}
  title={listening ? "Stop listening" : "Voice input"}
  type="button"
  onClick={startVoiceInput}
>
  <Mic size={19} />
</button>

              {/* Send */}
<button
  className="send-button"
  onClick={() => sendMessage()}
  title={typing ? "JanMitra is thinking..." : "Send message"}
  type="button"
  disabled={typing || !message.trim()}
>
  <Send size={19} />
</button>
        

            </div>

          </div>

          {/* Note */}

          <div className="assistant-note">

            <Sparkles size={15} />

            JanMitra AI provides assistance and guidance.
            Important information should be verified with official sources.

          </div>

        </div>
      </div>
    </>
  );
}

export default Assistant;