#!/bin/bash

# Docker Compose Hub Management Script
# This script manages the InteractiveAI deployment using Docker images from DockerHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose-hub.yml"
IMAGE_TAG="${IMAGE_TAG:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Display usage information
show_usage() {
    cat << EOF
Usage: $(basename "$0") <command> [options]

Commands:
  up              Start all services in the background
  down            Stop all services
  logs            View logs from all services
  logs <service>  View logs from a specific service
  ps              Show running containers
  status          Show service status
  pull            Pull the latest images from DockerHub
  restart         Restart all services
  restart <svc>   Restart a specific service
  exec <svc>      Execute shell in a service container
  build-up        Pull images and start services
  help            Show this help message

Options:
  IMAGE_TAG=<tag> Specify image tag (default: latest)
               Usage: IMAGE_TAG=v1.0.0 $(basename "$0") up

Environment Variables:
  IMAGE_TAG       Docker image tag to use (default: latest)
  COMPOSE_FILE    Path to docker-compose file (auto-detected)

Examples:
  # Start services with default (latest) images
  $(basename "$0") up

  # Start services with specific version
  IMAGE_TAG=v1.0.0 $(basename "$0") up

  # View logs from a specific service
  $(basename "$0") logs cab-context

  # Stop all services
  $(basename "$0") down

  # Pull latest images and start
  $(basename "$0") build-up

EOF
}

# Check if docker-compose file exists
check_compose_file() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Docker compose file not found: $COMPOSE_FILE"
        exit 1
    fi
}

# Start services
cmd_up() {
    check_compose_file
    print_info "Starting services with IMAGE_TAG=$IMAGE_TAG..."
    export IMAGE_TAG
    docker-compose -f "$COMPOSE_FILE" up -d
    print_success "Services started successfully!"
    print_info "Use '$(basename "$0") logs' to view logs"
}

# Stop services
cmd_down() {
    check_compose_file
    print_info "Stopping services..."
    docker-compose -f "$COMPOSE_FILE" down
    print_success "Services stopped successfully!"
}

# View logs
cmd_logs() {
    check_compose_file
    local service="$1"
    
    if [ -z "$service" ]; then
        print_info "Showing logs from all services (Ctrl+C to exit)..."
        docker-compose -f "$COMPOSE_FILE" logs -f
    else
        print_info "Showing logs from $service (Ctrl+C to exit)..."
        docker-compose -f "$COMPOSE_FILE" logs -f "$service"
    fi
}

# Show container status
cmd_ps() {
    check_compose_file
    docker-compose -f "$COMPOSE_FILE" ps
}

# Show service status
cmd_status() {
    check_compose_file
    print_info "Service status:"
    echo ""
    docker-compose -f "$COMPOSE_FILE" ps --services --status running | while read -r service; do
        print_success "$service is running"
    done
    echo ""
    docker-compose -f "$COMPOSE_FILE" ps --services --status exited | while read -r service; do
        print_warning "$service is stopped"
    done
}

# Pull latest images
cmd_pull() {
    check_compose_file
    print_info "Pulling images with tag: $IMAGE_TAG..."
    export IMAGE_TAG
    docker-compose -f "$COMPOSE_FILE" pull
    print_success "Images pulled successfully!"
}

# Restart services
cmd_restart() {
    check_compose_file
    local service="$1"
    
    if [ -z "$service" ]; then
        print_info "Restarting all services..."
        docker-compose -f "$COMPOSE_FILE" restart
        print_success "All services restarted!"
    else
        print_info "Restarting $service..."
        docker-compose -f "$COMPOSE_FILE" restart "$service"
        print_success "$service restarted!"
    fi
}

# Execute shell in container
cmd_exec() {
    check_compose_file
    local service="$1"
    
    if [ -z "$service" ]; then
        print_error "Service name required"
        echo "Usage: $(basename "$0") exec <service-name>"
        exit 1
    fi
    
    print_info "Opening shell in $service..."
    docker-compose -f "$COMPOSE_FILE" exec "$service" sh
}

# Pull and start
cmd_build_up() {
    check_compose_file
    print_info "Pulling images and starting services..."
    cmd_pull
    echo ""
    cmd_up
}

# Main script logic
main() {
    local command="$1"
    shift || true
    
    case "$command" in
        up)
            cmd_up "$@"
            ;;
        down)
            cmd_down "$@"
            ;;
        logs)
            cmd_logs "$@"
            ;;
        ps)
            cmd_ps "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        pull)
            cmd_pull "$@"
            ;;
        restart)
            cmd_restart "$@"
            ;;
        exec)
            cmd_exec "$@"
            ;;
        build-up)
            cmd_build_up "$@"
            ;;
        help|--help|-h)
            show_usage
            ;;
        "")
            print_error "No command provided"
            echo ""
            show_usage
            exit 1
            ;;
        *)
            print_error "Unknown command: $command"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
