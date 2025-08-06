#!/bin/bash

# Script to get your local network IP address
echo "Getting your local network IP address..."

# For macOS/Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}')
else
    echo "Unsupported OS. Please manually find your local IP address."
    exit 1
fi

echo "Your local network IP is: $LOCAL_IP"
echo ""
echo "Update your .env file with:"
echo "VITE_WEBSOCKET_URL=ws://$LOCAL_IP:8000/ws"
echo ""
echo "To update automatically, run:"
echo "sed -i '' 's/VITE_WEBSOCKET_URL=.*/VITE_WEBSOCKET_URL=ws:\/\/$LOCAL_IP:8000\/ws/' ./react/.env"
