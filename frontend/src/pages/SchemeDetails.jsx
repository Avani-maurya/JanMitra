import { ArrowLeft, FileText, CheckCircle } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";

function SchemeDetails() {
  const location = useLocation();

  const scheme = location.state?.scheme || {
    title: "Education Support Scheme",
    description:
      "Financial assistance for eligible students pursuing education.",
    eligibility:
      "Eligibility depends on age, occupation, income and applicable scheme criteria.",
    documents: [
      "Aadhaar Card",
      "Income Certificate",
      "Education / Student ID",
      "Bank Account Details",
    ],
  };

  return (
    <div className="module-page">
      <Navbar />

      <div className="module-container">

        <Link to="/schemes" className="back-link">
          <ArrowLeft size={17} />
          Back to Schemes
        </Link>

        <div className="module-header">
          <div className="module-icon">
            <FileText size={28} />
          </div>

          <div>
            <div className="section-label">
              SCHEME DETAILS
            </div>

            <h1>{scheme.title}</h1>

            <p>{scheme.description}</p>
          </div>
        </div>

        <div className="scheme-form">

          <h2>About this scheme</h2>

          <p>
            {scheme.description}
          </p>

          <h3>Eligibility</h3>

          <p>
            {scheme.eligibility}
          </p>

          <h3>Required Documents</h3>

          <div className="documents-list">
            {scheme.documents.map((document, index) => (
              <div
                className="document-item"
                key={index}
              >
                <CheckCircle size={18} />
                <span>{document}</span>
              </div>
            ))}
          </div>

          <div className="scheme-actions">

            <button
              className="primary-btn"
              type="button"
            >
              Apply / Learn More
            </button>

            <Link
              to="/schemes"
              className="secondary-btn"
            >
              Back to Schemes
            </Link>

          </div>

        </div>

      </div>
    </div>
  );
}

export default SchemeDetails;