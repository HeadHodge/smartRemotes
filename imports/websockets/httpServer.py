######################################################
##            GLOBAL VARIABLES
#############################################
#import paho.mqtt.client as mqtt
import websocket
import sys, time, json, threading, _thread as thread
from evdev import InputDevice, categorize, ecodes
####################################
##            MODULE VARIABLES
#############################################
print('Load wsServer')
import sys, time, json, traceback, asyncio
from aiohttp import web

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)
    
#######################################
#              MAIN
#######################################
app = web.Application()
app.add_routes([web.static('/smartRemotes', '/smartRemotes/_html2keyCode')])

if __name__ == '__main__':
    web.run_app(app, port=80)
