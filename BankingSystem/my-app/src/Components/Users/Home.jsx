import React, { useState, useEffect } from 'react';
import { Link, Navigate } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../static/css/style.css";

const Home = ({ messages }) => {
    const [user, setUser] = useState(null); // Initialize user state

    useEffect(() => {
        const fetchUser = async () => {
            const response = await fetch('http://localhost:8000/home/'); // Adjust the URL as needed
            const data = await response.json();
            setUser(data); // Set user state based on response
        };

        fetchUser();
    }, []); // Ensure useEffect is called unconditionally

    // Handle loading state
    if (user === null) {
        return <div>Loading...</div>; // Show a loading message while fetching user data
    }

    // Redirect if user is authenticated
    if (user.is_authenticated) {
        return <Navigate to={`/dashboard/${user.username}`} replace />;
    }
    const handleRedirect = () => {
        window.location.href = "http://localhost:8000/custom_admin/login/";
      };
    
    return (
        <div>
            <div className="container">
                <div className="row justify-content-center align-items-center min-vh-75">
                    <div className="col-md-8 text-center">
                        <div className="welcome-section fade-in">
                            <h1 className="display-4 mb-4">Welcome to Mthree Bank</h1>
                            <p className="lead mb-5">Experience modern banking with security and convenience</p>

                            <div className="d-flex justify-content-center gap-4">
                                <Link to="/login" className="btn btn-primary btn-lg">
                                    <i className="fas fa-sign-in-alt me-2"></i>Login
                                </Link>
                                <Link to="/register" className="btn btn-outline-primary btn-lg">
                                    <i className="fas fa-user-plus me-2"></i>Register
                                </Link>
                                <button onClick={handleRedirect}>
                                    Admin Login
                                </button>
                                {/* <Link to="/custom_admin_login">Admin Login</Link> */}
                            </div>
                        </div>

                        {/* Features Section */}
                        <div className="row mt-5 pt-5">
                            <div className="col-md-4">
                                <div className="feature-card">
                                    <i className="fas fa-shield-alt fa-3x mb-3 text-primary"></i>
                                    <h3>Secure Banking</h3>
                                    <p>Bank with confidence using our secure platform</p>
                                </div>
                            </div>
                            <div className="col-md-4">
                                <div className="feature-card">
                                    <i className="fas fa-mobile-alt fa-3x mb-3 text-primary"></i>
                                    <h3>Mobile Banking</h3>
                                    <p>Access your account anytime, anywhere</p>
                                </div>
                            </div>
                            <div className="col-md-4">
                                <div className="feature-card">
                                    <i className="fas fa-chart-line fa-3x mb-3 text-primary"></i>
                                    <h3>Smart Savings</h3>
                                    <p>Earn interest and grow your savings</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;