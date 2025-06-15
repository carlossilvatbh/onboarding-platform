import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="container">
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        <h1 style={{ fontSize: '4rem', color: 'var(--color-navy)', marginBottom: '1rem' }}>
          404
        </h1>
        <h2 style={{ color: 'var(--color-navy)', marginBottom: '1rem' }}>
          Page Not Found
        </h2>
        <p style={{ color: 'var(--color-s04)', marginBottom: '2rem' }}>
          The page you're looking for doesn't exist.
        </p>
        <Link to="/" className="btn btn-primary">
          Go Home
        </Link>
      </div>
    </div>
  );
};

export default NotFoundPage;

