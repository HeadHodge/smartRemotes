#!/usr/bin/python3
#
# thanhle Bluetooth keyboard/Mouse emulator DBUS Service
#

#from __future__ import absolute_import, print_function
#from optparse import OptionParser, make_option
import os
import sys
import time
#import uuid
import dbus
import dbus.service
import dbus.mainloop.glib
#import socket
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
#import logging
#from logging import debug, info, warning, error

#logging.basicConfig(level=logging.DEBUG)

class dbusServer(dbus.service.Object):
    print("Load dbusServer")

    def __init__(self):
        print("Start dbusServer")

        # set up as a dbus server
        bus_name = dbus.service.BusName("smartKeypads.ip2btBridge", dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/methods")

    @dbus.service.method('ip2bt.Input', in_signature='s')
    def send_string(self, string):
        print("Get send_string request through dbus")
        print("key msg: ", string)

    @dbus.service.method('ip2bt.Input', in_signature='yay')
    def send_keys(self, modifier_byte, keys):
        print("Get send_keys request through dbus")
        print("key msg: ", keys)
        state = [ 0xA1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ]
        state[2] = int(modifier_byte)
        count = 4
        for key_code in keys:
            if(count < 10):
                state[count] = int(key_code)
            count += 1
        #self.device.send_string(state)

    @dbus.service.method('ip2bt.Input', in_signature='yay')
    def send_mouse(self, modifier_byte, keys):
        print("Get send_keys request through dbus")
        state = [0xA1, 2, 0, 0, 0, 0]
        count = 2
        for key_code in keys:
            if(count < 6):
                state[count] = int(key_code)
            count += 1
        self.device.send_string(state)


# main routine
if __name__ == "__main__":
    # we an only run as root
    try:
        if not os.geteuid() == 0:
            sys.exit("Only root can run this script")

        DBusGMainLoop(set_as_default=True)
        myservice = dbusServer()
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        sys.exit()
