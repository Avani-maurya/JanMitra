import { useState } from "react";
import {
  ArrowLeft,
  Search,
  MapPin,
  CheckCircle,
} from "lucide-react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function Schemes() {
  const [age, setAge] = useState("");
  const [state, setState] = useState("");
  const [occupation, setOccupation] = useState("");
  const [incomeRange, setIncomeRange] = useState("");
  const [searched, setSearched] = useState(false);
  const [schemes, setSchemes] = useState([]);

  const findRelevantSchemes = () => {
    const results = [];

    // Student scheme
    if (occupation === "Student") {
      results.push({
        title: "Education Support Scheme",
        description:
          "Financial assistance for eligible students pursuing education.",
      });
    }

    // Farmer scheme
    if (occupation === "Farmer") {
      results.push({
        title: "Farmer Support Scheme",
        description:
          "Support program for eligible farmers based on applicable criteria.",
      });
    }

    // Low income scheme
    if (
      incomeRange === "Below ₹1 Lakh" ||
      incomeRange === "₹1–3 Lakh"
    ) {
      results.push({
        title: "Citizen Welfare Scheme",
        description:
          "Public assistance program for eligible citizens based on applicable criteria.",
      });
    }

    // General scheme for employee / self employed
    if (
      occupation === "Employee" ||
      occupation === "Self Employed"
    ) {
      results.push({
        title: "Citizen Services Support Scheme",
        description:
          "Public service support program for eligible citizens.",
      });
    }

    setSchemes(results);
    setSearched(true);
  };

  return (
    <div className="module-page">
      <Navbar />

      <div className="module-container">

        {/* Back button */}
        <Link to="/dashboard" className="back-link">
          <ArrowLeft size={17} />
          Back to Dashboard
        </Link>

        {/* Header */}
        <div className="module-header">

          <div className="module-icon">
            <Search size={28} />
          </div>

          <div>
            <div className="section-label">
              GOVERNMENT SCHEMES
            </div>

            <h1>Find schemes relevant to you.</h1>

            <p>
              Tell us a little about yourself and JanMitra can
              help identify schemes that may be relevant to your
              profile.
            </p>
          </div>

        </div>

        {/* Form */}
        <div className="scheme-form">

          <h2>Tell us about yourself</h2>

          <div className="form-grid">

            {/* Age */}
            <div className="form-group">
              <label>Age</label>

              <input
                type="number"
                placeholder="Enter your age"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                min="1"
                max="120"
              />
            </div>

            {/* State */}
            <div className="form-group">
              <label>State</label>

              <select
                value={state}
                onChange={(e) => setState(e.target.value)}
              >
                <option value="">
                  Select your state
                </option>

                <option value="Maharashtra">
                  Maharashtra
                </option>

                <option value="Delhi">
                  Delhi
                </option>

                <option value="Karnataka">
                  Karnataka
                </option>

                <option value="Gujarat">
                  Gujarat
                </option>

                <option value="Rajasthan">
                  Rajasthan
                </option>

                <option value="Uttar Pradesh">
                  Uttar Pradesh
                </option>
              </select>
            </div>

            {/* Occupation */}
            <div className="form-group">
              <label>Occupation</label>

              <select
                value={occupation}
                onChange={(e) =>
                  setOccupation(e.target.value)
                }
              >
                <option value="">
                  Select occupation
                </option>

                <option value="Student">
                  Student
                </option>

                <option value="Farmer">
                  Farmer
                </option>

                <option value="Employee">
                  Employee
                </option>

                <option value="Self Employed">
                  Self Employed
                </option>

                <option value="Other">
                  Other
                </option>
              </select>
            </div>

            {/* Income */}
            <div className="form-group">
              <label>Income Range</label>

              <select
                value={incomeRange}
                onChange={(e) =>
                  setIncomeRange(e.target.value)
                }
              >
                <option value="">
                  Select income range
                </option>

                <option value="Below ₹1 Lakh">
                  Below ₹1 Lakh
                </option>

                <option value="₹1–3 Lakh">
                  ₹1–3 Lakh
                </option>

                <option value="₹3–5 Lakh">
                  ₹3–5 Lakh
                </option>

                <option value="Above ₹5 Lakh">
                  Above ₹5 Lakh
                </option>
              </select>
            </div>

          </div>

          {/* Search Button */}
          <button
            className="primary-btn scheme-search-btn"
            onClick={findRelevantSchemes}
          >
            <Search size={18} />
            Find Relevant Schemes
          </button>

        </div>

        {/* Results */}
        <div className="results-section">

          <div className="section-heading">

            <div className="section-label">
              SCHEME RESULTS
            </div>

            <h2>
              Potentially relevant schemes
            </h2>

            <p>
              These are prototype results based on the
              information you provided. Actual eligibility
              should be verified using official scheme criteria.
            </p>

          </div>

          <div className="scheme-results">

            {!searched && (
              <p>
                Fill your profile and click
                "Find Relevant Schemes".
              </p>
            )}

            {searched && schemes.length === 0 && (
              <p>
                No potentially relevant schemes found
                for this profile.
              </p>
            )}

            {searched &&
              schemes.map((scheme, index) => (
                <div
                  className="scheme-result-card"
                  key={index}
                >

                  {/* Card top */}
                  <div className="scheme-result-top">

                    <div className="scheme-result-icon">
                      <CheckCircle size={22} />
                    </div>

                    <span className="relevance">
                      Potentially Relevant
                    </span>

                  </div>

                  {/* Title */}
                  <h3>
                    {scheme.title}
                  </h3>

                  {/* Description */}
                  <p>
                    {scheme.description}
                  </p>

                  {/* Meta */}
                  <div className="scheme-meta">

                    <span>
                      <MapPin size={15} />

                      {state
                        ? state
                        : "State / Central"}
                    </span>

                  </div>

                  {/* Details */}
                  <Link
  to="/scheme-details"
  state={{
    scheme: {
      title: scheme.title,
      description: scheme.description,
      eligibility:
        "Eligibility depends on age, occupation, income and applicable scheme criteria.",
      documents: [
        "Aadhaar Card",
        "Income Certificate",
        "Bank Account Details",
        "Relevant supporting documents",
      ],
    },
  }}
  className="text-btn"
>
  View Details

  <ArrowLeft
    size={15}
    style={{
      transform: "rotate(180deg)",
    }}
  />
</Link>

                </div>
              ))}

          </div>

        </div>

      </div>
    </div>
  );
}

export default Schemes;