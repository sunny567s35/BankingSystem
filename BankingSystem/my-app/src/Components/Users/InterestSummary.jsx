import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faPercentage, 
  faUserCircle, 
  faArrowLeft, 
  faChartPie, 
  faListAlt,
  faClock
} from '@fortawesome/free-solid-svg-icons';

const InterestSummary = () => {
  const { username } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState({
    account: {},
    customer: {},
    interest_transactions: [],
    annual_rate: 0,
    total_interest: 0,
    current_balance: 0,
    next_interest_time: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeLeft, setTimeLeft] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/dashboard/${username}/interest_summary/`, {
          credentials: 'include'
        });
        const result = await response.json();
        
        if (!response.ok) {
          if (result.redirect_username) {
            navigate(`/interest_summary/${result.redirect_username}`);
          } else {
            setError(result.error || 'Failed to fetch data');
          }
          return;
        }
        
        setData(result);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    
    fetchData();
    
    // Update countdown every second
    const timer = setInterval(() => {
      if (data.next_interest_time) {
        const now = new Date();
        const nextTime = new Date(data.next_interest_time);
        const diff = Math.floor((nextTime - now) / 1000);
        
        if (diff > 0) {
          const seconds = diff % 60;
          setTimeLeft(`${seconds}s`);
        } else {
          setTimeLeft('Any moment...');
        }
      }
    }, 1000);
    
    return () => clearInterval(timer);
  }, [username, navigate, data.next_interest_time]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  if (loading) return <div className="container mt-5 text-center">Loading...</div>;
  if (error) return (
    <div className="container mt-5">
      <div className="alert alert-danger">{error}</div>
      <button onClick={() => navigate(`/dashboard/${username}`)} className="btn btn-primary">
        Back to Dashboard
      </button>
    </div>
  );

  return (
    <div className="container mt-5">
      <div className="row mb-4">
        <div className="col-12">
          <h2 className="text-center mb-4">
            <FontAwesomeIcon icon={faPercentage} className="me-2" /> Interest Summary
          </h2>
          <div className="text-center mb-4">
            <button onClick={() => navigate(`/dashboard/${username}`)} className="btn btn-outline-primary">
              <FontAwesomeIcon icon={faArrowLeft} className="me-2" /> Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-6 mb-4">
          <div className="card shadow-sm">
            <div className="card-header bg-primary text-white">
              <h4 className="mb-0">
                <FontAwesomeIcon icon={faUserCircle} className="me-2" /> Account Info
              </h4>
            </div>
            <div className="card-body">
              <table className="table table-borderless">
                <tbody>
                  <tr>
                    <th>Account Holder:</th>
                    <td>{data.customer.first_name} {data.customer.last_name}</td>
                  </tr>
                  <tr>
                    <th>Account Number:</th>
                    <td>{data.account.account_number}</td>
                  </tr>
                  <tr>
                    <th>Account Type:</th>
                    <td>{data.account.account_type?.name}</td>
                  </tr>
                  <tr>
                    <th>Annual Rate:</th>
                    <td>{data.annual_rate}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="col-md-6 mb-4">
          <div className="card shadow-sm">
            <div className="card-header bg-success text-white">
              <h4 className="mb-0">
                <FontAwesomeIcon icon={faChartPie} className="me-2" /> Interest Summary
              </h4>
            </div>
            <div className="card-body">
              <table className="table table-borderless">
                <tbody>
                  <tr>
                    <th>Current Balance:</th>
                    <td>{formatCurrency(data.current_balance)}</td>
                  </tr>
                  <tr>
                    <th>24h Interest:</th>
                    <td className="text-success">+ {formatCurrency(data.total_interest)}</td>
                  </tr>
                  <tr>
                    <th>Next Interest:</th>
                    <td>
                      <FontAwesomeIcon icon={faClock} className="me-2" />
                      {timeLeft}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div className="card shadow-sm mb-5">
        <div className="card-header bg-info text-white">
          <h4 className="mb-0">
            <FontAwesomeIcon icon={faListAlt} className="me-2" /> Recent Interest Credits
          </h4>
        </div>
        <div className="card-body">
          {data.interest_transactions?.length > 0 ? (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Time</th>
                    <th>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {data.interest_transactions.map((txn, i) => (
                    <tr key={i}>
                      <td>{formatDate(txn.timestamp)}</td>
                      <td className="text-success">+ {formatCurrency(txn.amount)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="alert alert-info text-center">
              No interest transactions in the last 24 hours
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InterestSummary;