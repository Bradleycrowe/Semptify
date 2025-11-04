#!/bin/bash

# ============================================================
# Semptify Production Web Server Startup Script (Bash)
# Starts Flask with Waitress WSGI server
# ============================================================

set -e

# ============================================================
# CONFIGURATION
# ============================================================

PORT=${SEMPTIFY_PORT:-8080}
HOST=${SEMPTIFY_HOST:-0.0.0.0}
THREADS=${SEMPTIFY_THREADS:-4}
ENVIRONMENT=${FLASK_ENV:-production}
VENV_PATH=".venv"
PYTHON_SCRIPT="start_production.py"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============================================================
# FUNCTIONS
# ============================================================

print_header() {
    echo ""
    echo -e "${CYAN}$(printf '=%.0s' {1..60})${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}$(printf '=%.0s' {1..60})${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ============================================================
# STARTUP CHECKS
# ============================================================

print_header " SEMPTIFY PRODUCTION SERVER STARTUP "

# Check if Python is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
print_success "Python found: $PYTHON_VERSION"

# Check if virtual environment exists
print_info "Checking virtual environment..."
if [ ! -d "$VENV_PATH" ]; then
    print_warning "Virtual environment not found at $VENV_PATH"
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    print_success "Virtual environment created"
else
    print_success "Virtual environment found"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source "$VENV_PATH/bin/activate"
print_success "Virtual environment activated"

# Check if requirements are installed
print_info "Checking dependencies..."
REQUIRED_PACKAGES=("flask" "waitress" "requests")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -m pip show "$package" &> /dev/null; then
        print_success "Package installed: $package"
    else
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    print_warning "Missing packages: ${MISSING_PACKAGES[*]}"
    echo "Installing requirements..."
    pip install -q -r requirements.txt
    print_success "Requirements installed"
else
    print_success "All required packages are installed"
fi

# Check required directories
print_info "Checking required directories..."
DIRS=("uploads" "logs" "security" "copilot_sync" "final_notices" "data")
for dir in "${DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_success "Created directory: $dir"
    else
        print_success "Directory exists: $dir"
    fi
done

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

print_info "Setting environment variables..."

export FLASK_ENV="$ENVIRONMENT"
export FLASK_DEBUG="0"
export SEMPTIFY_PORT="$PORT"
export SEMPTIFY_HOST="$HOST"
export SEMPTIFY_THREADS="$THREADS"

# Set Flask secret if not already set
if [ -z "$FLASK_SECRET" ]; then
    print_warning "FLASK_SECRET not set. Using development default."
    export FLASK_SECRET="dev-secret-change-in-production"
fi

# Set security mode
if [ -z "$SECURITY_MODE" ]; then
    export SECURITY_MODE="enforced"
    print_info "SECURITY_MODE set to: enforced"
fi

print_success "Environment variables configured"

# ============================================================
# STARTUP INFO
# ============================================================

print_header " SERVER CONFIGURATION "

echo "Host:                $HOST"
echo "Port:                $PORT"
echo "Threads:             $THREADS"
echo "Environment:         $ENVIRONMENT"
echo "Python:              $PYTHON_VERSION"
echo "Working Directory:   $(pwd)"
echo ""

# ============================================================
# SIGNAL HANDLERS
# ============================================================

# Trap SIGINT (Ctrl+C) and SIGTERM for graceful shutdown
trap 'echo ""; echo "Shutting down server..."; exit 0' SIGINT SIGTERM

# ============================================================
# START SERVER
# ============================================================

print_header " STARTING SEMPTIFY PRODUCTION SERVER "

echo -e "${GREEN}🚀 Server starting at http://$HOST:$PORT${NC}"
echo -e "${CYAN}   Press Ctrl+C to stop${NC}"
echo ""

# Start the production server
python3 "$PYTHON_SCRIPT"

exit_code=$?
if [ $exit_code -ne 0 ]; then
    print_error "Server exited with code $exit_code"
    exit $exit_code
fi
