#!/bin/bash
# Start Gunicorn with proper port binding for Render
PORT=${PORT:-8080}
echo "Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 900 --access-logfile - --error-logfile - app:app
