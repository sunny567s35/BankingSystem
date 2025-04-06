import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useNavigate } from 'react-router-dom';
import { 
  faExchangeAlt, 
  faArrowDown,
  faArrowUp,
  faPercentage,
  faCoins,
  faChartLine,
  faBullhorn,
  faChevronRight,
  faInfoCircle,
  faArrowRight
} from '@fortawesome/free-solid-svg-icons';

const Dashboard = () => {
  const { username } = useParams();
  console.log("_________Username_________", username);
  const [account, setAccount] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [announcements, setAnnouncements] = useState([]);
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { message: 'Welcome back! Your account is active.', tags: 'success' },
    { message: 'New security features available. Update your settings.', tags: 'info' }
  ]);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setMessages([]);
    }, 5000); // 5 seconds
  
    return () => clearTimeout(timer);
  }, []);

  const dismissMessage = (index) => {
    setMessages(messages.filter((_, i) => i !== index));
  };

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/dashboard/${username}/`, {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
          credentials: 'include',
        });

        // Check content type before parsing
        const contentType = response.headers.get('content-type');
        console.log("_________Content Type_________", contentType);
        
        if (!contentType || !contentType.includes('application/json')) {
          // If not JSON, we were probably redirected to login
          navigate('/login', { state: { from: `/dashboard/${username}/` } });
          return;
        }

        const data = await response.json();
        console.log(data);
        if (data.status === 'unauthenticated' || data.redirect) {
          // Handle explicit unauthenticated response from backend
          navigate(data.redirect || '/login');
          return;
        }

        if (!response.ok) {
          throw new Error(data.message || "Failed to fetch dashboard data");
        }

        console.log("_________Data_________", data);
        console.log(data.announcements);
        setAnnouncements(data?.announcements || []);
        setAccount(data?.account);
        setTransactions(data?.transactions || []);
        
        // If the backend sends messages, you can set them here
        if (data?.messages && data?.messages?.length > 0) {
          setMessages(data?.messages);
        }
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        if (error.message.includes('Unexpected token')) {
          navigate('/login', { state: { from: `/dashboard/${username}/` } });
        } else {
          // Add error message to the messages display
          setMessages(prev => [...prev, {
            message: "An error occurred while fetching dashboard data.",
            tags: "danger"
          }]);
        }
      }
    };

    fetchDashboardData();
  }, [username, navigate]);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const processAnnouncements = () => {
    let data = [];
  
    try {
      data = typeof announcements === 'string' ? JSON.parse(announcements) : announcements;
    } catch (err) {
      console.error("Failed to parse announcements JSON:", err);
      return [];
    }
  
    if (!Array.isArray(data)) {
      console.warn("Parsed announcements is not an array:", data);
      return [];
    }
  
    const processed = data
      .map(item => {
        if (!item) return null;
  
        if (item?.model === "app.announcements") {
          const { pk, fields = {} } = item;
          return {
            id: pk,
            title: fields.title || "No title",
            message: fields.message || "",
            created_at: fields.created_at || null,
            is_active: fields.is_active !== false,
          };
        }
  
        return {
          id: item?.id || Math.random().toString(36).substr(2, 9),
          title: item?.title || "No title",
          message: item?.message || "",
          created_at: item?.created_at || null,
          is_active: item?.is_active !== false,
        };
      })
      .filter(item => item && item.is_active)
  
    console.log("Processed announcements array:", processed);
    return processed;
  };
  
  const processedAnnouncements = processAnnouncements();
  
  
  return (
    <div className="container">
      {/* Messages Display - Positioned at the very top */}
      {messages?.length > 0 && (
        <div className="mt-3">
          {messages?.map((message, index) => (
            <div key={index} className={`alert alert-${message?.tags} alert-dismissible fade show`} role="alert">
              <strong>{message?.message}</strong>
              <button 
                type="button" 
                className="btn-close" 
                onClick={() => dismissMessage(index)}
                aria-label="Close"
              />
            </div>
          ))}
        </div>
      )}
      
      {/* Welcome Message */}
      <div className="welcome-banner mb-4">
        <h2>Welcome, {username}!</h2>
      </div>
      
      {/* Credit Card and Announcements Row */}
      <div className="row mb-4">
        <div className="col-md-6 mb-3 mb-md-0">
          <div className="credit-card h-100">
            <div className="credit-card-header">
              <img
                src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAABZUlEQVRoge2ZzU7CQBSFv0YXRsWFuDQm+gy+k8/jelx3X0xMXBgXGBcGE0rpuGgZO4XpnZlSCPQkN2mmnbnnfJ1Op1NoaKiNLjAARsBn8v0BvABnQM9SdBd4A+LC9Aq0LYQ7wAj/IKbRB9pVRXvABwcH+QZOgYvk+zKZy/IOVG5jD5gQHmKIPrABLEJ9JnOhTKgQZBt4xL+NhcSQcA/fWQRJD/EQf5AZ8Bw4ZxnkGtshvlgEuSV/iEIvuCpBRhZBxpQPYh4kj0WQR8qvyDXmQYZYBIkI38o2gBPgOPkOYQyMq4jmGQEfVQWbVFDxf0VExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRFxExEVEXETERURcRMRFRPwvRKz+b+Ub2KoqOqP+P4X2gVYV0YaGGvkFbPjxDDIm4SgAAAAASUVORK5CYII="
                alt="chip" className="chip-icon" />
              <div className="bank-name">Mthree Bank</div>
            </div>
            <div className="credit-card-body">
              <div className="balance-title">Available Balance</div>
              <div className="balance-amount">Rs. {account?.balance?.toFixed(2)}</div>
              <div className="card-details">
                <div className="card-number">{account?.account_number}</div>
                <div className="card-name">{account?.firstname} {account?.lastname}</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Compact Announcements Column */}
        <div className="col-md-6 h-100">
          <div className="announcements-column h-100">
            <div className="announcements-card h-100 d-flex flex-column">
              <div className="announcements-header d-flex justify-content-between align-items-center pb-2">
                <h3 className="m-0 fs-5">
                  <FontAwesomeIcon icon={faBullhorn} className="me-2" />
                  Latest Announcements
                </h3>
              </div>
              <div className="announcements-body flex-grow-1" style={{ overflow: 'hidden' }}>
                {processedAnnouncements.length > 0 ? (
                  <div 
                    className="announcements-list" 
                    style={{
                      maxHeight: '200px',  // Reduced from 300px
                      overflowY: 'auto',
                      paddingRight: '4px'
                    }}
                  >
                    {processedAnnouncements.map((announcement, index) => (
                      <div 
                        className="announcement-item p-2 mb-1"  // Reduced padding
                        key={announcement.id}
                        style={{
                          fontSize: '0.85rem'  // Slightly smaller text
                        }}
                      >
                        <div className="announcement-title d-flex align-items-center">
                          <FontAwesomeIcon 
                            icon={faChevronRight} 
                            className="me-2 text-primary" 
                            style={{ fontSize: '0.7rem' }}  // Smaller icon
                          />
                          <span className="text-truncate" title={announcement.title}>
                            {announcement.title}
                          </span>
                        </div>
                        <div className="announcement-content text-muted mt-1">
                          {announcement.message.length > 80  // Reduced from 100
                            ? `${announcement.message.substring(0, 80)}...` 
                            : announcement.message}
                        </div>
                        <div 
                          className="announcement-date text-muted mt-1" 
                          style={{ fontSize: '0.7rem' }}  // Smaller date text
                        >
                          {formatDate(announcement.created_at)}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="no-announcements d-flex flex-column align-items-center justify-content-center h-100 p-2">
                    <FontAwesomeIcon 
                      icon={faInfoCircle} 
                      className="text-muted mb-2"
                      style={{ fontSize: '1.5rem' }}  // Smaller icon
                    />
                    <span 
                      className="text-muted text-center" 
                      style={{ fontSize: '0.9rem' }}  // Smaller text
                    >
                      No current announcements
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
        </div>

      {/* Rest of your existing Dashboard code... */}
      {/* Quick Actions, Recent Transactions, Interest Summary Section */}
      
      

       {/* Quick Actions */}
       <div className="row mb-4">
        <div className="col-12">
          <h3 className="section-title">Quick Actions</h3>
        </div>
        {[
          { title: "Deposit", icon: "fas fa-money-bill-wave", link: `/deposit/${username}` },
          { title: "Withdraw", icon: "fas fa-hand-holding-usd", link: `/withdraw/${username}` },
          { title: "Transfer", icon: "fas fa-exchange-alt", link: `/transfer/${username}` },
          { title: "Statement", icon: "fas fa-file-invoice", link: `/statement/${username}` }
        ].map((action, index) => (
          <div key={index} className="col-md-3 col-6 mb-3">
            <a href={action.link} className="quick-action-link">
              <div className="quick-action-card">
                <i className={`${action.icon} fa-2x mb-2`}></i>
                <h4>{action.title}</h4>
              </div>
            </a>
          </div>
        ))}
      </div>

      {/* Recent Transactions */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-header">
              <h3 className="mb-0">Recent Transactions</h3>
            </div>
            <div className="card-body">
              <div className="table-responsive">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Type</th>
                      <th>Amount</th>
                      <th>Balance</th>
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.length > 0 ? (
                      transactions.map((transaction, index) => (
                        <tr key={index}>
                          <td>{formatDate(transaction?.timestamp)}</td>
                          <td className={`${transaction?.type === 'Withdraw' || transaction?.type === 'Transfer Out' ? 'text-danger' : 'text-success'}`}>
                            {transaction?.type === 'Deposit' && <FontAwesomeIcon icon={faArrowDown} className="me-1" />}
                            {transaction?.type === 'Withdraw' && <FontAwesomeIcon icon={faArrowUp} className="me-1" />}
                            {(transaction?.type === 'Transfer In' || transaction?.type === 'Transfer Out') && <FontAwesomeIcon icon={faExchangeAlt} className="me-1" />}
                            {transaction?.type === 'Interest' && <FontAwesomeIcon icon={faPercentage} className="me-1" />}
                            {transaction?.type}
                          </td>
                          <td className={`${transaction?.type === 'Withdraw' || transaction?.type === 'Transfer Out' ? 'text-danger' : 'text-success'}`}>
                            {(transaction?.type === 'Withdraw' || transaction?.type === 'Transfer Out') ? '-' : ''}
                            Rs. {transaction?.amount?.toFixed(2)}
                          </td>
                          <td>Rs. {transaction?.balance_after?.toFixed(2)}</td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="4" className="text-center">No recent transactions</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interest Summary Section (Conditional) */}
      {console.log("_________Account_________", account?.account_type)}
      {account?.account_type === 'savings account' && (
        <div className="container mt-5">
          <div className="card interest-summary-promo" style={{ border: '2px solid #28a745' }}>
            <div className="card-body text-center py-4">
              <h3 className="mb-3"><FontAwesomeIcon icon={faCoins} className="me-2" /> Your Savings Account Benefits</h3>
              <p className="mb-4">Earn 6% annual interest on your balance. View your interest earnings and projections.</p>
              <Link to={`/interest_summary/${username}`} className="btn btn-warning btn-lg">
                <FontAwesomeIcon icon={faChartLine} className="me-2" /> View Interest Summary
              </Link>
            </div>
          </div>
        </div>
      )}
<style>
{`
  .text-success {
    color: #198754 !important;
    font-weight: 500;
  }

  .text-danger {
    color: #dc3545 !important;
    font-weight: 500;
  }
  
  .credit-card {
    background: linear-gradient(135deg, #2c3e50, #4ca1af);
    border-radius: 15px;
    color: white;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  
  .credit-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .chip-icon {
    width: 40px;
    height: auto;
  }
  
  .bank-name {
    font-size: 1.2rem;
    font-weight: bold;
  }
  
  .balance-title {
    font-size: 0.9rem;
    opacity: 0.8;
    margin-bottom: 5px;
  }
  
  .balance-amount {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .card-details {
    display: flex;
    justify-content: space-between;
  }
  
  .card-number {
    font-family: monospace;
    letter-spacing: 1px;
  }
  
  .quick-action-card {
    text-align: center;
    padding: 15px;
    border-radius: 10px;
    background-color: #f8f9fa;
    transition: transform 0.2s;
    height: 100%;
  }
  
  .quick-action-link:hover {
    text-decoration: none;
  }
  
  .quick-action-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }

  .interest-summary-promo {
    background: linear-gradient(135deg, #fff9e6, #ffecb3);
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  }
  
  .interest-summary-promo .card-body {
    padding: 2rem;
  }
  
  .interest-summary-promo h3 {
    color: #d4a017;
    font-weight: 600;
  }
  
  .announcements-column {
    width: 100%;
    height: 100%;
  }
  
  .announcements-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    border: 1px solid #e0e0e0;
    padding: 20px;
    height: 100%;
  }
  
  .announcements-header {
    padding-bottom: 15px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 15px;
  }
  
  .announcements-header h3 {
    margin: 0;
    font-size: 1.2rem;
    color: #2c3e50;
    font-weight: 600;
  }
  
  .announcements-body {
    flex-grow: 1;
    min-height: 0;
  }
  
  .announcements-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    height: 100%;
    overflow-y: auto;
    padding-right: 5px;
  }
  
  .announcement-item {
    padding: 12px;
    border-radius: 6px;
    transition: all 0.2s;
    border-left: 3px solid transparent;
    background-color: #f8f9fa;
  }
  
  .announcement-item:hover {
    background-color: #e9ecef;
    border-left: 3px solid #4ca1af;
  }
  
  .announcement-title {
    font-weight: 500;
    margin-bottom: 5px;
    color: #2c3e50;
  }
  
  .announcement-content {
    color: #6c757d;
    font-size: 0.9rem;
    line-height: 1.4;
    margin-bottom: 5px;
    white-space: pre-line;
  }
  
  .announcement-date {
    font-size: 0.8rem;
  }
  
  .no-announcements {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #6c757d;
    text-align: center;
    padding: 20px 0;
  }
  
  .view-all-link {
    color: #4ca1af;
    text-decoration: none;
    font-weight: 500;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    transition: all 0.2s;
  }
  
  .view-all-link:hover {
    color: #3a7a8c;
    text-decoration: underline;
  }
`}
</style>
</div>
  );
};

export default Dashboard;
