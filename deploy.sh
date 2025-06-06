#!/bin/bash

# Starlink Reseller Platform Deployment Script
# This script helps with the deployment of the Starlink Reseller Platform

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_message "Docker and Docker Compose are installed."
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_message ".env file created. Please edit it with your configuration."
        else
            print_error ".env.example file not found. Please create a .env file manually."
            exit 1
        fi
    else
        print_message ".env file found."
    fi
}

# Build and start the containers
start_containers() {
    print_message "Building and starting containers..."
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_message "Containers started successfully."
    else
        print_error "Failed to start containers."
        exit 1
    fi
}

# Stop the containers
stop_containers() {
    print_message "Stopping containers..."
    docker-compose down
    
    if [ $? -eq 0 ]; then
        print_message "Containers stopped successfully."
    else
        print_error "Failed to stop containers."
        exit 1
    fi
}

# Show container status
show_status() {
    print_message "Container status:"
    docker-compose ps
}

# Show container logs
show_logs() {
    if [ -z "$1" ]; then
        print_error "Please specify a service name (backend, frontend, postgres, redis)."
        exit 1
    fi
    
    print_message "Showing logs for $1..."
    docker-compose logs --tail=100 -f "$1"
}

# Initialize the database
init_database() {
    print_message "Initializing database..."
    
    # Set INIT_DB=true in .env file
    sed -i 's/INIT_DB=false/INIT_DB=true/g' .env
    
    # Restart backend container
    docker-compose restart backend
    
    print_message "Waiting for database initialization..."
    sleep 10
    
    # Set INIT_DB=false in .env file
    sed -i 's/INIT_DB=true/INIT_DB=false/g' .env
    
    print_message "Database initialized. Default admin user created:"
    print_message "Email: admin@example.com"
    print_message "Password: adminpassword"
    print_warning "Please change the default admin password after first login."
}

# Backup the database
backup_database() {
    BACKUP_FILE="starlink_platform_backup_$(date +%Y%m%d_%H%M%S).sql"
    print_message "Backing up database to $BACKUP_FILE..."
    
    docker-compose exec postgres pg_dump -U postgres starlink_platform > "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        print_message "Database backup created successfully."
    else
        print_error "Failed to create database backup."
        exit 1
    fi
}

# Restore the database
restore_database() {
    if [ -z "$1" ]; then
        print_error "Please specify a backup file."
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Backup file not found: $1"
        exit 1
    fi
    
    print_message "Restoring database from $1..."
    
    # Drop and recreate database
    docker-compose exec postgres psql -U postgres -c "DROP DATABASE IF EXISTS starlink_platform;"
    docker-compose exec postgres psql -U postgres -c "CREATE DATABASE starlink_platform;"
    
    # Restore from backup
    cat "$1" | docker-compose exec -T postgres psql -U postgres -d starlink_platform
    
    if [ $? -eq 0 ]; then
        print_message "Database restored successfully."
    else
        print_error "Failed to restore database."
        exit 1
    fi
}

# Show help message
show_help() {
    echo "Starlink Reseller Platform Deployment Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start       Build and start the containers"
    echo "  stop        Stop the containers"
    echo "  restart     Restart the containers"
    echo "  status      Show container status"
    echo "  logs        Show container logs (requires service name)"
    echo "  init-db     Initialize the database"
    echo "  backup      Backup the database"
    echo "  restore     Restore the database (requires backup file)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs backend"
    echo "  $0 backup"
    echo "  $0 restore starlink_platform_backup_20250606_120000.sql"
}

# Main script
case "$1" in
    start)
        check_docker
        check_env_file
        start_containers
        ;;
    stop)
        stop_containers
        ;;
    restart)
        stop_containers
        start_containers
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "$2"
        ;;
    init-db)
        init_database
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit 0

