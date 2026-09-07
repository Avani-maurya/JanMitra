import {
  FileText,
  Bot,
  MapPin,
  Mic,
  ArrowRight,
} from "lucide-react";
import { Link } from "react-router-dom";

import Navbar from "../components/Navbar";


function Dashboard() {
  const services = [
    {
      icon: FileText,
      title: "Government Schemes",
      description:
        "Find government schemes that may be relevant to your profile.",
      link: "/schemes",
    },
    {
      icon: Bot,
      title: "AI Citizen Assistant",
      description:
        "Ask questions and get simple conversational guidance.",
      link: "/assistant",
    },
    {
      icon: MapPin,
      title: "Report Civic Issue",
      description:
        "Report potholes, garbage, water leaks and other civic problems.",
      link: "/civic-report",
    },
    {
      icon: Mic,
      title: "Multilingual Voice",
      description:
        "Interact with JanMitra using voice in supported languages.",
      link: "/voice",
    },
  ]; 



  return (
    <div className="dashboard-page">
      <Navbar />

      <main className="dashboard-container">
      <div className="dashboard-section-heading">
  <div className="section-label">QUICK ACCESS</div>
  <h2>Your citizen services</h2>
  <p>Access JanMitra services quickly from your dashboard.</p>
</div> 

        {/* Header */}

        <div className="dashboard-header">
          <div>
            <div className="section-label">
              CITIZEN DASHBOARD
            </div>

            <h1>Welcome to JanMitra AI</h1>

            <p>
              Your simple digital assistant for everyday citizen
              services.
            </p>
          </div>

          <div className="dashboard-status">
            <span className="status-dot"></span>
            Services Online
          </div>
        </div>

        {/* Service Cards */}

        <div className="dashboard-grid">

          {services.map((service) => {
            const Icon = service.icon;

            return (
              <Link
                key={service.title}
                to={service.link}
                className="dashboard-card"
              >
                <div className="dashboard-card-icon">
                  <Icon size={25} />
                </div>

                <div className="dashboard-card-content">
                  <h2>{service.title}</h2>

                  <p>{service.description}</p>

                  <span className="dashboard-card-link">
                    Open Service
                    <ArrowRight size={16} />
                  </span>
                </div>
              </Link>
            );
          })}

        </div>
        <div className="dashboard-stats">
  <div>
    <strong>4</strong>
    <span>Citizen  Services</span>
  </div>

  <div>
    <strong>3</strong>
    <span>Languages</span>
  </div>

  <div>
    <strong>24/7</strong>
    <span>AI Assistance</span>
  </div>
</div>

        {/* Information */}
        

        <div className="dashboard-info">

          <div>
            <strong>Need help?</strong>

            <p>
              Ask JanMitra about government schemes, documents,
              civic complaints or citizen services.
            </p>
          </div>

          <Link to="/assistant" className="primary-btn">
            Ask JanMitra
            <ArrowRight size={16} />
          </Link>

        </div>

      </main>
    </div>
  );
}

export default Dashboard;