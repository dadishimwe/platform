import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

/**
 * Protected route component
 * @param {Object} props - Component props
 * @returns {JSX.Element} Protected route component
 */
export default function ProtectedRoute({ 
  children, 
  requiredRole = null,
  requiredPermission = null 
}) {
  const { user, loading, isAuthenticated, hasRole, hasPermission } = useAuth();
  const location = useLocation();
  
  // Show loading state
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="h-16 w-16 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
          <p className="mt-4 text-lg">Loading...</p>
        </div>
      </div>
    );
  }
  
  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />;
  }
  
  // Check role if required
  if (requiredRole && !hasRole(requiredRole)) {
    // Redirect based on user role
    if (hasRole('Admin') || hasRole('Super Admin')) {
      return <Navigate to="/admin" replace />;
    } else {
      return <Navigate to="/client" replace />;
    }
  }
  
  // Check permission if required
  if (requiredPermission) {
    const [resource, action] = requiredPermission.split('.');
    if (!hasPermission(resource, action)) {
      return <Navigate to="/unauthorized" replace />;
    }
  }
  
  // Render children if all checks pass
  return children;
}

