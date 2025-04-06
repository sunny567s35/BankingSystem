import React from "react";
import { Link } from "react-router-dom";

const AboutUs = () => {
  return (
    <div className="container mt-5">
      <div className="text-center mb-4">
        <h1 className="fw-bold text-primary">About Mthree Bank</h1>
        <p className="lead text-muted">Secure. Reliable. Future-ready Banking.</p>
      </div>

      <div className="row">
        {/* Mission Section */}
        <div className="col-md-6">
          <h3 className="text-dark">Our Mission</h3>
          <p>
            At Mthree Bank, our mission is to provide seamless, secure, and innovative banking solutions tailored to our customers' needs. 
            We strive to empower individuals and businesses by offering financial services that are efficient, accessible, and trustworthy.
          </p>
        </div>

        {/* Vision Section */}
        <div className="col-md-6">
          <h3 className="text-dark">Our Vision</h3>
          <p>
            To be the most customer-centric bank, driven by technology and trust, where financial goals are met with ease and security.
          </p>
        </div>
      </div>

      <hr />

      <div className="row mt-4">
        {/* Services Section */}
        <div className="col-md-6">
          <h3 className="text-dark">What We Offer</h3>
          <ul className="list-group">
            <li className="list-group-item">✔ Secure Online Banking</li>
            <li className="list-group-item">✔ Instant Money Transfers</li>
            <li className="list-group-item">✔ High-Interest Savings Accounts</li>
            <li className="list-group-item">✔ 24/7 Customer Support</li>
          </ul>
        </div>

        {/* Security Focus */}
        <div className="col-md-6">
          <h3 className="text-dark">Your Security, Our Priority</h3>
          <p>
            We use cutting-edge encryption and multi-factor authentication to keep your transactions safe. 
            Your trust is our biggest asset, and we continuously enhance our security measures to protect you.
          </p>
        </div>
      </div>

      {/* Call to Action */}
      <div className="text-center mt-5">
        <h4 className="fw-bold">Join Us Today</h4>
        <p>Experience secure and seamless banking with Mthree Bank.</p>
        <Link to="/register" className="btn btn-primary btn-lg">
          Open an Account
        </Link>
      </div>
    </div>
  );
};

export default AboutUs;