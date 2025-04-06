import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";

const RaiseTicket = () => {
  const { username } = useParams();
  const navigate = useNavigate();
  const [csrfToken, setCsrfToken] = useState("");
  const [subject, setSubject] = useState("");
  const [ticketType, setTicketType] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Fetch CSRF token from Django
  useEffect(() => {
    fetch("http://localhost:8000/get-csrf-token/", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => setCsrfToken(data.csrfToken))
      .catch((err) => console.error("Error fetching CSRF Token:", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    // Ensure inputs are trimmed and non-empty
    if (!subject.trim() || !ticketType || !description.trim()) {
      setError("All fields are required.");
      setLoading(false);
      return;
    }

    const ticketData = {
      subject: subject.trim(),
      ticket_type: ticketType,
      description: description.trim(),
    };

    try {
      const response = await fetch(`http://localhost:8000/raise-ticket/${username}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(ticketData),
        credentials: "include",
      });

      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.error || "Failed to create ticket.");
      }

      setSuccess("Ticket created successfully!");
      setTimeout(() => navigate(`/tickets/${username}`), 1500); // Redirect after success
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow">
            <div className="card-header bg-primary text-white">
              <h3 className="card-title">Raise a Ticket</h3>
            </div>
            <div className="card-body">
              {error && <p className="alert alert-danger">{error}</p>}
              {success && <p className="alert alert-success">{success}</p>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="subject" className="form-label">Subject</label>
                  <input
                    type="text"
                    id="subject"
                    className="form-control"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="ticketType" className="form-label">Ticket Type</label>
                  <select
                    id="ticketType"
                    className="form-control"
                    value={ticketType}
                    onChange={(e) => setTicketType(e.target.value)}
                    required
                  >
                    <option value="">Select Type</option>
                    <option value="general">General</option>
                    <option value="issue">Issue</option>
                    
                  </select>
                </div>
                <div className="mb-3">
                  <label htmlFor="description" className="form-label">Description</label>
                  <textarea
                    id="description"
                    className="form-control"
                    rows="4"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? "Submitting..." : "Submit Ticket"}
                </button>
                <button
                  type="button"
                  className="btn btn-secondary ms-2"
                  onClick={() => navigate(`/my_profile/${username}`)}
                  disabled={loading}
                >
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

export default RaiseTicket;