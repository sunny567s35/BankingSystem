import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import "../../static/css/style.css";

const Register = () => {
  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    phone: "",
    dob: "",
    gender: "",
    occupation: "",
    account_type: "",
    branch: "",
    initial_deposit: "",
    income: "",
    address: "",
    city: "",
    state: "",
    zipcode: "",
    country: "",
    password: "",
    confirm_password: "",
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirm_password) {
      alert("Passwords do not match!");
      return;
    }
    console.log(formData);
    try {
      const response = await fetch('http://localhost:8000/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const responseText = await response.text(); // Get the response as text
      console.log(responseText); // Log the response text

      if (!response.ok) {
        const errorData = JSON.parse(responseText); // Attempt to parse JSON
        alert(errorData.message || 'Registration failed');
        return;
      }

      alert("Account registration successful!");
      navigate('/login');
    } catch (error) {
      console.error('Error during registration:', error);
      alert('An error occurred during registration. Please try again.');
    }
  };

  return (
    <div className="container py-4">
      <div className="row justify-content-center">
        <div className="col-lg-10">
          <div className="card shadow-sm">
            <div className="card-header bg-primary text-white">
              <h3 className="mb-0">Create New Account</h3>
            </div>
            <div className="card-body p-4">
              <form onSubmit={handleSubmit}>
                <div className="row">
                  {/* Left Column: Personal Information */}
                  <div className="col-md-6">
                    <h5 className="mb-3 text-primary">Personal Information</h5>
                    {[
                      { label: "First Name", name: "firstname", type: "text" },
                      { label: "Last Name", name: "lastname", type: "text" },
                      { label: "Email Address", name: "email", type: "email" },
                      { label: "Phone Number", name: "phone", type: "tel" },
                      { label: "Date of Birth", name: "dob", type: "date" },
                      { label: "Occupation", name: "occupation", type: "text" },
                    ].map((field, index) => (
                      <div className="mb-3" key={index}>
                        <label className="form-label">{field.label}</label>
                        <input type={field.type} className="form-control" name={field.name} value={formData[field.name]} onChange={handleChange} required />
                      </div>
                    ))}

                    <div className="mb-3">
                      <label className="form-label">Gender</label>
                      <select className="form-select" name="gender" value={formData.gender} onChange={handleChange} required>
                        <option value="">Select Gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>

                  {/* Right Column: Account & Address Information */}
                  <div className="col-md-6">
                    <h5 className="mb-3 text-primary">Account & Address</h5>
                    {[
                      { label: "Account Type", name: "account_type", type: "select", options: ["Savings Account", "Current Account"] },
                      { label: "Branch", name: "branch", type: "select", options: ["Main Branch", "North Branch", "South Branch", "East Branch"] },
                      { label: "Initial Deposit ($)", name: "initial_deposit", type: "number" },
                      { label: "Annual Income ($)", name: "income", type: "number" },
                      { label: "Street Address", name: "address", type: "text" },
                      { label: "City", name: "city", type: "text" },
                      { label: "State", name: "state", type: "text" },
                      { label: "Zip Code", name: "zipcode", type: "text" },
                      { label: "Country", name: "country", type: "text" },
                      { label: "Password", name: "password", type: "password" },
                      { label: "Confirm Password", name: "confirm_password", type: "password" },
                    ].map((field, index) => (
                      <div className="mb-3" key={index}>
                        <label className="form-label">{field.label}</label>
                        {field.type === "select" ? (
                          <select className="form-select" name={field.name} value={formData[field.name]} onChange={handleChange} required>
                            <option value="">Select {field.label}</option>
                            {field.options.map((option, i) => (
                              <option key={i} value={option.toLowerCase()}>{option}</option>
                            ))}
                          </select>
                        ) : (
                          <input type={field.type} className="form-control" name={field.name} value={formData[field.name]} onChange={handleChange} required />
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="d-grid gap-2 mt-4">
                  <button type="submit" className="btn btn-primary btn-lg">Create Account</button>
                </div>
                <div className="text-center mt-3">
                  <p>Already have an account? <Link to="/login" className="text-primary">Login here</Link></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
