# Chat Application - Network Setup

This chat application consists of a FastAPI backend and a React frontend, both configured to run on your local network.

## Network Configuration

Your current network IP: `172.16.8.248`

## Running the Application

### 1. Start the FastAPI Backend Server

```bash
# Option 1: Using the custom run script (recommended)
cd /Users/hasanraza/Documents/ChatApp
python run_server.py

# Option 2: Using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The FastAPI server will be accessible at:
- Local: http://localhost:8000
- Network: http://172.16.8.248:8000
- WebSocket: ws://172.16.8.248:8000/ws

### 2. Start the React Frontend

```bash
cd /Users/hasanraza/Documents/ChatApp/react
npm install  # if not already done
npm run dev
```

The React app will be accessible at:
- Local: http://localhost:3000
- Network: http://172.16.8.248:3000

## Accessing from Other Devices

Other devices on your network can access the application using:
- **React Frontend**: http://172.16.8.248:3000
- **FastAPI Backend**: http://172.16.8.248:8000

## Configuration Files

### Environment Variables (.env)
The React app uses environment variables for WebSocket configuration:
```
VITE_WEBSOCKET_URL=ws://172.16.8.248:8000/ws
```

### Network IP Detection
Run this script to get your current network IP:
```bash
./get_network_ip.sh
```

## Troubleshooting

### If your IP address changes:
1. Run `./get_network_ip.sh` to get your new IP
2. Update the `.env` file in the react folder
3. Restart both servers

### Firewall Issues:
- Ensure ports 3000 and 8000 are open on your firewall
- On macOS, you might need to allow the applications through the firewall in System Preferences

### Network Access Issues:
- Make sure all devices are on the same network
- Check if your router allows inter-device communication
- Some corporate networks might block custom ports

## Development vs Production

### Development (Current Setup):
- Uses local network IP (172.16.8.248)
- Suitable for testing on local network devices

### Production:
- Update `VITE_WEBSOCKET_URL` to use your production server domain
- Configure proper SSL certificates for `wss://` connections
- Set up proper reverse proxy and load balancing if needed
