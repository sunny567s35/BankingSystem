import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

const ChangePassword = () => {
  const { username } = useParams();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    old_password: "",
    new_password1: "",
    new_password2: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const response = await fetch(`http://localhost:8000/change_password/${username}/`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": document.cookie.match(/csrftoken=([^;]*)/)?.[1] || "",
        },
        body: new URLSearchParams(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.success);
        setTimeout(() => navigate(`/my_profile/${username}`), 2000); // Redirect after success
      } else {
        setError(data.error);
      }
    } catch {
      setError("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow">
            <div className="card-header bg-primary text-white">
              <h3 className="card-title">Change Password</h3>
            </div>
            <div className="card-body">
              {error && <p className="text-danger">{error}</p>}
              {success && <p className="text-success">{success}</p>}

              <form onSubmit={handleSubmit}>
                <div className="form-group mb-3">
                  <label>Old Password</label>
                  <input
                    type="password"
                    className="form-control"
                    name="old_password"
                    value={formData.old_password}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="form-group mb-3">
                  <label>New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    name="new_password1"
                    value={formData.new_password1}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="form-group mb-3">
                  <label>Confirm New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    name="new_password2"
                    value={formData.new_password2}
                    onChange={handleChange}
                    required
                  />
                </div>

                <button type="submit" className="btn btn-primary me-2">
                  Change Password
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => navigate(`/my_profile/${username}`)}>
                  Cancel
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChangePassword;