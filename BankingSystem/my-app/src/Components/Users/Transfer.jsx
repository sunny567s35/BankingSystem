import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const Transfer = () => {
  const [formData, setFormData] = useState({
    recipient_account: '',
    amount: ''
  });
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [accountData, setAccountData] = useState({
    account_number: '',
    current_balance: 0
  });
  const [recipientInfo, setRecipientInfo] = useState('');
  const [accountValidation, setAccountValidation] = useState('');
  const { username } = useParams();
  const navigate = useNavigate();

  // Fetch account data on component mount
  useEffect(() => {
    const fetchAccountData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/dashboard/${username}/transfer/`, {
          method: 'GET',
          headers: {
            "X-CSRFToken": getCsrfToken(),
          },
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Failed to fetch account data');
        }

        const data = await response.json();
        setAccountData({
          account_number: data.account_number,
          current_balance: parseFloat(data.current_balance)
        });
      } catch (err) {
        setError(err.message);
      }
    };

    fetchAccountData();
  }, [username]);

  // Real-time account validation
  const handleRecipientAccountChange = async (e) => {
    const accountNumber = e.target.value;
    setFormData({ ...formData, recipient_account: accountNumber });
    
    if (accountNumber.length >= 4) {
      try {
        const response = await fetch(`http://localhost:8000/validate_account/${accountNumber}`, {
          credentials: 'include'
        });
        const data = await response.json();
        
        if (data.exists) {
          setAccountValidation(
            <span className="text-success">
              <i className="fas fa-check-circle"></i> Valid account
            </span>
          );
          setRecipientInfo(
            <span className="text-success">
              <i className="fas fa-user"></i> {data.recipient_name}
            </span>
          );
        } else {
          setAccountValidation(
            <span className="text-danger">
              <i className="fas fa-times-circle"></i> Account not found
            </span>
          );
          setRecipientInfo('');
        }
      } catch (err) {
        console.error('Validation error:', err);
      }
    } else {
      setAccountValidation('');
      setRecipientInfo('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    setSuccessMessage('');

    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      setError('Amount must be greater than zero');
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/dashboard/${username}/transfer/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include',
        body: JSON.stringify({ 
          amount: parseFloat(formData.amount),
          recipient_account: formData.recipient_account,
          username: username
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error processing transfer');
      }

      if (data.status === 'success') {
        setSuccessMessage(data.message);
        setFormData({ recipient_account: '', amount: '' });
        setRecipientInfo('');
        setAccountData(prev => ({
          ...prev,
          current_balance: parseFloat(data.new_balance)
        }));
      } else {
        setError(data.message || 'Error processing transfer');
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
            <div className="card-header">
              <h3 className="mb-0">Transfer Money</h3>
            </div>
            <div className="card-body p-4">
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

              <form id="transfer-form" className="needs-validation" noValidate onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="account_number" className="form-label">Your Account</label>
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
                  <label htmlFor="current_balance" className="form-label">Your Balance</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="fas fa-rupee-sign"></i></span>
                    <input 
                      type="text" 
                      className="form-control" 
                      id="current_balance" 
                      value={`Rs. ${accountData.current_balance.toFixed(2)}`} 
                      readOnly 
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="recipient_account" className="form-label">Recipient Account</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="fas fa-user"></i></span>
                    <input 
                      type="text" 
                      className="form-control" 
                      id="recipient_account" 
                      name="recipient_account" 
                      value={formData.recipient_account}
                      onChange={handleRecipientAccountChange}
                      required 
                    />
                  </div>
                  <div id="account-validation" className="mt-1">{accountValidation}</div>
                  <div id="recipient-info" className="mt-2 small text-muted">{recipientInfo}</div>
                </div>

                <div className="mb-4">
                  <label htmlFor="amount" className="form-label">Amount (Rs.)</label>
                  <div className="input-group">
                    <span className="input-group-text"><i className="fas fa-rupee-sign"></i></span>
                    <input 
                      type="number" 
                      className="form-control" 
                      id="amount" 
                      name="amount"
                      value={formData.amount}
                      onChange={(e) => setFormData({...formData, amount: e.target.value})}
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
                        <i className="fas fa-exchange-alt me-2"></i>Transfer Money
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

export default Transfer;