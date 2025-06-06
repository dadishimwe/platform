# Starlink Reseller Platform Deployment Guide

This guide provides comprehensive instructions for deploying the Starlink Reseller Platform, including both the backend API and frontend dashboard.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Environment Configuration](#environment-configuration)
5. [Deployment Options](#deployment-options)
   - [Docker Deployment](#docker-deployment)
   - [Manual Deployment](#manual-deployment)
6. [Database Initialization](#database-initialization)
7. [Security Considerations](#security-considerations)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Appendix](#appendix)

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 20 GB
- **Operating System**: Ubuntu 20.04 LTS or newer

### Recommended Requirements

- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 50 GB
- **Operating System**: Ubuntu 22.04 LTS

## Prerequisites

Before deploying the Starlink Reseller Platform, ensure you have the following prerequisites installed:

- **Docker**: Version 20.10.0 or newer
- **Docker Compose**: Version 2.0.0 or newer
- **Git**: For cloning the repository

For manual deployment, you'll also need:

- **Python**: Version 3.11 or newer
- **Node.js**: Version 20.0.0 or newer
- **PostgreSQL**: Version 15.0 or newer
- **Redis**: Version 7.0 or newer
- **Nginx**: Version 1.18.0 or newer

## Project Structure

The Starlink Reseller Platform consists of two main components:

1. **Backend API** (`starlink_api`): A Flask-based RESTful API that handles data processing, authentication, and communication with the Starlink Telemetry API.

2. **Frontend Dashboard** (`frontend/starlink-dashboard`): A React-based web application that provides user interfaces for both clients and administrators.

```
starlink_platform/
├── starlink_api/            # Backend API
│   ├── src/                 # Source code
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Docker configuration
├── frontend/                # Frontend applications
│   └── starlink-dashboard/  # React dashboard
│       ├── src/             # Source code
│       ├── public/          # Static files
│       ├── package.json     # Node.js dependencies
│       └── Dockerfile       # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
└── .env.example             # Environment variables template
```

## Environment Configuration

1. Create a `.env` file in the root directory by copying the `.env.example` file:

```bash
cp .env.example .env
```

2. Edit the `.env` file and update the following variables:

- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `STARLINK_API_KEY`: Your Starlink Telemetry API key

## Deployment Options

### Docker Deployment

Docker deployment is the recommended method for deploying the Starlink Reseller Platform.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/your-repository/starlink_platform.git
cd starlink_platform
```

#### Step 2: Configure Environment Variables

```bash
cp .env.example .env
# Edit .env file with your configuration
```

#### Step 3: Build and Start the Containers

```bash
docker-compose up -d
```

This command will:
- Build the Docker images for the backend and frontend
- Start the PostgreSQL and Redis containers
- Start the backend API container
- Start the frontend dashboard container

#### Step 4: Initialize the Database

For the first run, set `INIT_DB=true` in the `.env` file to initialize the database with default roles, permissions, and an admin user.

After the first run, set `INIT_DB=false` to prevent reinitializing the database on subsequent starts.

#### Step 5: Access the Application

- **Frontend Dashboard**: http://localhost
- **Backend API**: http://localhost:5000/api

### Manual Deployment

If you prefer to deploy the application without Docker, follow these steps:

#### Backend Deployment

1. Navigate to the backend directory:

```bash
cd starlink_platform/starlink_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
export FLASK_APP=src/main.py
export FLASK_ENV=production
export DATABASE_URI=postgresql://postgres:postgres@localhost:5432/starlink_platform
export JWT_SECRET_KEY=your-secret-key
# Add other environment variables as needed
```

5. Initialize the database:

```bash
export INIT_DB=true
flask run
```

6. Start the application with Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 src.main:app
```

#### Frontend Deployment

1. Navigate to the frontend directory:

```bash
cd starlink_platform/frontend/starlink-dashboard
```

2. Install dependencies:

```bash
pnpm install
```

3. Build the application:

```bash
pnpm run build
```

4. Configure Nginx:

```bash
sudo cp nginx.conf /etc/nginx/sites-available/starlink-dashboard
sudo ln -s /etc/nginx/sites-available/starlink-dashboard /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## Database Initialization

The database initialization script creates the following:

1. **Roles**:
   - Super Admin: Full access to all features
   - Admin: Administrative access to manage organizations and users
   - Organization Admin: Administrative access within an organization
   - Technician: Access to device management and technical operations
   - Support: Access to support features
   - Viewer: Read-only access
   - Client: Client access to their own data

2. **Default Admin User**:
   - Email: admin@example.com
   - Password: adminpassword

**Important**: Change the default admin password immediately after the first login.

## Security Considerations

1. **Environment Variables**:
   - Never commit the `.env` file to version control
   - Use strong, unique passwords for database and JWT secret key
   - Rotate the JWT secret key periodically

2. **API Security**:
   - The API uses JWT for authentication
   - Access tokens expire after 1 hour by default
   - Refresh tokens expire after 30 days by default

3. **Production Deployment**:
   - Use HTTPS for all communications
   - Set up a reverse proxy (e.g., Nginx) with proper security headers
   - Configure firewall rules to restrict access to necessary ports

## Monitoring and Maintenance

1. **Logging**:
   - Backend logs are available in the Docker container:
     ```bash
     docker logs starlink_backend
     ```
   - Frontend logs are available in the Nginx logs:
     ```bash
     sudo tail -f /var/log/nginx/access.log
     sudo tail -f /var/log/nginx/error.log
     ```

2. **Database Backup**:
   - Regular backups of the PostgreSQL database are recommended:
     ```bash
     docker exec starlink_postgres pg_dump -U postgres starlink_platform > backup.sql
     ```

3. **Updates**:
   - To update the application, pull the latest changes and rebuild the containers:
     ```bash
     git pull
     docker-compose down
     docker-compose up -d --build
     ```

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check if PostgreSQL is running:
     ```bash
     docker ps | grep postgres
     ```
   - Verify database credentials in the `.env` file

2. **API Not Responding**:
   - Check if the backend container is running:
     ```bash
     docker ps | grep backend
     ```
   - Check backend logs for errors:
     ```bash
     docker logs starlink_backend
     ```

3. **Frontend Not Loading**:
   - Check if the frontend container is running:
     ```bash
     docker ps | grep frontend
     ```
   - Check Nginx logs for errors:
     ```bash
     docker logs starlink_frontend
     ```

## Appendix

### API Documentation

The backend API provides the following endpoints:

- **Authentication**:
  - `POST /api/auth/register`: Register a new user
  - `POST /api/auth/login`: Login and get access token
  - `POST /api/auth/refresh`: Refresh access token
  - `GET /api/auth/me`: Get current user data
  - `POST /api/auth/logout`: Logout and invalidate token

- **Users**:
  - `GET /api/users`: Get all users
  - `GET /api/users/{id}`: Get user by ID
  - `POST /api/users`: Create a new user
  - `PUT /api/users/{id}`: Update user
  - `DELETE /api/users/{id}`: Delete user

- **Organizations**:
  - `GET /api/organizations`: Get all organizations
  - `GET /api/organizations/{id}`: Get organization by ID
  - `POST /api/organizations`: Create a new organization
  - `PUT /api/organizations/{id}`: Update organization
  - `DELETE /api/organizations/{id}`: Delete organization

- **Devices**:
  - `GET /api/devices`: Get all devices
  - `GET /api/devices/{id}`: Get device by ID
  - `POST /api/devices`: Create a new device
  - `PUT /api/devices/{id}`: Update device
  - `DELETE /api/devices/{id}`: Delete device

- **Telemetry**:
  - `GET /api/telemetry/user-terminals`: Get user terminal telemetry
  - `GET /api/telemetry/routers`: Get router telemetry
  - `GET /api/telemetry/alerts`: Get alerts
  - `POST /api/telemetry/sync`: Sync telemetry data

- **Support**:
  - `GET /api/support/tickets`: Get all tickets
  - `GET /api/support/tickets/{id}`: Get ticket by ID
  - `POST /api/support/tickets`: Create a new ticket

- **Notifications**:
  - `GET /api/notifications/user`: Get user notifications
  - `POST /api/notifications/user/{id}/read`: Mark notification as read
  - `POST /api/notifications/user/read-all`: Mark all notifications as read

### Environment Variables Reference

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `POSTGRES_USER` | PostgreSQL username | postgres |
| `POSTGRES_PASSWORD` | PostgreSQL password | postgres |
| `POSTGRES_DB` | PostgreSQL database name | starlink_platform |
| `FLASK_ENV` | Flask environment | production |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | super-secret-key-change-in-production |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token expiration time (seconds) | 3600 |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token expiration time (seconds) | 2592000 |
| `INIT_DB` | Initialize database on startup | false |
| `STARLINK_API_URL` | Starlink API URL | https://api.starlink.com |
| `STARLINK_API_KEY` | Starlink API key | your-starlink-api-key |

