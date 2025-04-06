import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { format, parseISO } from 'date-fns';

const TicketDetail = () => {
  const { username, ticket_id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTicket = async () => {
      try {
        const response = await fetch(`http://localhost:8000/user_ticket_detail/${username}/${ticket_id}/`, {
          credentials: 'include'
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch ticket');
        }
        
        const data = await response.json();
        setTicket(data.ticket); // Make sure to access data.ticket if your Django view returns {ticket: {...}}
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTicket();
  }, [ticket_id, username]);

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'open': return 'bg-primary';
      case 'in_progress': return 'bg-warning';
      case 'resolved': return 'bg-success';
      default: return 'bg-secondary';
    }
  };

  const formatDate = (dateString) => {
    try {
      // First try parsing as ISO string
      const date = parseISO(dateString);
      return format(date, 'MMM d, yyyy HH:mm');
    } catch (e) {
      // If that fails, try creating from the string directly
      try {
        const date = new Date(dateString);
        return format(date, 'MMM d, yyyy HH:mm');
      } catch (e) {
        console.error('Failed to parse date:', dateString);
        return 'Invalid date';
      }
    }
  };

  if (loading) return <div className="text-center mt-5">Loading ticket details...</div>;
  if (error) return <div className="alert alert-danger mt-5">Error: {error}</div>;
  if (!ticket) return <div className="alert alert-warning mt-5">Ticket not found</div>;
  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow">
            <div className="card-header bg-primary text-white">
              <h3 className="card-title">Ticket #{ticket.id}</h3>
            </div>
            <div className="card-body">
              <div className="mb-4">
                <h5>Ticket Details</h5>
                <div className="row mb-3">
                  <div className="col-md-4"><strong>Type:</strong></div>
                  <div className="col-md-8">{ticket.ticket_type_display || ticket.ticket_type}</div>
                </div>
                <div className="row mb-3">
                  <div className="col-md-4"><strong>Status:</strong></div>
                  <div className="col-md-8">
                    <span className={`badge ${getStatusBadgeClass(ticket.status)}`}>
                      {ticket.status_display || ticket.status}
                    </span>
                  </div>
                </div>
                <div className="row mb-3">
                  <div className="col-md-4"><strong>Created:</strong></div>
                  <div className="col-md-8">{formatDate(ticket.created_at)}</div>
                </div>
                <div className="row mb-3">
                  <div className="col-md-4"><strong>Last Updated:</strong></div>
                  <div className="col-md-8">{formatDate(ticket.updated_at)}</div>
                </div>
                <div className="row mb-3">
                  <div className="col-md-4"><strong>Subject:</strong></div>
                  <div className="col-md-8">{ticket.subject}</div>
                </div>
                <div className="row">
                  <div className="col-md-4"><strong>Description:</strong></div>
                  <div className="col-md-8">
                    {ticket.description.split('\n').map((paragraph, i) => (
                      <p key={i}>{paragraph}</p>
                    ))}
                  </div>
                </div>
              </div>
              
              {ticket.resolution && (
                <div className="mb-4">
                  <h5>Resolution</h5>
                  <div className="card bg-light">
                    <div className="card-body">
                      {ticket.resolution.split('\n').map((paragraph, i) => (
                        <p key={i}>{paragraph}</p>
                      ))}
                    </div>
                  </div>
                </div>
              )}
              
              <button 
                onClick={() => navigate(`/tickets/${username}`)} 
                className="btn btn-secondary"
              >
                Back to Tickets
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketDetail;