#############################################
##            MODULE VARIABLES
#############################################
print('Load keyCode2hassio')
    
from gi.repository import GLib
from multiprocessing import Process
import os, sys, time, json, traceback, queue, threading

if len(sys.argv) < 3: 
    print('Terminate usb2hassio, missing required zone name and/or event list arguments')
    print('Example: python3 usb2hassio.py masterBedroom 3,4,5,6')
    sys.exit()

path = os.path.join(os.path.dirname(__file__), '../../imports/usb')
sys.path.append(path)
path = os.path.join(os.path.dirname(__file__), '../../imports/websockets')
sys.path.append(path)
path = os.path.join(os.path.dirname(__file__), '../../imports/maps/key2hassioMap')
sys.path.append(path)
path = os.path.join(os.path.dirname(__file__), '../../imports/maps/usb2keyMap')
sys.path.append(path)
import wsClient, usbServer, usb2keyMap, key2hassioMap

_ioQueue = queue.Queue()
_ioQueue = {"greeting": "hello"}

# keyCode formatted Input
_inputOptions = {
    "zone": sys.argv[1],
    "channels": sys.argv[2].split(','),
    "queue": _ioQueue,
    "onEvent": None
   }

# hassio service events Output
_outputOptions = {
    "endpoint": "ws://192.168.0.160:8123/api/websocket",
    "address": "192.168.0.160",
    "port": "8123",
    "path": "/api/websocket",
    "queue": _ioQueue,
    "onEvent": None
   }
   
_buffer = 'hello'
   
def onInputEvent(eventType='key', eventData='', options=None):
    print(f' \nonInput Event, eventType: {eventType}')
    print(f'***Input: {eventData}', options, _inputOptions)
    global _buffer
    print(f'Got for Input {_ioQueue}')
    
    _outputOptions["reply"] = {"greeting": "hello"}
    
    key = usb2keyMap.translateKey(eventData)
    hassioCommand = key2hassioMap.translateKey(key)

    #if(hassioCommand != None): ioQueue.put(hassioCommand)
    print(' \n***Queue: ', hassioCommand)
    _buffer = 'goodbye'
    
async def onOutputEvent(eventType='post', eventData=''):
    print(f'onOutputEvent type: {eventType}, type: {eventData}')
    global _ioQueue
    content = json.loads(eventData)

    if(content['type'] == "auth_required"): print('auth_required'); return '{"type": "auth", "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI1NmVhNzU3ODkzMDE0MTMzOTJhOTZiYmY3MTZiOWYyOCIsImlhdCI6MTYxNDc1NzQ2OSwiZXhwIjoxOTMwMTE3NDY5fQ.K2WwAh_9OjXZP5ciIcJ4lXYiLcSgLGrC6AgTPeIp8BY"}'       

    print(f'Wait for Output ')
    _ioQueue = {"greeting": "goodbye"}
    while True:
        time.sleep(.5)
        print(f'Wait for Output {_buffer}')
        continue
        hassioCommand = ioQueue.get()
        print(' \n***Unqueue: ', hassioCommand)
    
def reply(content):
    print(f'reply: {content}')
    
#############################################
##                MAIN
#############################################
try:
    # Start wsServer Module
    try:
        _inputOptions['onEvent'] = onInputEvent
        #usbServer = Process(target=usbServer.start, args=(_inputOptions,))
        usbServer = threading.Thread(target=usbServer.start, args=(_inputOptions,))
        usbServer.start()
    except:
        print('Abort run usbServer: ', sys.exc_info()[0])
        traceback.print_exc()

    # Start wsClient Module
    try:
        _outputOptions['onEvent'] = onOutputEvent
        #wsClient = Process(target=wsClient.start, args=(_outputOptions, _inputOptions))
        wsClient = threading.Thread(target=wsClient.start, args=(_outputOptions,))
        wsClient.start()
    except:
        print('Abort run wsClient: ', sys.exc_info()[0])
        traceback.print_exc()
except:
    print('Abort keyCode2hassio.py', sys.exc_info()[0])
    traceback.print_exc()



#eventData='{"type": "command", "command": "Louder", "id": "webClient", "zone": "livingRoom", "device": "webBrowser"}'
#print(f'key2hassio translation: {key2hassioMap.translateKey(json.loads(eventData), reply)}')
