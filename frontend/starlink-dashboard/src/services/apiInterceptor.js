/**
 * API interceptor for handling authentication headers and token refresh
 */

// Base URL for API requests
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Flag to prevent multiple refresh token requests
let isRefreshing = false;
let refreshSubscribers = [];

/**
 * Subscribe to token refresh
 * @param {Function} callback - Callback function to execute when token is refreshed
 */
function subscribeTokenRefresh(callback) {
  refreshSubscribers.push(callback);
}

/**
 * Notify subscribers that token has been refreshed
 * @param {string} token - New access token
 */
function onTokenRefreshed(token) {
  refreshSubscribers.forEach(callback => callback(token));
  refreshSubscribers = [];
}

/**
 * Refresh access token
 * @returns {Promise<string>} Promise with new access token
 */
async function refreshAccessToken() {
  try {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }
    
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refreshToken }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Failed to refresh token');
    }
    
    const { access_token } = data.data;
    localStorage.setItem('token', access_token);
    
    return access_token;
  } catch (error) {
    // Clear tokens on refresh failure
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    throw error;
  }
}

/**
 * Create fetch request with authentication
 * @param {string} url - Request URL
 * @param {Object} options - Request options
 * @returns {Promise} Promise with response
 */
export async function fetchWithAuth(url, options = {}) {
  // Add authentication header if token exists
  const token = localStorage.getItem('token');
  
  // Clone options to avoid modifying the original
  const requestOptions = { ...options };
  
  // Initialize headers if not exists
  requestOptions.headers = requestOptions.headers || {};
  
  // Add authentication header if token exists
  if (token) {
    requestOptions.headers.Authorization = `Bearer ${token}`;
  }
  
  try {
    // Make the request
    const response = await fetch(url, requestOptions);
    
    // If response is 401 Unauthorized, try to refresh token
    if (response.status === 401) {
      // Check if error is due to expired token
      const data = await response.json();
      const isTokenExpired = data.code === 'token_expired';
      
      if (isTokenExpired && token) {
        try {
          let newToken;
          
          // If already refreshing, wait for it to complete
          if (isRefreshing) {
            newToken = await new Promise(resolve => {
              subscribeTokenRefresh(token => {
                resolve(token);
              });
            });
          } else {
            // Start refreshing
            isRefreshing = true;
            newToken = await refreshAccessToken();
            isRefreshing = false;
            onTokenRefreshed(newToken);
          }
          
          // Retry the request with new token
          requestOptions.headers.Authorization = `Bearer ${newToken}`;
          return fetch(url, requestOptions);
        } catch (error) {
          // If refresh fails, redirect to login
          window.location.href = '/auth/login';
          throw error;
        }
      }
      
      // If not token expired or no token, just return the response
      return response;
    }
    
    // Return the response for other status codes
    return response;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

/**
 * Create API request with authentication
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Request options
 * @returns {Promise} Promise with response data
 */
export async function apiRequestWithAuth(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetchWithAuth(url, options);
  const data = await response.json();
  
  if (!response.ok) {
    throw new Error(data.message || response.statusText);
  }
  
  return data;
}

export default {
  fetchWithAuth,
  apiRequestWithAuth,
};

