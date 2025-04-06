import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const Statement = () => {
  const [statementData, setStatementData] = useState({
    customer: {
      first_name: '',
      last_name: '',
      created_at: '',
      phone: '',
      email: ''
    },
    address: null,
    account: {
      account_number: '',
      last_transaction_date: null
    },
    branch: {
      branch_name: '',
      location: ''
    },
    account_type: {
      name: ''
    },
    current_balance: 0,
    transactions: [],
    transaction_balances: [],
    generation_date: new Date(),
    masked_phone: '',
    masked_email: ''
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const { username } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStatementData = async () => {
      try {
        console.log(`Fetching statement for username: ${username}`); // Debug log
        const response = await fetch(`http://localhost:8000/dashboard/${username}/statement/`, {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            // Add authorization if needed
            // 'Authorization': `Bearer ${yourToken}`
          }
        });
        
        if (!response.ok) {
          const errorData = await response.json(); // Try to get error details
          console.error('Server error details:', errorData);
          throw new Error(`Failed to fetch statement data: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Received data:', data); // Debug log
        setStatementData(data);
      } catch (error) {
        console.error('Error fetching statement:', error);
        // Consider adding user feedback here
      } finally {
        setIsLoading(false);
      }
    };
  
    fetchStatementData();
  }, [username]);

  const handleDownloadPdf = async () => {
    setIsGeneratingPdf(true);
    try {
      const response = await fetch(`http://localhost:8000/download_statement_pdf/`, {
        credentials: 'include',
        headers: {
          'Accept': 'application/pdf',
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate PDF');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Mthree_Bank_Statement.pdf';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('PDF download failed:', error);
      // Add user feedback here
    } finally {
      setIsGeneratingPdf(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading account statement...</p>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-md-10">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              {/* Bank Header */}
              <div className="text-center mb-4">
                <h1 className="text-primary mb-0">Mthree Bank</h1>
                <p className="text-muted">Customer Account Statement</p>
              </div>
              
              {/* Customer and Account Information */}
              <div className="row mb-4">
                <div className="col-md-6">
                  <div className="card bg-light p-3">
                    <h4 className="mb-3">Customer Information</h4>
                    <p className="mb-1"><strong>Name:</strong> {statementData.customer.first_name} {statementData.customer.last_name}</p>
                    {statementData.address && (
                      <p className="mb-1"><strong>Address:</strong> 
                        {statementData.address.street}, {statementData.address.city}, 
                        {statementData.address.state} - {statementData.address.zip_code}, 
                        {statementData.address.country}
                      </p>
                    )}
                    <p className="mb-1"><strong>Mobile:</strong> {statementData.masked_phone}</p>
                    <p className="mb-1"><strong>Email:</strong> {statementData.masked_email}</p>
                    <p className="mb-1"><strong>Member Since:</strong> {formatDate(statementData.customer.created_at)}</p>
                  </div>
                </div>
                
                <div className="col-md-6">
                  <div className="card bg-light p-3">
                    <h4 className="mb-3">Account Information</h4>
                    <p className="mb-1"><strong>Account Number:</strong> {statementData.account.account_number}</p>
                    <p className="mb-1"><strong>Branch:</strong> {statementData.branch.branch_name} ({statementData.branch.location})</p>
                    <p className="mb-1"><strong>Account Type:</strong> {statementData.account_type.name}</p>
                    <p className="mb-1"><strong>Current Balance:</strong> Rs. {statementData.current_balance.toFixed(2)}</p>
                    <p className="mb-1"><strong>Last Activity:</strong> 
                      {statementData.account.last_transaction_date ? 
                        formatDate(statementData.account.last_transaction_date) : 
                        'No transactions'}
                    </p>
                  </div>
                </div>
              </div>
              
              {/* Statement Title */}
              <h2 className="text-center mb-4">Account Statement as of {formatDate(statementData.generation_date)}</h2>
              
              {/* Action Buttons */}
              <div className="text-center mb-3">
                <button 
                  className="btn btn-outline-primary me-2"
                  onClick={() => navigate(`/dashboard/${username}`)}
                >
                  <i className="fas fa-arrow-left me-1"></i> Back to Dashboard
                </button>
                <a 
                  className="btn btn-success" 
                  id="downloadPdf" 
                  download
                  onClick={handleDownloadPdf}
                >
                  {isGeneratingPdf ? (
                    <>
                      <i className="fas fa-spinner fa-spin me-1"></i> Generating PDF...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-download me-1"></i> Download PDF
                    </>
                  )}
                </a>
              </div>
              
              {/* Transactions Table */}
              <div className="table-responsive">
                <table className="table table-bordered">
                  <thead className="table-dark">
                    <tr>
                      <th>Date & Time</th>
                      <th>Transaction ID</th>
                      <th>Description</th>
                      <th>Amount (Rs.)</th>
                      <th>Balance (Rs.)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {statementData.transactions.length > 0 ? (
                        statementData.transactions.map((transaction) => {
                        // Convert both IDs to strings for comparison since backend sends string IDs
                        const transactionBalance = statementData.transaction_balances.find(
                            ([tid]) => tid.toString() === transaction.id.toString()
                        )?.[1] || 0;
                        
                        return (
                            <tr key={transaction.id}>
                            <td>{formatDate(transaction.timestamp)}</td>
                            <td>TX{transaction.id.toString().padStart(8, '0')}</td>
                            <td>
                                {transaction.description || 
                                (transaction.transaction_type === 'Transfer In' && transaction.transfer_in && 
                                    `Received from A/C ${transaction.transfer_in.sender_account_number}`) ||
                                (transaction.transaction_type === 'Transfer Out' && transaction.transfer_out && 
                                    `Sent to A/C ${transaction.transfer_out.recipient_account_number}`) ||
                                transaction.transaction_type}
                            </td>
                            <td className={
                                transaction.transaction_type === 'Withdraw' || 
                                transaction.transaction_type === 'Transfer Out' ? 
                                'text-danger' : 'text-success'
                            }>
                                {transaction.transaction_type === 'Withdraw' || 
                                transaction.transaction_type === 'Transfer Out' ? '-' : '+'}
                                {transaction.amount.toFixed(2)}
                            </td>
                            <td>{transactionBalance.toFixed(2)}</td>
                            </tr>
                        );
                        })
                    ) : (
                        <tr>
                        <td colSpan="5" className="text-muted text-center">No transactions found</td>
                        </tr>
                    )}
                    </tbody>
                  <tfoot>
                    <tr className="table-secondary">
                      <td colSpan="4" className="text-end"><strong>Current Balance:</strong></td>
                      <td><strong>Rs. {statementData.current_balance.toFixed(2)}</strong></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
              
              {/* Footer Notes */}
              <div className="mt-4 text-center text-muted small">
                <p>This statement was generated on {formatDate(statementData.generation_date)}</p>
                <p>Please notify the bank immediately of any discrepancies</p>
                <p className="mt-2">Mthree Bank • Customer Service: 1800-123-4567</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx='true'>{`
        .card {
          border-radius: 10px;
        }
        .table {
          font-size: 0.9rem;
        }
        .table th {
          white-space: nowrap;
          vertical-align: middle;
        }
        .text-danger {
          color: #dc3545 !important;
          font-weight: 500;
        }
        .text-success {
          color: #28a745 !important;
          font-weight: 500;
        }
        .table tfoot td {
          font-weight: bold;
        }
      `}</style>
    </div>
  );
};

export default Statement;