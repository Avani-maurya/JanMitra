import { useState } from "react";
import {
  ArrowLeft,
  Camera,
  CheckCircle,
  MapPin,
  Send,
  Upload,
} from "lucide-react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";

function CivicReport() {
  const [issueType, setIssueType] = useState("");
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [photo, setPhoto] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!issueType || !description || !location) {
      alert("Please fill in all required fields.");
      return;
    }

    setSubmitted(true);
  };

  if (submitted) {
    return (
      <div className="civic-page">
        <Navbar />

        <div className="civic-container">
          <div className="success-card">
            <div className="success-icon">
              <CheckCircle size={42} />
            </div>

            <div className="section-label">
              REPORT SUBMITTED
            </div>

            <h1>Thank you for reporting the issue.</h1>

            <p>
              Your civic issue has been recorded successfully.
              In the future, JanMitra will connect this report to
              the appropriate civic authority.
            </p>

            <div className="report-id">
              <span>Prototype Report ID</span>
              <strong>
                JM-{Date.now().toString().slice(-6)}
              </strong>
            </div>

            <div className="success-actions">
              <Link to="/dashboard" className="primary-btn">
                Back to Dashboard
              </Link>

              <button
                className="secondary-btn"
                onClick={() => setSubmitted(false)}
              >
                Report Another Issue
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="civic-page">
      <Navbar />

      <div className="civic-container">
        <Link to="/dashboard" className="back-link">
          <ArrowLeft size={17} />
          Back to Dashboard
        </Link>

        <div className="civic-header">
          <div className="module-icon">
            <MapPin size={28} />
          </div>

          <div>
            <div className="section-label">
              CIVIC ISSUE REPORTING
            </div>

            <h1>Report a civic issue.</h1>

            <p>
              Help improve your community by reporting potholes,
              water leaks, garbage and other civic problems.
            </p>
          </div>
        </div>

        <form
          className="civic-form"
          onSubmit={handleSubmit}
        >
          <div className="form-section">
            <h2>Issue details</h2>

            <p className="form-help">
              Provide basic information about the problem.
            </p>

            <div className="form-group">
              <label>
                Issue Type <span>*</span>
              </label>

              <select
                value={issueType}
                onChange={(e) => setIssueType(e.target.value)}
              >
                <option value="">
                  Select the issue type
                </option>

                <option value="pothole">
                  Pothole / Damaged Road
                </option>

                <option value="water">
                  Water Leak
                </option>

                <option value="garbage">
                  Garbage / Waste
                </option>

                <option value="streetlight">
                  Streetlight
                </option>

                <option value="drainage">
                  Drainage / Sewerage
                </option>

                <option value="other">
                  Other
                </option>
              </select>
            </div>

            <div className="form-group">
              <label>
                Description <span>*</span>
              </label>

              <textarea
                rows="5"
                placeholder="Describe the issue and any useful details..."
                value={description}
                onChange={(e) =>
                  setDescription(e.target.value)
                }
              />
            </div>
          </div>

          <div className="form-section">
            <h2>Location</h2>

            <p className="form-help">
              Tell us where the issue is located.
            </p>

            <div className="location-input">
              <MapPin size={19} />

              <input
                type="text"
                placeholder="Enter location or landmark"
                value={location}
                onChange={(e) =>
                  setLocation(e.target.value)
                }
              />
            </div>

            <button
              type="button"
              className="location-button"
              onClick={() => {
                if (navigator.geolocation) {
                  navigator.geolocation.getCurrentPosition(
                    (position) => {
                      setLocation(
                        `GPS: ${position.coords.latitude.toFixed(
                          5
                        )}, ${position.coords.longitude.toFixed(5)}`
                      );
                    },
                    () => {
                      alert(
                        "Unable to access your location. Please enter it manually."
                      );
                    }
                  );
                } else {
                  alert(
                    "Geolocation is not supported by this browser."
                  );
                }
              }}
            >
              <MapPin size={17} />
              Use My Current Location
            </button>
          </div>

          <div className="form-section">
            <h2>Add a photo</h2>

            <p className="form-help">
              A photo can help authorities understand the issue.
            </p>

            <label className="upload-box">
             <input
  type="file"
  accept="image/*"
  hidden
  onChange={(e) => {
    const file = e.target.files[0];

    if (file) {
      setPhoto(file);
    }
  }}
/>
{photo && (
  <div className="photo-preview">
    <img
      src={URL.createObjectURL(photo)}
      alt="Selected civic issue"
    />
    <span>{photo.name}</span>
  </div>
)}

              <div className="upload-icon">
                <Camera size={25} />
              </div>

              <strong>Upload an image</strong>

              <span>PNG, JPG or JPEG</span>

              <div className="upload-action">
                <Upload size={16} />
                Choose File
              </div>
            </label>
          </div>

          <div className="form-submit">
            <button
              type="submit"
              className="primary-btn"
            >
              <Send size={18} />
              Submit Civic Report
            </button>
          </div>
        </form>

        <div className="civic-note">
          Prototype: submitted reports are currently stored only
          within the frontend session. Backend persistence and
          authority integration will be added later.
        </div>
      </div>
    </div>
  );
}

export default CivicReport;