# Starlink Reseller Platform

A comprehensive web application for Starlink resellers to manage their clients, devices, and telemetry data.

## Overview

The Starlink Reseller Platform is a full-stack web application that provides Starlink resellers with a powerful dashboard to manage their clients, monitor device performance, and analyze telemetry data. The platform includes both a client-facing portal and an admin dashboard.

### Key Features

#### Client-Facing Portal

- **Real-time Usage Dashboard**: Monitor current and historical data consumption and bandwidth utilization
- **Account Management**: Update profile settings, contact information, and billing details
- **Service Plans**: View current plan, usage limits, and upgrade/downgrade options
- **Performance Metrics**: Track network latency, uptime statistics, and speed tests
- **Support System**: Create support tickets, access knowledge base, and get help
- **Alerts & Notifications**: Receive alerts for usage thresholds, service interruptions, and plan renewals

#### Admin/Reseller Platform

- **Multi-tenant Management**: Create and manage organizations and hierarchy
- **User Role Management**: Assign roles with different permission levels
- **Device Management**: Provision, configure, and monitor terminals
- **Customer Relationship Management**: Onboard clients and manage services
- **Analytics & Reporting**: Analyze usage patterns, performance KPIs, and more
- **Inventory Management**: Track terminals and plan deployments

## Technology Stack

### Backend

- **Framework**: Flask (Python)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **API Integration**: Starlink Telemetry API

### Frontend

- **Framework**: React
- **UI Components**: Tailwind CSS, shadcn/ui
- **State Management**: React Context API
- **Routing**: React Router
- **Data Visualization**: Recharts

## Project Structure

```
starlink_platform/
├── starlink_api/            # Backend API
│   ├── src/                 # Source code
│   │   ├── config/          # Configuration
│   │   ├── models/          # Database models
│   │   ├── routes/          # API routes
│   │   ├── schemas/         # Data schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Docker configuration
├── frontend/                # Frontend applications
│   └── starlink-dashboard/  # React dashboard
│       ├── src/             # Source code
│       │   ├── assets/      # Static assets
│       │   ├── components/  # UI components
│       │   ├── contexts/    # React contexts
│       │   ├── hooks/       # Custom hooks
│       │   ├── layouts/     # Page layouts
│       │   ├── pages/       # Page components
│       │   └── services/    # API services
│       ├── public/          # Static files
│       ├── package.json     # Node.js dependencies
│       └── Dockerfile       # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── .env.example             # Environment variables template
└── deployment_guide.md      # Deployment instructions
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository/starlink_platform.git
cd starlink_platform
```

2. Create environment file:

```bash
cp .env.example .env
# Edit .env file with your configuration
```

3. Build and start the containers:

```bash
docker-compose up -d
```

4. Access the application:

- **Frontend Dashboard**: http://localhost
- **Backend API**: http://localhost:5000/api

For detailed deployment instructions, see the [Deployment Guide](deployment_guide.md).

## User Roles

The platform supports the following user roles:

- **Super Admin**: Full platform control, multi-org management
- **Organization Admin**: Full control within their organization
- **Technician**: Device management, technical operations
- **Sales/Support**: Customer management, billing access
- **Viewer**: Read-only access to assigned areas
- **Client**: Access to their own account and usage data

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## Support

For support, please contact your account manager or email support@example.com.

