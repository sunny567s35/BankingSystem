import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const MyProfile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [username, setUsername] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:8000/get_user/", { credentials: "include" })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          navigate("/login");
        } else {
          setUsername(data.user);
        }
      })
      .catch(() => navigate("/login"));
  }, [navigate]);

  useEffect(() => {
    if (!username) return;

    fetch(`http://localhost:8000/my_profile/${username}/`, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch profile. Please try again.");
        }
        return response.json();
      })
      .then((data) => {
        setProfile(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [username]);

  if (!username) return <p>Loading user...</p>;
  if (loading) return <p>Loading profile...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div className="container profile-container">
      <div className="row justify-content-center">
        <div className="col-lg-10">
          <div className="profile-header text-center mb-5">
            <div className="profile-avatar">
              <i className="fas fa-user-circle"></i>
            </div>
            <h1 className="profile-name">
              {profile.first_name} {profile.last_name}
            </h1>
            <p className="profile-email">{profile.email}</p>
            <div className="profile-status">
              <span className="badge bg-success">Active</span>
            </div>
          </div>

          <div className="row">
            <div className="col-md-6 mb-4">
              <ProfileCard title="Personal Information" icon="fa-user">
                <ProfileInfo label="Full Name" value={`${profile.first_name} ${profile.last_name}`} icon="fa-id-card" />
                <ProfileInfo label="Date of Birth" value={profile.date_of_birth || "Not specified"} icon="fa-birthday-cake" />
                <ProfileInfo label="Gender" value={profile.gender || "Not specified"} icon="fa-venus-mars" />
                <ProfileInfo label="Occupation" value={profile.occupation || "Not specified"} icon="fa-briefcase" />
                <ProfileInfo 
                  label="Income" 
                  value={`₹${(Number(profile.income) || 0).toFixed(2)}`} 
                  icon="fa-money-bill-wave" 
                />
              </ProfileCard>
            </div>

            <div className="col-md-6 mb-4">
              <ProfileCard title="Account Information" icon="fa-university">
                <ProfileInfo label="Username" value={profile.username} icon="fa-user" />
                <ProfileInfo label="Email" value={profile.email} icon="fa-envelope" />
                <ProfileInfo label="Phone" value={profile.phone || "Not specified"} icon="fa-phone" />
                <ProfileInfo label="Account Number" value={profile.account_number} icon="fa-id-badge" />
                <ProfileInfo label="Account Created" value={profile.date_created} icon="fa-calendar-alt" />
                <ProfileInfo label="Branch" value={profile.branch} icon="fa-building" />
                <ProfileInfo label="Account Type" value={profile.account_type} icon="fa-credit-card" />
              </ProfileCard>
            </div>
          </div>

          {/* Compact Balance Section */}
          <div className="row justify-content-center">
            {/* Change col-md-6 to col-md-12 to make it full width */}
            <div className="col-md-12 mb-4">
              <div className="card profile-card">
                <div className="card-header bg-primary text-white py-2">
                  <h5 className="mb-0"><i className="fas fa-wallet me-2"></i> Account Balance</h5>
                </div>
                <div className="card-body p-3">
                  <BalanceDisplay balance={profile.balance_amount} />
                </div>
              </div>
            </div>
          </div>

          <div className="profile-actions text-center mb-5">
            <button className="btn btn-outline-primary me-3" onClick={() => navigate(`/dashboard/${username}`)}>
              <i className="fas fa-arrow-left me-2"></i> Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const BalanceDisplay = ({ balance }) => {
  const [showPasswordPrompt, setShowPasswordPrompt] = useState(false);
  const [showBalance, setShowBalance] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const verifyPassword = () => {
    if (!password) {
      setError("Please enter your password!");
      return;
    }

    fetch("http://localhost:8000/verify_balance_password/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.cookie.match(/csrftoken=([^;]*)/)?.[1] || "",
      },
      body: JSON.stringify({ password }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setShowBalance(true);
          setError("");
        } else {
          setError("Invalid password. Please try again!");
        }
      })
      .catch(() => setError("An error occurred. Please try again."));
  };

  return (
    <div className="text-center">
      {showBalance ? (
        <div>
          <p className="mb-1 small text-muted">Current Balance</p>
          <h4 className="text-success mb-0">₹{balance?.toFixed(2) || "0.00"}</h4>
        </div>
      ) : !showPasswordPrompt ? (
        <button 
          onClick={() => setShowPasswordPrompt(true)} 
          className="btn btn-sm btn-primary"
        >
          <i className="fas fa-eye me-1"></i> Show Balance
        </button>
      ) : (
        <div>
          <input 
            type="password" 
            className="form-control form-control-sm mb-2" 
            placeholder="Enter password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
          />
          <div className="d-flex justify-content-center gap-2">
            <button 
              onClick={verifyPassword} 
              className="btn btn-sm btn-success flex-grow-1"
            >
              <i className="fas fa-check me-1"></i> Verify
            </button>
            <button 
              onClick={() => {
                setShowPasswordPrompt(false);
                setPassword("");
                setError("");
              }} 
              className="btn btn-sm btn-outline-secondary"
            >
              <i className="fas fa-times"></i>
            </button>
          </div>
          {error && <p className="text-danger mt-1 small mb-0">{error}</p>}
        </div>
      )}
    </div>
  );
};

const ProfileCard = ({ title, icon, children }) => (
  <div className="card profile-card h-100">
    <div className="card-header bg-primary text-white">
      <h4><i className={`fas ${icon} me-2`}></i> {title}</h4>
    </div>
    <div className="card-body">{children}</div>
  </div>
);

const ProfileInfo = ({ label, value, icon }) => (
  <div className="profile-info-item">
    <label><i className={`fas ${icon} me-2`}></i> {label}</label>
    <p>{value}</p>
  </div>
);

export default MyProfile;