import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import api from '@/services/api';

// Create authentication context
const AuthContext = createContext();

// Token refresh interval (15 minutes)
const REFRESH_INTERVAL = 15 * 60 * 1000;

/**
 * Authentication provider component
 * @param {Object} props - Component props
 * @returns {JSX.Element} AuthProvider component
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshTimer, setRefreshTimer] = useState(null);

  /**
   * Refresh access token
   */
  const refreshToken = useCallback(async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await api.auth.refreshToken();
      
      if (response.data && response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        return true;
      }
      
      return false;
    } catch (err) {
      console.error('Token refresh error:', err);
      logout();
      return false;
    }
  }, []);

  /**
   * Setup token refresh timer
   */
  const setupRefreshTimer = useCallback(() => {
    // Clear existing timer
    if (refreshTimer) {
      clearInterval(refreshTimer);
    }
    
    // Set new timer
    const timer = setInterval(refreshToken, REFRESH_INTERVAL);
    setRefreshTimer(timer);
    
    return () => {
      clearInterval(timer);
    };
  }, [refreshTimer, refreshToken]);

  // Initialize authentication state
  useEffect(() => {
    const initAuth = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('token');
        
        if (token) {
          // Get current user data
          const response = await api.auth.me();
          
          if (response.data) {
            setUser(response.data);
            setupRefreshTimer();
          } else {
            throw new Error('Failed to get user data');
          }
        }
      } catch (err) {
        console.error('Authentication error:', err);
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
    
    // Cleanup refresh timer on unmount
    return () => {
      if (refreshTimer) {
        clearInterval(refreshTimer);
      }
    };
  }, [setupRefreshTimer, refreshTimer]);

  /**
   * Login user
   * @param {Object} credentials - User credentials
   * @returns {Promise} Promise with login result
   */
  const login = async (credentials) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await api.auth.login(credentials);
      
      if (response.data) {
        const { user, access_token, refresh_token } = response.data;
        
        localStorage.setItem('token', access_token);
        localStorage.setItem('refreshToken', refresh_token);
        
        setUser(user);
        setupRefreshTimer();
        
        return { success: true, user };
      }
      
      return { success: false, message: 'Login failed' };
    } catch (err) {
      setError(err.message || 'Login failed');
      return { success: false, message: err.message || 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout user
   */
  const logout = useCallback(() => {
    // Clear refresh timer
    if (refreshTimer) {
      clearInterval(refreshTimer);
      setRefreshTimer(null);
    }
    
    // Clear tokens
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    
    // Clear user data
    setUser(null);
    
    // Try to call logout API (but don't wait for it)
    try {
      api.auth.logout().catch(() => {});
    } catch (err) {
      console.error('Logout error:', err);
    }
  }, [refreshTimer]);

  /**
   * Check if user has role
   * @param {string} role - Role to check
   * @returns {boolean} True if user has role
   */
  const hasRole = useCallback((role) => {
    if (!user || !user.roles) return false;
    return user.roles.some(r => r.name === role);
  }, [user]);

  /**
   * Check if user has permission
   * @param {string} resource - Resource to check
   * @param {string} action - Action to check
   * @returns {boolean} True if user has permission
   */
  const hasPermission = useCallback((resource, action) => {
    if (!user || !user.permissions) return false;
    return user.permissions.some(p => p.resource === resource && p.action === action);
  }, [user]);

  // Context value
  const value = {
    user,
    loading,
    error,
    login,
    logout,
    refreshToken,
    hasRole,
    hasPermission,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Use authentication hook
 * @returns {Object} Authentication context
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;

