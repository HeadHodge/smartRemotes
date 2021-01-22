############################
#
# Capture Control Input
#
############################
import asyncio, evdev, sys, websockets
from evdev import InputDevice, categorize, ecodes

controlWords = {
          1: "Esc",
          2: "1",
          3: "2",
          4: "3",
          5: "4",
          6: "5",
          7: "6",
          8: "7",
          9: "8",
         10: "9",
         11: "0",
         28: "Ok",
        103: "Up",
        104: "Less",
        105: "Left",
        106: "Right",
        108: "Down",
        109: "More",
        113: "Mute",
        114: "Softer",
        115: "Louder",
        116: "On/Off",
        127: "Compose",
        158: "Last",
        163: "Forward",
        164: "Start/Stop",
        165: "Backward",
        172: "Home"
}

###################
# Get Control Word
###################
def getControlWord(inputChar, inputCode):
    global controlWords
    
    try:
        print('Enter getControlWord', inputCode, controlWords[inputCode])
        return(controlWords[inputCode])
        
    except Exception as e:
        print(e)
        return(inputChar)

###################
# Send Input
###################
async def sendInput(inputChar, inputCode):

    try:
        controlWord = getControlWord(inputChar, inputCode)
        
        async with websockets.connect("ws://localhost:8080") as websocket:
            print('Send Request', controlWord)
            await websocket.send('{'+f'"symbol": "{controlWord}", "name": "Bob"'+'}')
            print('Sent')

            print('Get Reply')
            greeting = await websocket.recv()
            print(greeting)

    except Exception as e:
        print('Oopps')
        print(e)

    else:
        print('Done')
        
###################
# Capture Input
###################
async def captureInput(device):
    async for event in device.async_read_loop():
        if event.type != 1 : continue
        inputEvent = categorize(event)
        if inputEvent.keystate != 0 : continue
        print('Captured: ', device.path, inputEvent.keycode, inputEvent.scancode)
        await sendInput(inputEvent.keycode, inputEvent.scancode)

###################
#      MAIN
###################
if len(sys.argv) == 1:
  location = 'home'
else:
  location = sys.argv[1]
  
## Open Control Input Channels
chan1 = evdev.InputDevice('/dev/input/event3')
chan2 = evdev.InputDevice('/dev/input/event4')
chan3 = evdev.InputDevice('/dev/input/event5')
chan4 = evdev.InputDevice('/dev/input/event6')

## Make Control Input Channels Private
chan1.grab()
chan2.grab()
chan3.grab()
chan4.grab()

## Listen for Contrrol Input
print(location, chan1.name, chan1.info.vendor, chan1.info.product, chan1.info.bustype)

for device in chan1, chan2, chan3, chan4:
    asyncio.ensure_future(captureInput(device))

loop = asyncio.get_event_loop()
loop.run_forever()