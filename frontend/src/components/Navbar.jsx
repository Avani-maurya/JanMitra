import { Link, useLocation } from "react-router-dom";
import {useState} from "react";
import { ChevronDown } from "lucide-react";

function Navbar() {
  const location = useLocation();
  const [languageOpen, setLanguageOpen] = useState(false);
const [language, setLanguage] = useState("EN");

  return (
    <header className="site-navbar">
      <div className="navbar-container">

        {/* Logo */}
        <Link to="/" className="navbar-brand">
          <div className="brand-mark">JM</div>

          <div className="brand-text">
            <strong>JanMitra AI</strong>
            <span>Your Citizen Assistant</span>
          </div>
        </Link>

        {/* Main Navigation */}
        <nav className="navbar-links">

          <Link
            to="/"
            className={location.pathname === "/" ? "active" : ""}
          >
            Home
          </Link>

          <Link
            to="/dashboard"
            className={
              location.pathname === "/dashboard" ? "active" : ""
            }
          >
            Dashboard
          </Link>

          <div className="nav-dropdown">
            <button type="button" className="nav-dropdown-button" onClick={() => setIsDropdownOpen(!isDropdownOpen)}>
              Services
              <ChevronDown size={15} />
            </button>

            <div className="nav-dropdown-menu">
              <Link to="/schemes">
                Government Schemes
              </Link>

              <Link to="/assistant">
                AI Citizen Assistant
              </Link>

              <Link to="/civic-report">
                Report Civic Issue
              </Link>

              <Link to="/voice">
                Voice Assistant
              </Link>
            </div>
          </div>

        </nav>

        {/* Right Side */}
        <div className="navbar-actions">

          <div className="language-selector">
  <button
    className="language-button"
    onClick={() => setLanguageOpen(!languageOpen)}
  >
    {language}
    <ChevronDown size={14} />
  </button>

  {languageOpen && (
    <div className="language-menu">
      <button
        onClick={() => {
          setLanguage("EN");
          setLanguageOpen(false);
        }}
      >
        English
      </button>

      <button
        onClick={() => {
          setLanguage("HI");
          setLanguageOpen(false);
        }}
      >
        हिंदी
      </button>

      <button
        onClick={() => {
          setLanguage("MR");
          setLanguageOpen(false);
        }}
      >
        मराठी
      </button>
    </div>
  )}
</div>

          <Link to="/login" className="navbar-login">
            Login
          </Link>

          <Link to="/dashboard" className="navbar-start">
            Get Started
          </Link>

        </div>

      </div>
    </header>
  );
}

export default Navbar;