import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";

const Base = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const getCSRFToken = () => {
    const match = document.cookie.match(/csrftoken=([^ ;]+)/);
    return match ? match[1] : "";
  };

  const fetchUser = async () => {
    try {
      const response = await fetch("http://localhost:8000/get_user/", {
        method: "GET",
        credentials: "include",
      });

      const data = await response.json();
      console.log("Full /get_user/ response:", data);

      if (response.ok && data.user) {
        setUser({ username: data.user });
      } else {
        console.error("User not found in response:", data);
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching user:", error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8000/user_logout/", {
        method: "POST",
        credentials: "include",
        headers: { "X-CSRFToken": getCSRFToken() },
      });

      if (response.ok) {
        setUser(null);
        navigate("/login");
      } else {
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("Error during logout:", error);
    }
  };

  return (
    <div>
      <nav className="navbar navbar-expand-lg" style={{ backgroundColor: "#6a0dad" }}>
        <div className="container">
          <Link className="navbar-brand text-white" to={user ? `/dashboard/${user.username}` : "/"}>
            <i className="fas fa-university me-2"></i> Mthree Bank
          </Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            {loading ? (
              <span className="text-white">Loading...</span>
            ) : user ? (
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link text-white" to={`/dashboard/${user.username}`}>
                    <i className="fas fa-home me-2"></i> Dashboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/about">
                    <i className="fas fa-info-circle me-2"></i> About Us
                  </Link>
                </li>
                <li className="nav-item dropdown">
                  <button className="nav-link dropdown-toggle text-white" id="profileDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <i className="fas fa-user me-2"></i> Profile
                  </button>
                  <ul className="dropdown-menu" aria-labelledby="profileDropdown">
                    <li>
                      <Link className="dropdown-item" to={`/my_profile/${user.username}`}>
                        <i className="fas fa-user-circle me-2"></i> My Profile
                      </Link>
                    </li>
                    <li>
                      <Link className="dropdown-item" to={`/change_password/${user.username}`}>
                        <i className="fas fa-key me-2"></i> Change Password
                      </Link>
                    </li>
                  </ul>
                </li>
                <li className="nav-item dropdown">
                  <button className="nav-link dropdown-toggle text-white" id="ticketsDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <i className="fas fa-ticket-alt me-2"></i> Tickets
                  </button>
                  <ul className="dropdown-menu" aria-labelledby="ticketsDropdown">
                    <li>
                      <Link className="dropdown-item" to={`/tickets/${user.username}`}>
                        <i className="fas fa-list me-2"></i> My Tickets
                      </Link>
                    </li>
                    <li>
                      <Link className="dropdown-item" to={`/raise-ticket/${user.username}`}>
                        <i className="fas fa-plus-circle me-2"></i> Raise Ticket
                      </Link>
                    </li>
                  </ul>
                </li>
                <li className="nav-item">
                  <button className="nav-link btn btn-link text-danger" onClick={handleLogout}>
                    <i className="fas fa-sign-out-alt me-2"></i> Logout
                  </button>
                </li>
              </ul>
            ) : (
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/login">
                    <i className="fas fa-sign-in-alt me-2"></i> Login
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link text-white" to="/register">
                    <i className="fas fa-user-plus me-2"></i> Register
                  </Link>
                </li>
              </ul>
            )}
          </div>
        </div>
      </nav>
      <main className="container py-4">{children}</main>
      <footer className="footer mt-auto py-3 bg-light">
        <div className="container text-center">
          <span className="text-muted">© 2024 Modern Banking App. All rights reserved.</span>
        </div>
      </footer>
    </div>
  );
};

export default Base;