import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import './Header.css';

// Assets
import btsLogo from '../../assets/bts-logo.png';

// Store actions (will be created later)
// import { logout } from '../../store/authSlice';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  
  // Get auth state from Redux store
  const isAuthenticated = useSelector(state => state.auth?.isAuthenticated || false);
  const user = useSelector(state => state.auth?.user);
  
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    // dispatch(logout());
    navigate('/');
    setIsMobileMenuOpen(false);
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  const isActivePath = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="header">
      <nav className="navbar">
        <div className="container">
          <div className="navbar-content">
            {/* Brand */}
            <Link to="/" className="navbar-brand" onClick={closeMobileMenu}>
              <img 
                src={btsLogo} 
                alt="BTS Global Bank" 
                className="brand-logo"
                width="40"
                height="40"
              />
              <div className="brand-text">
                <span className="brand-name">BTS Global Bank</span>
                <span className="brand-tagline">be anywhere</span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="navbar-nav desktop-nav">
              {!isAuthenticated ? (
                <>
                  <Link 
                    to="/" 
                    className={`nav-link ${isActivePath('/') ? 'active' : ''}`}
                  >
                    Home
                  </Link>
                  <Link 
                    to="/login" 
                    className={`nav-link ${isActivePath('/login') ? 'active' : ''}`}
                  >
                    Login
                  </Link>
                </>
              ) : (
                <>
                  <Link 
                    to="/dashboard" 
                    className={`nav-link ${isActivePath('/dashboard') ? 'active' : ''}`}
                  >
                    Dashboard
                  </Link>
                  <Link 
                    to="/kyc-profile" 
                    className={`nav-link ${isActivePath('/kyc-profile') ? 'active' : ''}`}
                  >
                    KYC Profile
                  </Link>
                  <Link 
                    to="/ubo-declaration" 
                    className={`nav-link ${isActivePath('/ubo-declaration') ? 'active' : ''}`}
                  >
                    UBO Declaration
                  </Link>
                  <Link 
                    to="/pep-declaration" 
                    className={`nav-link ${isActivePath('/pep-declaration') ? 'active' : ''}`}
                  >
                    PEP Declaration
                  </Link>
                  <Link 
                    to="/documents" 
                    className={`nav-link ${isActivePath('/documents') ? 'active' : ''}`}
                  >
                    Documents
                  </Link>
                  
                  {/* User Menu */}
                  <div className="user-menu">
                    <span className="user-greeting">
                      Hello, {user?.firstName || 'User'}
                    </span>
                    <button 
                      onClick={handleLogout}
                      className="btn btn-outline btn-sm"
                    >
                      Logout
                    </button>
                  </div>
                </>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button 
              className="mobile-menu-toggle"
              onClick={toggleMobileMenu}
              aria-label="Toggle mobile menu"
              aria-expanded={isMobileMenuOpen}
            >
              <span className={`hamburger ${isMobileMenuOpen ? 'active' : ''}`}>
                <span></span>
                <span></span>
                <span></span>
              </span>
            </button>
          </div>

          {/* Mobile Navigation */}
          <div className={`mobile-nav ${isMobileMenuOpen ? 'active' : ''}`}>
            {!isAuthenticated ? (
              <>
                <Link 
                  to="/" 
                  className={`mobile-nav-link ${isActivePath('/') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  Home
                </Link>
                <Link 
                  to="/login" 
                  className={`mobile-nav-link ${isActivePath('/login') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  Login
                </Link>
              </>
            ) : (
              <>
                <div className="mobile-user-info">
                  <span className="mobile-user-greeting">
                    Hello, {user?.firstName || 'User'}
                  </span>
                </div>
                
                <Link 
                  to="/dashboard" 
                  className={`mobile-nav-link ${isActivePath('/dashboard') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  Dashboard
                </Link>
                <Link 
                  to="/kyc-profile" 
                  className={`mobile-nav-link ${isActivePath('/kyc-profile') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  KYC Profile
                </Link>
                <Link 
                  to="/ubo-declaration" 
                  className={`mobile-nav-link ${isActivePath('/ubo-declaration') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  UBO Declaration
                </Link>
                <Link 
                  to="/pep-declaration" 
                  className={`mobile-nav-link ${isActivePath('/pep-declaration') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  PEP Declaration
                </Link>
                <Link 
                  to="/documents" 
                  className={`mobile-nav-link ${isActivePath('/documents') ? 'active' : ''}`}
                  onClick={closeMobileMenu}
                >
                  Documents
                </Link>
                
                <button 
                  onClick={handleLogout}
                  className="mobile-logout-btn"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;

