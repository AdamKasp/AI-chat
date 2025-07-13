#!/bin/bash
set -e

# Wait for dependencies (e.g., database)
echo "Starting AI Agent application..."

# Migrations or other startup operations (if needed)
# python -m app.database.migrate

# Run the application
exec "$@"