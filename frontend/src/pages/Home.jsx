import {
  ArrowRight,
  Bot,
  Building2,
  FileText,
  MapPin,
  Mic,
  ShieldCheck,
  Sparkles,
  Volume2,
} from "lucide-react";

import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import ServiceCard from "../components/ServiceCard";

function Home() {
  return (
    <>
      <Navbar />

      {/* ================= HERO ================= */}
      <main>
        <section className="hero" id="home">
          <div className="hero-container">

            <div className="hero-content">

              <div className="eyebrow">
                <Sparkles size={14} />
                AI-powered citizen assistance
              </div>

              <h1>
                Your needs.
                <br />
                <span>One intelligent</span> platform.
              </h1>

              <p className="hero-description">
                JanMitra AI helps you discover government schemes,
                get answers to your questions, report civic issues
                and interact through voice — all in one place.
              </p>

              <div className="hero-buttons">

                <Link to="/login" className="primary-btn">
                  Explore JanMitra
                  <ArrowRight size={17} />
                </Link>

                <Link to="/voice" className="secondary-btn">
                  <Mic size={17} />
                  Try Voice Assistant
                </Link>

              </div>

              <div className="trust-line">
                <ShieldCheck size={15} />
                Designed with accessibility and citizen convenience in mind
              </div>

            </div>

            {/* ================= AI PREVIEW ================= */}

            <div className="hero-visual">

              <div className="glow"></div>

              <div className="assistant-card">

                <div className="assistant-header">

                  <div className="assistant-profile">

                    <div className="assistant-icon">
                      <Bot size={21} />
                    </div>

                    <div>
                      <strong>JanMitra AI</strong>
                      <span>Online • Ready to help</span>
                    </div>

                  </div>

                  <div className="status-dot"></div>

                </div>

                <div className="chat-area">

                  <div className="message bot-message">
                    <Bot size={16} className="message-icon" />

                    <p>
                      Hello! How can I help you today?
                    </p>
                  </div>

                  <div className="message user-message">
                    <p>
                      Can I find government schemes for me?
                    </p>
                  </div>

                  <div className="message bot-message">
                    <Bot size={16} className="message-icon" />

                    <p>
                      Absolutely. Tell me a little about yourself
                      and I can help you find relevant schemes.
                    </p>
                  </div>

                </div>

                <Link
                  to="/assistant"
                  className="assistant-input"
                >
                  <span>Ask JanMitra anything...</span>

                  <span className="assistant-input-button">
                    <Mic size={16} />
                  </span>
                </Link>

              </div>

              {/* Floating Scheme Card */}

              <div className="floating-card scheme-float">

                <FileText size={19} />

                <div>
                  <strong>Relevant schemes</strong>
                  <span>Personalized assistance</span>
                </div>

              </div>

              {/* Floating Voice Card */}

              <div className="floating-card voice-float">

                <Volume2 size={19} />

                <div>
                  <strong>Voice enabled</strong>
                  <span>English • हिंदी</span>
                </div>

              </div>

            </div>

          </div>
        </section>

        {/* ================= SERVICES ================= */}

        <section className="services-section" id="services">

          <div className="section-container">

            <div className="section-heading">

              <div className="section-label">
                WHAT JANMITRA CAN DO
              </div>

              <h2>
                One platform for your everyday citizen needs.
              </h2>

              <p>
                Access multiple forms of citizen assistance through
                a simple, unified experience.
              </p>

            </div>

            <div className="services-grid">

              <ServiceCard
                icon={<Building2 size={28} />}
                title="Government Schemes"
                description="Discover government schemes and understand which ones may be relevant to you."
                action="Find Schemes"
                onClick={() => window.location.href = "/schemes"}
              />

              <ServiceCard
                icon={<Bot size={28} />}
                title="AI Citizen Assistant"
                description="Ask questions in natural language and get simple, conversational guidance."
                action="Ask JanMitra"
                onClick={() =>
                  window.location.href = "/assistant"
                }
              />

              <ServiceCard
                icon={<MapPin size={28} />}
                title="Report Civic Issues"
                description="Report potholes, water leaks, garbage and other civic problems easily."
                action="Report an Issue"
                onClick={() =>
                  window.location.href = "/civic-report"
                }
              />

              <ServiceCard
                icon={<Mic size={28} />}
                title="Multilingual Voice"
                description="Interact with JanMitra using voice in supported languages."
                action="Try Voice Assistant"
                onClick={() =>
                  window.location.href = "/voice"
                }
              />

            </div>

          </div>

        </section>

        {/* ================= HOW IT WORKS ================= */}

        <section className="how-section" id="how-it-works">

          <div className="section-container">

            <div className="section-heading center-heading">

              <div className="section-label">
                HOW IT WORKS
              </div>

              <h2>
                Simple. Intelligent. Accessible.
              </h2>

              <p>
                JanMitra is designed to make citizen assistance easier
                from the first interaction.
              </p>

            </div>

            <div className="steps">

              <div className="step">

                <div className="step-number">
                  01
                </div>

                <h3>
                  Tell us what you need
                </h3>

                <p>
                  Ask a question, select a service or speak to
                  JanMitra using voice.
                </p>

              </div>

              <div className="step-line"></div>

              <div className="step">

                <div className="step-number">
                  02
                </div>

                <h3>
                  JanMitra understands
                </h3>

                <p>
                  The platform processes your request and identifies
                  the appropriate assistance.
                </p>

              </div>

              <div className="step-line"></div>

              <div className="step">

                <div className="step-number">
                  03
                </div>

                <h3>
                  Get useful guidance
                </h3>

                <p>
                  Receive relevant information and guidance in a
                  simple, understandable format.
                </p>

              </div>

            </div>

          </div>

        </section>

        {/* ================= VISION ================= */}

        <section className="vision-section" id="about">

          <div className="vision-container">

            <div>

              <div className="section-label">
                OUR VISION
              </div>

              <h2>
                Making citizen services easier to discover.
              </h2>

            </div>

            <div className="vision-text">

              <p>
                JanMitra AI is designed as an intelligent assistance
                layer that helps citizens discover, understand and
                navigate relevant public services more easily.
              </p>

              <Link to="/dashboard" className="text-btn">
                Learn more about JanMitra
                <ArrowRight size={16} />
              </Link>

            </div>

          </div>

        </section>

      </main>

      {/* ================= FOOTER ================= */}

      <footer className="footer">

        <div className="footer-container">

          <div className="footer-brand">

            <div className="brand">

              <div className="brand-icon">
                <Bot size={21} />
              </div>

              <div>
                <div className="brand-name">
                  JanMitra AI
                </div>

                <div className="brand-tagline">
                  Your Citizen Assistant
                </div>
              </div>

            </div>

            <p className="footer-description">
              AI-powered assistance designed to make citizen services
              simpler and more accessible.
            </p>

          </div>

          <div className="footer-links">

            <a href="#home">Home</a>
            <a href="#services">Services</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#about">About</a>

          </div>

        </div>

        <div className="footer-bottom">

          <span>
            © 2026 JanMitra AI. Mini Project Prototype.
          </span>

          <span>
            Built for citizens.
          </span>

        </div>

      </footer>
    </>
  );
}

export default Home;