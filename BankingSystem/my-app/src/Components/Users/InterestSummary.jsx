import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faPercentage, 
  faUserCircle, 
  faArrowLeft, 
  faChartPie, 
  faListAlt 
} from '@fortawesome/free-solid-svg-icons';

const InterestSummary = () => {
  const { username } = useParams();
  console.log("_________Username_________", username);
  const navigate = useNavigate();
  const [accountData, setAccountData] = useState({
    customer: {
      first_name: '',
      last_name: ''
    },
    account: {
      account_number: '',
      account_type: {
        name: ''
      }
    },
    annual_rate: 0,
    total_interest: 0,
    projected_daily_interest: 0,
    interest_transactions: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInterestData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/dashboard/${username}/interest_summary/`, {
          credentials: 'include'
        });

        const data = await response.json();

        if (!response.ok) {
          // Handle error responses from Django
          if (data.redirect_username) {
            navigate(`/interest_summary/${data.redirect_username}`);
          } else if (data.error) {
            setError(data.error);
          } else {
            setError('Failed to fetch interest data');
          }
          return;
        }

        // Verify the username matches (if present in response)
        if (data.customer && data.customer.username && data.customer.username !== username) {
          navigate(`/interest_summary/${data.customer.username}`);
          return;
        }

        setAccountData(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching interest data:", error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchInterestData();
  }, [username, navigate]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount).replace('₹', '₹');
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  if (loading) {
    return <div className="container mt-5 text-center">Loading...</div>;
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">
          Error: {error}
        </div>
        <button 
          onClick={() => navigate(`/dashboard/${username}`)} 
          className="btn btn-primary"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <div className="row mb-4">
        <div className="col-12">
          <h2 className="text-center mb-4">
            <FontAwesomeIcon icon={faPercentage} className="me-2" /> Interest Summary
          </h2>
          <div className="text-center mb-4">
            <button 
              onClick={() => navigate(`/dashboard/${username}`)} 
              className="btn btn-outline-primary"
            >
              <FontAwesomeIcon icon={faArrowLeft} className="me-2" /> Back to Dashboard
            </button>
          </div>
        </div>
      </div>

      {!accountData.account ? (
        <div className="alert alert-warning">
          No account found. Please contact support.
        </div>
      ) : (
        <>
          <div className="row">
            <div className="col-md-6 mb-4">
              <div className="card shadow-sm">
                <div className="card-header bg-primary text-white">
                  <h4 className="mb-0">
                    <FontAwesomeIcon icon={faUserCircle} className="me-2" /> Account Information
                  </h4>
                </div>
                <div className="card-body">
                  <div className="table-responsive">
                    <table className="table table-borderless">
                      <tbody>
                        <tr>
                          <th>Account Holder:</th>
                          <td>{accountData.customer.first_name} {accountData.customer.last_name}</td>
                        </tr>
                        <tr>
                          <th>Account Number:</th>
                          <td>{accountData.account.account_number}</td>
                        </tr>
                        <tr>
                          <th>Account Type:</th>
                          <td>{accountData.account.account_type.name}</td>
                        </tr>
                        <tr>
                          <th>Annual Interest Rate:</th>
                          <td>{accountData.annual_rate}%</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>

            <div className="col-md-6 mb-4">
              <div className="card shadow-sm">
                <div className="card-header bg-success text-white">
                  <h4 className="mb-0">
                    <FontAwesomeIcon icon={faChartPie} className="me-2" /> Interest Overview
                  </h4>
                </div>
                <div className="card-body">
                  <div className="table-responsive">
                    <table className="table table-borderless">
                      <tbody>
                        <tr>
                          <th>Total Interest (Last 24 hours):</th>
                          <td>{formatCurrency(accountData.total_interest)}</td>
                        </tr>
                        <tr>
                          <th>Projected Daily Interest:</th>
                          <td>{formatCurrency(accountData.projected_daily_interest)}</td>
                        </tr>
                        <tr>
                          <th>Next Interest Credit:</th>
                          <td>{new Date().toLocaleTimeString('en-US', { hour: '2-digit', hour12: false })}:00</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="card shadow-sm mb-5">
            <div className="card-header bg-info text-white">
              <h4 className="mb-0">
                <FontAwesomeIcon icon={faListAlt} className="me-2" /> Recent Hourly Interest Credits
              </h4>
            </div>
            <div className="card-body">
              {accountData.interest_transactions?.length > 0 ? (
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead className="table-light">
                      <tr>
                        <th>Date</th>
                        <th>Description</th>
                        <th>Amount</th>
                      </tr>
                    </thead>
                    <tbody>
                      {accountData.interest_transactions.map((transaction, index) => (
                        <tr key={index}>
                          <td>{formatDate(transaction.timestamp)}</td>
                          <td>Interest Credit</td>
                          <td className="text-success">+ {formatCurrency(transaction.amount)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="alert alert-info text-center">
                  No interest transactions in the last 30 days.
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default InterestSummary;