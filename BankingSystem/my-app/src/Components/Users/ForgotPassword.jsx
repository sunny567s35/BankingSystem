import React, { useState } from 'react';

const ForgotPassword = () => {
    const [step, setStep] = useState(1);
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [otpSent, setOtpSent] = useState(false);

    const getCsrfToken = () => {
        const match = document.cookie.match(/csrftoken=([\w-]+)/);
        return match ? match[1] : '';
    };

    const handleOtpFlow = async () => {
        if (!email.trim()) {
            alert('Please enter your email address');
            return;
        }

        // First click: send OTP
        if (!otpSent) {
            try {
                const response = await fetch('http://localhost:8000/send_otp/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify({
                        email,
                        purpose: 'password_reset'
                    })
                });

                const data = await response.json();

                if (data.success) {
                    alert('OTP sent to your email!');
                    console.log('DEBUG OTP:', data.debug_otp); // REMOVE IN PRODUCTION
                    setOtpSent(true);
                } else {
                    alert(data.message || 'Failed to send OTP.');
                }
            } catch (err) {
                console.error(err);
                alert('Failed to send OTP. Please check the network or try again.');
            }
        }

        // Second click: verify OTP
        if (otpSent && otp.trim()) {
            try {
                const response = await fetch("http://localhost:8000/verify_otp/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email,
                        otp,
                        purpose: "password_reset",
                    }),
                });

                const data = await response.json();

                if (data.success) {
                    alert('OTP verified! Set your new password.');
                    setStep(2);
                } else {
                    alert('Invalid OTP. Please try again.');
                }
            } catch (err) {
                console.error(err);
                alert('Error verifying OTP.');
            }
        }
    };

    const handleResetPassword = async (e) => {
        e.preventDefault();

        if (newPassword !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/forgot-password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                credentials: 'include',
                body: JSON.stringify({
                    email,
                    otp,
                    new_password: newPassword,
                    confirm_password: confirmPassword
                })
            });

            const data = await response.json();

            if (data.success) {
                alert('Password reset successful! Please login with your new password.');
                window.location.href = "/login";
            } else {
                alert(data.message || 'Failed to reset password.');
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred while resetting password.');
        }
    };

    return (
        <div className="container my-5">
            <div className="row justify-content-center">
                <div className="col-md-6">
                    <div className="card shadow rounded-3">
                        <div className="card-header bg-primary text-white">
                            <h3 className="text-center">Reset Password</h3>
                        </div>
                        <div className="card-body">
                            <form onSubmit={handleResetPassword}>
                                {/* Email Field - Always Visible */}
                                <div className="mb-4">
                                    <label className="form-label">Email Address</label>
                                    <div className="input-group">
                                        <span className="input-group-text"><i className="fas fa-envelope"></i></span>
                                        <input
                                            type="email"
                                            className="form-control"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            required
                                        />
                                    </div>
                                </div>

                                {/* OTP Field - Only if not verified */}
                                {step === 1 && otpSent && (
                                    <div className="mb-4">
                                        <label className="form-label">Enter OTP</label>
                                        <div className="input-group">
                                            <span className="input-group-text"><i className="fas fa-key"></i></span>
                                            <input
                                                type="text"
                                                className="form-control"
                                                value={otp}
                                                onChange={(e) => setOtp(e.target.value)}
                                                required
                                            />
                                        </div>
                                    </div>
                                )}

                                {/* Combined OTP Button */}
                                {step === 1 && (
                                    <button
                                        type="button"
                                        className="btn btn-primary w-100 mb-4"
                                        onClick={handleOtpFlow}
                                    >
                                        <i className="fas fa-paper-plane me-2"></i>
                                        {otpSent ? "Verify OTP" : "Send OTP"}
                                    </button>
                                )}

                                {/* New Password Fields - Only if OTP is verified */}
                                {step === 2 && (
                                    <>
                                        <div className="mb-4">
                                            <label className="form-label">New Password</label>
                                            <div className="input-group">
                                                <span className="input-group-text"><i className="fas fa-lock"></i></span>
                                                <input
                                                    type="password"
                                                    className="form-control"
                                                    value={newPassword}
                                                    onChange={(e) => setNewPassword(e.target.value)}
                                                    required
                                                />
                                            </div>
                                        </div>

                                        <div className="mb-4">
                                            <label className="form-label">Confirm Password</label>
                                            <div className="input-group">
                                                <span className="input-group-text"><i className="fas fa-lock"></i></span>
                                                <input
                                                    type="password"
                                                    className="form-control"
                                                    value={confirmPassword}
                                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                                    required
                                                />
                                            </div>
                                        </div>

                                        <button type="submit" className="btn btn-success w-100">
                                            <i className="fas fa-save me-2"></i> Reset Password
                                        </button>
                                    </>
                                )}
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
