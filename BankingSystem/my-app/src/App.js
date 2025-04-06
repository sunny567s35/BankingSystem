import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import Home from './Components/Users/Home'; // Ensure this path is correct
import Dashboard from './Components/Users/Dashboard'; // Ensure this path is correct
import Base from './Components/Users/Base'; // Ensure this path is correct
import Login from './Components/Users/Login'; // Ensure this path is correct
import Register from './Components/Users/Register'; // Ensure this path is correct
import Deposit from './Components/Users/Deposit'; // Ensure this path is correct
import Withdraw from './Components/Users/Withdraw'; // Ensure this path is correct
import Transfer from './Components/Users/Transfer'; // Ensure this path is correct
import Statement from './Components/Users/Statement'; // Ensure this path is correct
import InterestSummary from './Components/Users/InterestSummary'; // Ensure this path is correct
import MyProfile from './Components/Users/MyProfile'; // Ensure this path is correct
import ChangePassword from './Components/Users/ChangePassword'; // Ensure this path is correct
import AboutUs from './Components/Users/AboutUs'; // Ensure this path is correct
import MyTickets from './Components/Users/MyTickets'; // Ensure this path is correct
import RaiseTicket from './Components/Users/RaiseTicket'; // Ensure this path is correct
import TicketDetail from './Components/Users/TicketDetail'; // Ensure this path is correct
import ForgotPassword from './Components/Users/ForgotPassword'
function App() {
  const [user, setUser] = useState(' ');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user && user !== "undefined") {
      try {
        const parsedUser = JSON.parse(user);
        console.log("Parsed user:", parsedUser); // Log the parsed user
        setUser(parsedUser);
      } catch (error) {
        console.error("Error parsing user data:", error);
        localStorage.removeItem('user'); // Clear corrupted data
      }
    }
  }, []);

  const handleLogin = (userData) => {
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData); // Ensure this is called after successful login
    window.location.href = `/dashboard/${userData.username}`; // Redirect to dashboard
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <Router>
      <Base user={user} setUser={setUser} messages={messages} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard/:username" element={<Dashboard />} />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route path='/deposit/:username' element={<Deposit />} />
          <Route path='/withdraw/:username' element={<Withdraw />} />
          <Route path='/transfer/:username' element={<Transfer />} />
          <Route path='/statement/:username' element={<Statement />} />
          <Route path='/interest_summary/:username' element={<InterestSummary />} />
          <Route path='/my_profile/:username' element={<MyProfile />} />
          <Route path='/change_password/:username' element={<ChangePassword />} />
          <Route path='/about' element={<AboutUs />} />
          <Route path='/tickets/:username' element={<MyTickets />} />
          <Route path='/raise-ticket/:username' element={<RaiseTicket />} />
          <Route path='/user_ticket_detail/:username/:ticket_id' element={<TicketDetail />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          {/* Add more routes as needed */}
        </Routes>
      </Base>
    </Router>
  );
}

export default App;