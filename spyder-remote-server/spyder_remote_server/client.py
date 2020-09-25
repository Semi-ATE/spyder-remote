#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
# socket.connect("tcp://127.0.0.1:52719")
socket.connect("tcp://192.168.1.103:35813")
data = {'kernel': {"command": 'start', "prefix": '/Users/goanpeca/miniconda3/envs/pip37'}}
data = {'kernel': {"command": 'start', "prefix": '/home/conda/forge/envs/py37'}}
data = {'kernel': {"command": 'close_all'}}

message = json.dumps(data)
print("Sending request %s …" % message)
socket.send_string(message)

#  Get the reply.
message = socket.recv()
print("Received reply %s" % (message))
