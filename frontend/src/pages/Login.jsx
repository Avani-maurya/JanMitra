import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ArrowLeft, Lock, Mail, LogIn } from "lucide-react";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    setError("");

    // Frontend prototype login
    navigate("/dashboard");
  };

  return (
    <div className="login-page">

      <div className="login-card">

        <Link to="/" className="back-link">
          <ArrowLeft size={17} />
          Back to Home
        </Link>

        <div className="login-header">
          <div className="login-icon">
            <LogIn size={25} />
          </div>

          <h1>Welcome back</h1>

          <p>
            Login to continue using JanMitra AI citizen services.
          </p>
        </div>

        <form onSubmit={handleLogin} className="login-form">

          <div className="form-group">
            <label>Email Address</label>

            <div className="input-wrapper">
              <Mail size={17} />

              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="form-group"> 
            <div className="login-options">
  <label>
    <input type="checkbox" />
    Remember me
  </label>
<button
  type="button"
  className="forgot-btn"
  onClick={() => {
    alert("Password reset will be available after backend integration.");
  }}
>
  Forgot password?
</button>
  
</div>
            <label>Password</label>

            <div className="input-wrapper">
              <Lock size={17} />

              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          {error && (
            <p className="login-error">
              {error}
            </p>
          )}

          <button type="submit" className="primary-btn login-submit">
            Login
            <LogIn size={17} />
          </button>

        </form>

        <div className="login-note">
          This is a frontend prototype. Authentication will be
          connected to the backend later.
        </div>

      </div>

    </div>
  );
}

export default Login;