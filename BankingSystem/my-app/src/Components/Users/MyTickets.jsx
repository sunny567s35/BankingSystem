import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const MyTickets = () => {
  const { username } = useParams(); // Extract username from URL params
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTickets = async () => {
    try {
      const response = await fetch(`http://localhost:8000/tickets/${username}/`, {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      });
  
      if (!response.ok) throw new Error("Failed to fetch tickets");
  
      const data = await response.json();
      setTickets(data.tickets); // Access `tickets` key
    } catch (error) {
      console.error("Error fetching tickets:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (username) {
      fetchTickets();
    }
  }, [username]);

  const getStatusBadge = (status) => {
    switch (status) {
      case "open":
        return "badge bg-primary";
      case "in_progress":
        return "badge bg-warning";
      case "resolved":
        return "badge bg-success";
      default:
        return "badge bg-secondary";
    }
  };

  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-12">
          <div className="card shadow">
            <div className="card-header bg-primary text-white">
              <h3 className="card-title">My Tickets</h3>
            </div>
            <div className="card-body">
              {loading ? (
                <p>Loading tickets...</p>
              ) : tickets.length === 0 ? (
                <p className="text-center">No tickets found.</p>
              ) : (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th>Ticket ID</th>
                        <th>Type</th>
                        <th>Subject</th>
                        <th>Status</th>
                        <th>Created</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tickets.map((ticket) => (
                        <tr key={ticket.id}>
                          <td>#{ticket.id}</td>
                          <td>{ticket.ticket_type_display}</td>
                          <td>{ticket.subject}</td>
                          <td>
                            <span className={getStatusBadge(ticket.status)}>
                              {ticket.status_display}
                            </span>
                          </td>
                          <td>{new Date(ticket.created_at).toLocaleString()}</td>
                          <td>
                            <a href={`/user_ticket_detail/${username}/${ticket.id}`} className="btn btn-sm btn-info">
                              View
                            </a>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyTickets;