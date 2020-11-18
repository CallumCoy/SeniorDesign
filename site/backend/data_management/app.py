import export
import get
import delete
import save
import streams

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from streams import socketio


def createApp():
    # create and configure the app

    app = Flask(__name__)
    CORS(app, resources={r"/foo": {"origins": "*"}})
    app.config['SECRET_KEY'] = 'secret'

    socketio.init_app(app)

    app.register_blueprint(save.bp)
    app.register_blueprint(delete.bp)
    app.register_blueprint(get.bp)
    app.register_blueprint(export.bp)
    app.register_blueprint(streams.bp)

    if __name__ == "__main__":
        socketio.run(app, host='0.0.0.0', debug=True)

    return app
