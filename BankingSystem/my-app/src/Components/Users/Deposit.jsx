import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const Deposit = () => {
  const [amount, setAmount] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [accountData, setAccountData] = useState({
    account_number: '',
    current_balance: 0
  });
  const { username } = useParams();
  const navigate = useNavigate();

  // Fetch account data on component mount
  useEffect(() => {
    const fetchAccountData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/dashboard/${username}/deposit/`, {
          method: 'GET', // Ensure this is a GET request
          headers: {
            "X-CSRFToken": getCsrfToken(), // Ensure you have a function to get CSRF token
          },
          credentials: 'include', // Important for session-based auth
        });

        if (!response.ok) {
          throw new Error('Failed to fetch account data');
        }

        const data = await response.json();
        setAccountData({
          account_number: data.account_number,
          current_balance: data.current_balance
        });
      } catch (err) {
        setError(err.message);
      }
    };

    fetchAccountData();
  }, [username]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    setSuccessMessage('');

    if (!amount || parseFloat(amount) <= 0) {
      setError('Amount must be greater than zero');
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/dashboard/${username}/deposit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken(), // Ensure you have a function to get the CSRF token
        },
        credentials: 'include', // Important for session-based auth
        body: JSON.stringify({ amount: parseFloat(amount) })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error processing deposit');
      }

      if (data.status === 'success') {
        setSuccessMessage(data.message);
        setAmount('');
        setAccountData(prev => ({
          ...prev,
          current_balance: parseFloat(data.new_balance)
        }));
      } else {
        setError(data.message || 'Error processing deposit');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getCsrfToken = () => {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
  };

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <h2 className="text-center mb-4">Deposit Money</h2>
              <p className="text-muted text-center mb-4">Deposit money into your account</p>
              
              <div id="message-container">
                {error && (
                  <div className="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>{error}</strong>
                    <button 
                      type="button" 
                      className="btn-close" 
                      onClick={() => setError('')} 
                      aria-label="Close"
                    ></button>
                  </div>
                )}
                {successMessage && (
                  <div className="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>{successMessage}</strong>
                    <button 
                      type="button" 
                      className="btn-close" 
                      onClick={() => setSuccessMessage('')} 
                      aria-label="Close"
                    ></button>
                  </div>
                )}
              </div>

              <form id="deposit-form" className="needs-validation" noValidate onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="account_number" className="form-label">Account Number</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="fas fa-university"></i></span>
                    <input 
                      type="text" 
                      className="form-control" 
                      id="account_number" 
                      value={accountData.account_number} 
                      readOnly 
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="current_balance" className="form-label">Current Balance</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="fas fa-rupee-sign"></i></span>
                    <input 
                      type="text" 
                      className="form-control" 
                      id="current_balance" 
                      value={`Rs. ${accountData?.current_balance?.toFixed(2)}`} 
                      readOnly 
                    />
                  </div>
                </div>

                <div className="mb-4">
                  <label htmlFor="amount" className="form-label">Deposit Amount (Rs.)</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="fas fa-rupee-sign"></i></span>
                    <input 
                      type="number" 
                      className="form-control" 
                      id="amount" 
                      name="amount"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                      step="0.01" 
                      min="0.01" 
                      required 
                    />
                    <div className="invalid-feedback">
                      Please enter a valid amount greater than zero.
                    </div>
                  </div>
                </div>

                <div className="d-grid gap-2">
                  <button 
                    type="submit" 
                    className="btn btn-primary btn-lg"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        Processing...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-money-bill-wave me-2"></i>Deposit Money
                      </>
                    )}
                  </button>
                </div>
              </form>

              <div className="text-center mt-3">
                <button 
                  className="btn btn-link text-decoration-none" 
                  onClick={() => navigate(`/dashboard/${username}`)}
                >
                  <i className="fas fa-arrow-left me-1"></i>Back to Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Deposit;