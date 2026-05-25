import sys
import os

# Add the backend directory to the path for Vercel
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
