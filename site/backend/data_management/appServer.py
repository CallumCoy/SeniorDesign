from app import createApp, socketio
from dotenv import load_dotenv

from robotSetup import Robot, handler
from signal import signal, SIGINT

signal(SIGINT, handler)

try:
    roboto = Robot()
except:
    print('failed to create Robot')
    handler()


load_dotenv("../.env")

if __name__ == '__main__':
    app = createApp()
    socketio.run(app, host='0.0.0.0', debug=True)
