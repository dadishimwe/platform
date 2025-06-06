/**
 * API service for interacting with the backend
 */
import { apiRequestWithAuth } from './apiInterceptor';

// Base URL for API requests
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

// Default headers for API requests
const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
};

/**
 * API service
 */
const api = {
  /**
   * Authentication API
   */
  auth: {
    /**
     * Login user
     * @param {Object} credentials - User credentials
     * @returns {Promise} Promise with user data and tokens
     */
    login: (credentials) => {
      return fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(credentials),
      }).then(response => response.json());
    },
    
    /**
     * Refresh access token
     * @returns {Promise} Promise with new access token
     */
    refreshToken: () => {
      const refreshToken = localStorage.getItem('refreshToken');
      return fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify({ refreshToken }),
      }).then(response => response.json());
    },
    
    /**
     * Get current user
     * @returns {Promise} Promise with user data
     */
    me: () => {
      return apiRequestWithAuth('/auth/me', {
        method: 'GET',
      });
    },
    
    /**
     * Logout user
     * @returns {Promise} Promise with success message
     */
    logout: () => {
      return apiRequestWithAuth('/auth/logout', {
        method: 'POST',
      });
    },
    
    /**
     * Change password
     * @param {Object} data - Password data
     * @returns {Promise} Promise with success message
     */
    changePassword: (data) => {
      return apiRequestWithAuth('/auth/change-password', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(data),
      });
    },
  },
  
  /**
   * User API
   */
  users: {
    /**
     * Get all users
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with users data
     */
    getAll: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/users?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get user by ID
     * @param {string} id - User ID
     * @returns {Promise} Promise with user data
     */
    getById: (id) => {
      return apiRequestWithAuth(`/users/${id}`, {
        method: 'GET',
      });
    },
    
    /**
     * Create user
     * @param {Object} user - User data
     * @returns {Promise} Promise with created user data
     */
    create: (user) => {
      return apiRequestWithAuth('/users', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(user),
      });
    },
    
    /**
     * Update user
     * @param {string} id - User ID
     * @param {Object} user - User data
     * @returns {Promise} Promise with updated user data
     */
    update: (id, user) => {
      return apiRequestWithAuth(`/users/${id}`, {
        method: 'PUT',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(user),
      });
    },
    
    /**
     * Delete user
     * @param {string} id - User ID
     * @returns {Promise} Promise with success message
     */
    delete: (id) => {
      return apiRequestWithAuth(`/users/${id}`, {
        method: 'DELETE',
      });
    },
    
    /**
     * Get user roles
     * @param {string} id - User ID
     * @returns {Promise} Promise with user roles
     */
    getRoles: (id) => {
      return apiRequestWithAuth(`/users/${id}/roles`, {
        method: 'GET',
      });
    },
  },
  
  /**
   * Organization API
   */
  organizations: {
    /**
     * Get all organizations
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with organizations data
     */
    getAll: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/organizations?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get organization by ID
     * @param {string} id - Organization ID
     * @returns {Promise} Promise with organization data
     */
    getById: (id) => {
      return apiRequestWithAuth(`/organizations/${id}`, {
        method: 'GET',
      });
    },
    
    /**
     * Create organization
     * @param {Object} organization - Organization data
     * @returns {Promise} Promise with created organization data
     */
    create: (organization) => {
      return apiRequestWithAuth('/organizations', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(organization),
      });
    },
    
    /**
     * Update organization
     * @param {string} id - Organization ID
     * @param {Object} organization - Organization data
     * @returns {Promise} Promise with updated organization data
     */
    update: (id, organization) => {
      return apiRequestWithAuth(`/organizations/${id}`, {
        method: 'PUT',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(organization),
      });
    },
    
    /**
     * Delete organization
     * @param {string} id - Organization ID
     * @returns {Promise} Promise with success message
     */
    delete: (id) => {
      return apiRequestWithAuth(`/organizations/${id}`, {
        method: 'DELETE',
      });
    },
    
    /**
     * Get organization users
     * @param {string} id - Organization ID
     * @returns {Promise} Promise with organization users
     */
    getUsers: (id) => {
      return apiRequestWithAuth(`/organizations/${id}/users`, {
        method: 'GET',
      });
    },
    
    /**
     * Add user to organization
     * @param {string} id - Organization ID
     * @param {Object} userData - User data
     * @returns {Promise} Promise with success message
     */
    addUser: (id, userData) => {
      return apiRequestWithAuth(`/organizations/${id}/users`, {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(userData),
      });
    },
    
    /**
     * Remove user from organization
     * @param {string} id - Organization ID
     * @param {string} userId - User ID
     * @returns {Promise} Promise with success message
     */
    removeUser: (id, userId) => {
      return apiRequestWithAuth(`/organizations/${id}/users/${userId}`, {
        method: 'DELETE',
      });
    },
    
    /**
     * Get organization service plans
     * @param {string} id - Organization ID
     * @returns {Promise} Promise with organization service plans
     */
    getServicePlans: (id) => {
      return apiRequestWithAuth(`/organizations/${id}/service-plans`, {
        method: 'GET',
      });
    },
  },
  
  /**
   * Device API
   */
  devices: {
    /**
     * Get all devices
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with devices data
     */
    getAll: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/devices?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get device by ID
     * @param {string} id - Device ID
     * @returns {Promise} Promise with device data
     */
    getById: (id) => {
      return apiRequestWithAuth(`/devices/${id}`, {
        method: 'GET',
      });
    },
    
    /**
     * Create device
     * @param {Object} device - Device data
     * @returns {Promise} Promise with created device data
     */
    create: (device) => {
      return apiRequestWithAuth('/devices', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(device),
      });
    },
    
    /**
     * Update device
     * @param {string} id - Device ID
     * @param {Object} device - Device data
     * @returns {Promise} Promise with updated device data
     */
    update: (id, device) => {
      return apiRequestWithAuth(`/devices/${id}`, {
        method: 'PUT',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(device),
      });
    },
    
    /**
     * Delete device
     * @param {string} id - Device ID
     * @returns {Promise} Promise with success message
     */
    delete: (id) => {
      return apiRequestWithAuth(`/devices/${id}`, {
        method: 'DELETE',
      });
    },
    
    /**
     * Get device configurations
     * @param {string} id - Device ID
     * @returns {Promise} Promise with device configurations
     */
    getConfigurations: (id) => {
      return apiRequestWithAuth(`/devices/${id}/configurations`, {
        method: 'GET',
      });
    },
    
    /**
     * Add configuration to device
     * @param {string} id - Device ID
     * @param {Object} config - Configuration data
     * @returns {Promise} Promise with success message
     */
    addConfiguration: (id, config) => {
      return apiRequestWithAuth(`/devices/${id}/configurations`, {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(config),
      });
    },
    
    /**
     * Get device status
     * @param {string} id - Device ID
     * @returns {Promise} Promise with device status
     */
    getStatus: (id) => {
      return apiRequestWithAuth(`/devices/${id}/status`, {
        method: 'GET',
      });
    },
  },
  
  /**
   * Telemetry API
   */
  telemetry: {
    /**
     * Get user terminal telemetry
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with telemetry data
     */
    getUserTerminalTelemetry: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/telemetry/user-terminals?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get router telemetry
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with telemetry data
     */
    getRouterTelemetry: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/telemetry/routers?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get alerts
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with alerts data
     */
    getAlerts: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/telemetry/alerts?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Sync telemetry data
     * @param {Object} data - Sync data
     * @returns {Promise} Promise with success message
     */
    sync: (data) => {
      return apiRequestWithAuth('/telemetry/sync', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(data),
      });
    },
    
    /**
     * Get usage statistics
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with usage statistics
     */
    getUsageStats: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/telemetry/stats/usage?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get performance statistics
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with performance statistics
     */
    getPerformanceStats: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/telemetry/stats/performance?${queryString}`, {
        method: 'GET',
      });
    },
  },
  
  /**
   * Support API
   */
  support: {
    /**
     * Get all tickets
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with tickets data
     */
    getTickets: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/support/tickets?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get ticket by ID
     * @param {string} id - Ticket ID
     * @returns {Promise} Promise with ticket data
     */
    getTicketById: (id) => {
      return apiRequestWithAuth(`/support/tickets/${id}`, {
        method: 'GET',
      });
    },
    
    /**
     * Create ticket
     * @param {Object} ticket - Ticket data
     * @returns {Promise} Promise with created ticket data
     */
    createTicket: (ticket) => {
      return apiRequestWithAuth('/support/tickets', {
        method: 'POST',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(ticket),
      });
    },
    
    /**
     * Get knowledge base categories
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with categories data
     */
    getKbCategories: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/support/kb/categories?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get knowledge base articles
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with articles data
     */
    getKbArticles: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/support/kb/articles?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Get knowledge base article by ID
     * @param {string} id - Article ID
     * @returns {Promise} Promise with article data
     */
    getKbArticleById: (id) => {
      return apiRequestWithAuth(`/support/kb/articles/${id}`, {
        method: 'GET',
      });
    },
  },
  
  /**
   * Notification API
   */
  notifications: {
    /**
     * Get user notifications
     * @param {Object} params - Query parameters
     * @returns {Promise} Promise with notifications data
     */
    getUserNotifications: (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      return apiRequestWithAuth(`/notifications/user?${queryString}`, {
        method: 'GET',
      });
    },
    
    /**
     * Mark notification as read
     * @param {string} id - Notification ID
     * @returns {Promise} Promise with success message
     */
    markAsRead: (id) => {
      return apiRequestWithAuth(`/notifications/user/${id}/read`, {
        method: 'POST',
      });
    },
    
    /**
     * Mark all notifications as read
     * @returns {Promise} Promise with success message
     */
    markAllAsRead: () => {
      return apiRequestWithAuth('/notifications/user/read-all', {
        method: 'POST',
      });
    },
    
    /**
     * Get notification preferences
     * @returns {Promise} Promise with preferences data
     */
    getPreferences: () => {
      return apiRequestWithAuth('/notifications/preferences', {
        method: 'GET',
      });
    },
    
    /**
     * Update notification preference
     * @param {string} type - Notification type
     * @param {Object} preference - Preference data
     * @returns {Promise} Promise with updated preference data
     */
    updatePreference: (type, preference) => {
      return apiRequestWithAuth(`/notifications/preferences/${type}`, {
        method: 'PUT',
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(preference),
      });
    },
  },
};

export default api;

