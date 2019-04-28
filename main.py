import ssl
import websocket
import sys
import string
from threading import Thread
import random
import time
import queue
import threading

def run(*args):
	proxyip = args[0].split(":")[0]
	proxyport = args[0].split(":")[1]
	randId = ''.join(random.choice(string.ascii_uppercase ) for _ in range(100))
	name = random.choice(names)
	avatar = random.choice(avatars)
	print("connecting")
	ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE,"check_hostname": False})
	url = "wss://www.websitey.com:2237/socket.io/?fp="+randId+"&d="+randId+"8&EIO=3&transport=websocket"
	try:
		ws.connect(url, http_proxy_host=proxyip, http_proxy_port=proxyport)
	except :
		print ('caught a timeout')
		return

	print("Receiving")
	ws.recv()
	ws.recv()
	print("Logging In")
	avatar = 'https://eoimages.gsfc.nasa.gov/images/imagerecords/73000/73751/world.topo.bathy.200407.3x21600x21600.B1.png';
	ws.send('42["loginTry",{"username":"'+name+'","avatar":"'+avatar+'","country":"US","private_state":false}]')
	print("Receiving")
	ws.recv()
	print("Sending..............")
	randmsg = ''.join(random.choice(string.ascii_uppercase ) for _ in range(3))
	[ws.send('42["newMessage","'+randmsg+'","#000"]') for x in range(600)]
	print("Closing")
	ws.close()


class MyThread(threading.Thread):
    def __init__(self, theQueue=None):
        threading.Thread.__init__(self)
        self.theQueue=theQueue

    def run(self):
        while True:
            thing=self.theQueue.get()
            self.process(thing)
            self.theQueue.task_done()

    def process(self, thing):
        time.sleep(1)
        print ('processing %s',thing)
        run(thing)


queue=queue.Queue()
AVAILABLE_CPUS=9 #threads

with open(sys.argv[1]) as f:
    proxies = f.read().splitlines()
with open(sys.argv[2],encoding="utf8") as f:
    names = f.read().splitlines()
with open(sys.argv[3]) as f:
    avatars = f.read().splitlines()

for OneOf in range(AVAILABLE_CPUS):
    thread=MyThread(theQueue=queue)
    thread.start() # thread started. But since there are no tasks in Queue yet it is just waiting.

for prox in proxies:
    queue.put(prox) # as soon as task in added here one of available Threads picks it up