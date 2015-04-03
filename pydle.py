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

    @TODO   Linux and OS X compatibility
            processing and storing of note, bookmarks, highlights
"""

import win32com.client
import re
import os

class Pydle:
    def __init__(self):
        if self._detectDevice():
            self._getBooks()

    def _detectDevice(self):
        """ Hook into the Win32 API with win32com to retrieve Kindle device info """
        self.wmi = win32com.client.GetObject("winmgmts:")
        for usb in self.wmi.InstancesOf("Win32_USBControllerDevice"):
            if re.search("kindle", usb.Dependent, re.IGNORECASE):
                for logical_disk in self.wmi.InstancesOf("Win32_LogicalDisk"):
                    if re.search("kindle", logical_disk.VolumeName, re.IGNORECASE):
                        self.drive_letter = logical_disk.DeviceID
                        self.description = logical_disk.Description
                        self.name = logical_disk.VolumeName

                        return True
        return False

    def _getBooks(self):
        """ Traverse the documents directory where the books are stored """
        for root, dirs, files in os.walk(self.driveLetter + "\\documents"):
            for name in files:
                if re.search("\.mobi|\.pdf", name, re.IGNORECASE):
                    print(root + "\\" + name)

    def printInfo(self):
        """ Print out some info about the device """
        try:
            with open(self.drive_letter + "\\system\\version.txt") as fd:
                print("Version: " + fd.readline().strip())
            print("Device Name: " + self.name)
            print("Description: " + self.description)
            print("Drive Letter: " + self.drive_letter)
        except (AttributeError):
            print("No device detected.")

if __name__ == "__main__":
    pydle = Pydle()
    # pydle.printInfo()
