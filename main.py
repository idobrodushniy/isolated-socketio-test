import eventlet
import socketio

eventlet.monkey_patch()
sio = socketio.Server(
    logger=True,
    engineio_logger=True,
    ping_timeout=5,  # shorter ping configs set for quicker testing
    ping_interval=10,  # shorter ping configs set for quicker testing
)
app = socketio.WSGIApp(sio, socketio_path="socket.io")


@sio.event
def connect(sid, environ):
    print(f"{sid}: [CONNECT HANDLER] Rejecting connection attempt.")
    return False


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(("", 7777)), app)
