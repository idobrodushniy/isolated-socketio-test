## Prerequisites
- If you prefer to use Python directly, then please install Python 3.10.4 to make sure you have the same environment.
- If you prefer using docker, please build the environment for two different versions of socketio.

### How to run with Docker? (suggested to have same environment)
- Build the container with socketio version 5.8.0(default version in requirements). Run `docker build . -t sio-test--580`
- Update the version in `requirements.txt` to 4.6.1. Run `docker build . -t sio-test--461`
- Run both containers on different ports. E.g.:
  - `docker run --rm -p 7778:7777 sio-test--461` - 4.6.1 version is running on 7778
  - `docker run --rm -p 7777:7777 sio-test--580` - 5.8.0 version is running on 7777

### How to run without Docker?
- Update the desired version of socketio in requirements.txt. (4.6.1 or 5.8.0)
- Install requirements `pip3 install -r requirements.txt`
- Run the app `python3 main.py`


## How to reproduce?

### v 5.8.0
- Use any tool for establishing socketio connection and sending messages. We used Postman or Insomnia.
- Connect to the socketio by sending a request to URL `ws://localhost:7777/socket.io/?EIO=4&transport=websocket`. Server should return a message about successful handshake.
- Send a message with a content `40` to attempt to connect.
- Server should send you back the message `44{"message":"Connection rejected by server"}` 
- Send several `40` messages in a row. Every time server returns `44{"message":"Connection rejected by server"}`.
- Wait until server pings you with a message `2`. Don't reply with `3`. Continue sending a few `40`. Server should stop responding at some point, but connection will stay alive.
- You can send infinite amount of `40` messages with no messages coming back and websocket connection will not disappear if you continue sending messages often.
- Check the logs of socketio container. You will see
```
Server initialized for eventlet.
(7) wsgi starting up on http://0.0.0.0:7777
(7) accepted ('172.17.0.1', 63498)
8UXe4Xb3X--Na8-RAAAA: Sending packet OPEN data {'sid': '8UXe4Xb3X--Na8-RAAAA', 'upgrades': [], 'pingTimeout': 5000, 'pingInterval': 10000}
8UXe4Xb3X--Na8-RAAAA: Received request to upgrade to websocket
8UXe4Xb3X--Na8-RAAAA: Upgrade to websocket successful
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Sending packet PING data None
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
8UXe4Xb3X--Na8-RAAAA: Sending packet MESSAGE data 4{"message":"Connection rejected by server"}
8UXe4Xb3X--Na8-RAAAA: Client is gone, closing socket
8UXe4Xb3X--Na8-RAAAA: Client is gone, closing socket
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
message handler error
Traceback (most recent call last):
  File "/usr/local/lib/python3.10/site-packages/engineio/server.py", line 621, in _trigger_event
    return self.handlers[event](*args)
  File "/usr/local/lib/python3.10/site-packages/socketio/server.py", line 791, in _handle_eio_message
    self._handle_connect(eio_sid, pkt.namespace, pkt.data)
  File "/usr/local/lib/python3.10/site-packages/socketio/server.py", line 682, in _handle_connect
    'connect', namespace, sid, self.environ[eio_sid])
KeyError: '8UXe4Xb3X--Na8-RAAAA'
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
Cannot send to sid 8UXe4Xb3X--Na8-RAAAA
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
Cannot send to sid 8UXe4Xb3X--Na8-RAAAA
8UXe4Xb3X--Na8-RAAAA: Received packet MESSAGE data 0
Cannot send to sid 8UXe4Xb3X--Na8-RAAAA
```

### v 5.8.0 (with a patch)
- Apply the diff to apply the patch -> `git apply tmp.diff`
- Perform all the tests from the section above. The main difference is that after timeout on the server, websocket connection gonna be closed and KeyError will not appear.

### v 4.6.1
- Use any tool for establishing socketio connection and sending messages. We used Postman or Insomnia.
- Try to connect to `ws://localhost:7778/socket.io/?EIO=3&transport=websocket`. 
- It will return 401 status code.
- Check the logs of socketio, it should be
```
Server initialized for eventlet.
(7) wsgi starting up on http://0.0.0.0:7777
(7) accepted ('172.17.0.1', 57204)
27d39a7f93b445908afce0f70b2da1f7: Sending packet OPEN data {'sid': '27d39a7f93b445908afce0f70b2da1f7', 'upgrades': [], 'pingTimeout': 5000, 'pingInterval': 10000}
Application rejected connection
172.17.0.1 - - [28/Jul/2023 23:39:04] "GET /socket.io/?EIO=3&transport=websocket HTTP/1.1" 401 172 0.001009
(7) accepted ('172.17.0.1', 57206)
da19b6a016a445a4be1c8bdc330c4b45: Sending packet OPEN data {'sid': 'da19b6a016a445a4be1c8bdc330c4b45', 'upgrades': [], 'pingTimeout': 5000, 'pingInterval': 10000}
Application rejected connection
172.17.0.1 - - [28/Jul/2023 23:39:15] "GET /socket.io/?EIO=3&transport=websocket HTTP/1.1" 401 172 0.000800
(7) accepted ('172.17.0.1', 57208)
44e83cff6fc841479650c782d25de48c: Sending packet OPEN data {'sid': '44e83cff6fc841479650c782d25de48c', 'upgrades': [], 'pingTimeout': 5000, 'pingInterval': 10000}
Application rejected connection
172.17.0.1 - - [28/Jul/2023 23:39:16] "GET /socket.io/?EIO=3&transport=websocket HTTP/1.1" 401 172 0.000950
```