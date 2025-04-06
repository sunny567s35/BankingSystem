import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../static/css/style.css";

const Login = ({ user, messages }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [verifying, setVerifying] = useState(false);

  if (user) {
    return <Navigate to={`/dashboard/${user.username}`} replace />;
  }

  const handleVerifyEmail = async () => {
    if (!email) {
      alert("Please enter an email address first!");
      return;
    }

    setVerifying(true);
    try {
      const response = await fetch("http://localhost:8000/send-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, purpose: "login" }),
      });

      const responseText = await response.text();
      const data = JSON.parse(responseText);

      if (data.success) {
        setOtpSent(true);
        alert("OTP sent to your email!");
      } else {
        alert("Error sending OTP: " + data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while sending OTP. Please try again.");
    } finally {
      setVerifying(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password || (otpSent && !otp)) {
      alert("Please fill in all fields!");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
          otp: otpSent ? otp : null,
          purpose: "login",
        }),
      });

      const responseText = await response.text();
      const data = JSON.parse(responseText);

      if (data.status === "success") {
        alert(data.message);
        localStorage.setItem("user", JSON.stringify(data.user));
        window.location.href = data.redirect;
      } else {
        alert(data.message || "Login failed");
        setOtp(""); // Clear OTP input if login fails
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("An error occurred during login. Please try again.");
    }
  };

  return (
    <div className="container py-4">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <h2 className="text-center mb-4">Login to Your Account</h2>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Email Address</label>
                  <div className="input-group">
                    <span className="input-group-text">
                      <i className="fas fa-envelope"></i>
                    </span>
                    <input
                      type="email"
                      className="form-control"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <div className="input-group">
                    <span className="input-group-text">
                      <i className="fas fa-lock"></i>
                    </span>
                    <input
                      type="password"
                      className="form-control"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="d-grid gap-2 mb-3">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={handleVerifyEmail}
                    disabled={verifying}
                  >
                    <i className="fas fa-envelope-open-text me-2"></i>
                    {verifying ? "Sending..." : "Verify Email"}
                  </button>
                </div>

                {otpSent && (
                  <div className="mb-3">
                    <label className="form-label">Enter OTP</label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="fas fa-key"></i>
                      </span>
                      <input
                        type="text"
                        className="form-control"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        required
                      />
                    </div>
                  </div>
                )}

                <div className="d-grid gap-2 mb-3">
                  <button type="submit" className="btn btn-primary btn-lg">
                    <i className="fas fa-sign-in-alt me-2"></i>Login
                  </button>
                  <div className="text-center mt-2">
                    <a href="/forgot-password" className="text-decoration-none">
                      Forgot Password?
                    </a>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
