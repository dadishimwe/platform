import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from 'next-themes';
import { AuthProvider } from '@/contexts/AuthContext';
import ProtectedRoute from '@/components/common/ProtectedRoute';

// Layouts
import MainLayout from '@/layouts/MainLayout';
import AdminLayout from '@/layouts/AdminLayout';
import ClientLayout from '@/layouts/ClientLayout';
import AuthLayout from '@/layouts/AuthLayout';

// Auth Pages
import LoginPage from '@/pages/auth/LoginPage';
import RegisterPage from '@/pages/auth/RegisterPage';

// Admin Pages
import AdminDashboardPage from '@/pages/admin/DashboardPage';

// Client Pages
import ClientDashboardPage from '@/pages/client/DashboardPage';

// Common Pages
import UnauthorizedPage from '@/pages/UnauthorizedPage';

// Import styles
import './App.css';

/**
 * App component
 * @returns {JSX.Element} App component
 */
function App() {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Auth Routes */}
            <Route path="/auth" element={<AuthLayout />}>
              <Route path="login" element={<LoginPage />} />
              <Route path="register" element={<RegisterPage />} />
            </Route>
            
            {/* Admin Routes */}
            <Route
              path="/admin"
              element={
                <ProtectedRoute requiredRole="Admin">
                  <AdminLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<AdminDashboardPage />} />
              {/* Add more admin routes here */}
            </Route>
            
            {/* Client Routes */}
            <Route
              path="/client"
              element={
                <ProtectedRoute>
                  <ClientLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<ClientDashboardPage />} />
              {/* Add more client routes here */}
            </Route>
            
            {/* Common Routes */}
            <Route path="/unauthorized" element={<UnauthorizedPage />} />
            
            {/* Default Route */}
            <Route path="/" element={<Navigate to="/auth/login" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;

