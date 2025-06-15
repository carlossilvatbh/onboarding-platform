import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              Digital KYC Platform
            </h1>
            <p className="hero-subtitle">
              Secure, efficient, and compliant customer onboarding solution for global banking
            </p>
            <div className="hero-cta">
              <Link to="/login" className="btn btn-primary btn-lg">
                Start Onboarding
              </Link>
              <a href="#features" className="btn btn-outline btn-lg">
                Learn More
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Why Choose BTS Global Bank?</h2>
            <p className="section-subtitle">
              Our digital KYC platform provides comprehensive compliance solutions with cutting-edge technology
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                🔒
              </div>
              <h3 className="feature-title">Secure & Compliant</h3>
              <p className="feature-description">
                Bank-grade security with full regulatory compliance across multiple jurisdictions
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                ⚡
              </div>
              <h3 className="feature-title">Fast Processing</h3>
              <p className="feature-description">
                Streamlined onboarding process that reduces verification time from days to minutes
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                🌍
              </div>
              <h3 className="feature-title">Global Reach</h3>
              <p className="feature-description">
                Support for international customers with multi-language and multi-currency capabilities
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                📊
              </div>
              <h3 className="feature-title">Real-time Monitoring</h3>
              <p className="feature-description">
                Advanced analytics and monitoring tools for risk assessment and compliance tracking
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                🤖
              </div>
              <h3 className="feature-title">AI-Powered</h3>
              <p className="feature-description">
                Machine learning algorithms for enhanced fraud detection and risk scoring
              </p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">
                📱
              </div>
              <h3 className="feature-title">Mobile Ready</h3>
              <p className="feature-description">
                Responsive design that works seamlessly across all devices and platforms
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="process-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Simple Onboarding Process</h2>
            <p className="section-subtitle">
              Get started with our streamlined KYC process in just a few steps
            </p>
          </div>
          
          <div className="process-steps">
            <div className="process-step">
              <div className="step-number">1</div>
              <h3 className="step-title">Create Profile</h3>
              <p className="step-description">
                Provide basic information and create your secure account
              </p>
            </div>
            
            <div className="process-step">
              <div className="step-number">2</div>
              <h3 className="step-title">Upload Documents</h3>
              <p className="step-description">
                Submit required identification and verification documents
              </p>
            </div>
            
            <div className="process-step">
              <div className="step-number">3</div>
              <h3 className="step-title">Complete Declarations</h3>
              <p className="step-description">
                Fill out UBO and PEP declarations for compliance
              </p>
            </div>
            
            <div className="process-step">
              <div className="step-number">4</div>
              <h3 className="step-title">Get Approved</h3>
              <p className="step-description">
                Receive approval and start using our banking services
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2 className="cta-title">Ready to Get Started?</h2>
            <p className="cta-description">
              Join thousands of customers who trust BTS Global Bank for their financial needs
            </p>
            <Link to="/login" className="btn btn-primary btn-lg">
              Start Your Application
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;

