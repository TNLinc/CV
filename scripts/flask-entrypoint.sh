#!/bin/bash

# Start server
echo "Starting server"
gunicorn -c core/config.py --bind 0.0.0.0:8000 main:app