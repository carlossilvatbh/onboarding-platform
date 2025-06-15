import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

// Styles
import './styles/bts-design-system.css';
import './App.css';

// Components
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import LoadingSpinner from './components/LoadingSpinner/LoadingSpinner';

// Pages
import HomePage from './pages/HomePage/HomePage';
import KYCProfilePage from './pages/KYCProfilePage/KYCProfilePage';
import UBODeclarationPage from './pages/UBODeclarationPage/UBODeclarationPage';
import PEPDeclarationPage from './pages/PEPDeclarationPage/PEPDeclarationPage';
import DocumentsPage from './pages/DocumentsPage/DocumentsPage';
import DashboardPage from './pages/DashboardPage/DashboardPage';
import LoginPage from './pages/LoginPage/LoginPage';
import NotFoundPage from './pages/NotFoundPage/NotFoundPage';

// Store
import { store } from './store/store';

// Utils
import { ProtectedRoute } from './utils/ProtectedRoute';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="App">
            <Header />
            
            <main className="main-content">
              <React.Suspense fallback={<LoadingSpinner />}>
                <Routes>
                  {/* Public Routes */}
                  <Route path="/" element={<HomePage />} />
                  <Route path="/login" element={<LoginPage />} />
                  
                  {/* Protected Routes */}
                  <Route path="/dashboard" element={
                    <ProtectedRoute>
                      <DashboardPage />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/kyc-profile" element={
                    <ProtectedRoute>
                      <KYCProfilePage />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/ubo-declaration" element={
                    <ProtectedRoute>
                      <UBODeclarationPage />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/pep-declaration" element={
                    <ProtectedRoute>
                      <PEPDeclarationPage />
                    </ProtectedRoute>
                  } />
                  
                  <Route path="/documents" element={
                    <ProtectedRoute>
                      <DocumentsPage />
                    </ProtectedRoute>
                  } />
                  
                  {/* 404 Page */}
                  <Route path="*" element={<NotFoundPage />} />
                </Routes>
              </React.Suspense>
            </main>
            
            <Footer />
            
            {/* Toast Notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'var(--color-white)',
                  color: 'var(--color-navy)',
                  border: '1px solid var(--color-s06)',
                  borderRadius: 'var(--border-radius-md)',
                  fontFamily: 'var(--font-family-base)',
                },
                success: {
                  iconTheme: {
                    primary: 'var(--color-action)',
                    secondary: 'var(--color-white)',
                  },
                },
                error: {
                  iconTheme: {
                    primary: '#DC2626',
                    secondary: 'var(--color-white)',
                  },
                },
              }}
            />
          </div>
        </Router>
      </QueryClientProvider>
    </Provider>
  );
}

export default App;

