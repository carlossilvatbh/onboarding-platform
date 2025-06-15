import React from 'react';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-title">BTS Global Bank</h3>
            <p className="footer-description">
              Secure, efficient, and compliant digital KYC platform for global banking solutions.
            </p>
            <p className="footer-tagline">be anywhere</p>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-subtitle">Services</h4>
            <ul className="footer-links">
              <li><a href="#kyc">KYC Verification</a></li>
              <li><a href="#ubo">UBO Declaration</a></li>
              <li><a href="#pep">PEP Screening</a></li>
              <li><a href="#compliance">Compliance</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-subtitle">Support</h4>
            <ul className="footer-links">
              <li><a href="#help">Help Center</a></li>
              <li><a href="#contact">Contact Us</a></li>
              <li><a href="#documentation">Documentation</a></li>
              <li><a href="#api">API Reference</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4 className="footer-subtitle">Legal</h4>
            <ul className="footer-links">
              <li><a href="#privacy">Privacy Policy</a></li>
              <li><a href="#terms">Terms of Service</a></li>
              <li><a href="#compliance">Compliance</a></li>
              <li><a href="#security">Security</a></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <div className="footer-copyright">
            <p>&copy; {currentYear} BTS Global Bank. All rights reserved.</p>
          </div>
          
          <div className="footer-meta">
            <span className="footer-version">v1.0.0</span>
            <span className="footer-separator">•</span>
            <span className="footer-status">
              <span className="status-indicator"></span>
              All systems operational
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

