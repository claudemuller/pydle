#!/usr/bin/env python
# pydle.py

# Copyright 2015 Claude Müller.
#
# Licensed under the MIT License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Python class to check for USB connected Kindle and interface with its storage

    @TODO   OS X compatibility
            Processing and storing of note, bookmarks, highlights
            Integration into Evernote, Google Drive and Dropbox to store notes
"""

import sys
import re
import os
if sys.platform == "win":
    import win32com.client
else:
    import dbus
    from gi.repository import GLib as glib
    from pyudev import Context, Monitor
try:
    from pyudev.glib import MonitorObserver
except:
    from pyudev.glib import GUDevMonitorObserver as MonitorObserver

class Pydle:
    def __init__(self, platform):
        self.platform = platform
        self.booksDir = "/documents"
        self.dictionaries = self.booksDir + "/dictionaries"
        self.noteBook = self.booksDir + "/My Clippings.txt"

        if self._detectDevice():
            self._getBooks()

    def _detectDevice(self):
        """ Detect and retrieve Kindle device info """

        # Use win32com for Windows environment
        if self.platform == "win":
            self.wmi = win32com.client.GetObject("winmgmts:")
            for usb in self.wmi.InstancesOf("Win32_USBControllerDevice"):
                if re.search("kindle", usb.Dependent, re.IGNORECASE):
                    for logical_disk in self.wmi.InstancesOf("Win32_LogicalDisk"):
                        if re.search("kindle", logical_disk.VolumeName, re.IGNORECASE):
                            self.mountPoint = logical_disk.DeviceID
                            self.description = logical_disk.Description
                            self.name = logical_disk.VolumeName

                            return True
        # Else assume a *nix environment
        else:
            bus = dbus.SystemBus()
            ud_manager_obj = bus.get_object("org.freedesktop.UDisks", "/org/freedesktop/UDisks")
            ud_manager = dbus.Interface(ud_manager_obj, 'org.freedesktop.UDisks')

            for dev in ud_manager.EnumerateDevices():
                device_obj = bus.get_object("org.freedesktop.UDisks", dev)
                device_props = dbus.Interface(device_obj, dbus.PROPERTIES_IFACE)

                if device_props.Get('org.freedesktop.UDisks.Device', "DriveVendor") == "Kindle":
                    mountPaths = device_props.Get('org.freedesktop.UDisks.Device', "DeviceMountPaths")
                    if len(mountPaths) > 0:
                        self.vendor = device_props.Get('org.freedesktop.UDisks.Device', "DriveVendor")
                        for point in mountPaths:
                            self.mountPoint = point
                        self.serial = device_props.Get('org.freedesktop.UDisks.Device', "DriveSerial")
                        self.size = device_props.Get('org.freedesktop.UDisks.Device', "PartitionSize")

            print(self.mountPoint)

        return False

    def _listenOnUsb(self):
        context = Context()
        monitor = Monitor.from_netlink(context)

        monitor.filter_by(subsystem="usb")
        observer = MonitorObserver(monitor)
        observer.connect("device-event", self._deviceEvent)
        monitor.start()

        glib.MainLoop().run()

    def _deviceEvent(observer, device, action = ""):
        if hasattr(device, "action"):
            action = device.action

        print("event {0} on device {1}".format(action, device))

    def _getBooks(self):
        """ Traverse the documents directory where the books are stored """
        for root, dirs, files in os.walk(self.driveLetter + "\\documents"):
            for name in files:
                if re.search("\.mobi|\.pdf", name, re.IGNORECASE):
                    print(root + "\\" + name)

    def printInfo(self):
        """ Print out some info about the device """
        try:
            with open(self.mountPoint + "\\system\\version.txt") as fd:
                print("Version: " + fd.readline().strip())
            print("Device Name: " + self.name)
            print("Description: " + self.description)
            print("Mount Point: " + self.mountPoint)
        except (AttributeError):
            print("No device detected.")

if __name__ == "__main__":
    pydle = Pydle(sys.platform)
    # pydle.printInfo()

