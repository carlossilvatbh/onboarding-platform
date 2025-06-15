import React from 'react';

const DashboardPage = () => {
  return (
    <div className="container">
      <div className="dashboard-layout">
        <div className="dashboard-content">
          <h1>Dashboard</h1>
          <p>Welcome to your BTS Global Bank dashboard.</p>
          <div className="card">
            <h2>KYC Status</h2>
            <p>Your KYC verification is in progress.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

