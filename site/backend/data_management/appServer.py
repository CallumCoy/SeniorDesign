from app import createApp, socketio
from dotenv import load_dotenv

from robotSetup import handler
from signal import signal, SIGINT

signal(SIGINT, handler)


load_dotenv("/home/sewerbot/repo/SeniorDesign/site/backend/.env")

if __name__ == '__main__':
    app = createApp()
    socketio.run(app, host='0.0.0.0', debug=True)
