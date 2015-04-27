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
    Python frontend for Pydle class

"""

from tkinter import Tk, Listbox, Menu, TOP, BOTH, X, LEFT, RIGHT, N, W, S, E, FLAT, END
from ttk import Style, Button, Frame
from pydle import pydle

class App(Frame):
    version = "0.1"
    padding = 10
    screenWidth = 800
    screenHeight = 600

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.py = pydle()

        self._initUI()

    def _initUI(self):
        self.parent.title("Pydle v" + self.version)
        self.parent.minsize(width=str(self.screenWidth), height=str(self.screenHeight))
        # self.parent.config(border=0)

        # Styles
        style = Style()
        style.configure("TFrame", background="gray", border=0)
        style.configure("TButton", background="gray", foreground="lightgray", highlightforeground="black", highlightbackground="darkgray", compound=RIGHT, relief=FLAT)

        self.config(style="TFrame")
        self.pack(fill=BOTH, expand=1)

        # Menus
        mnuBar = Menu(self.parent)
        self.parent.config(menu=mnuBar)

        mnuFile = Menu(mnuBar, background="gray")
        mnuFile.add_command(label="Exit", command=self.onExitMnu)
        mnuBar.add_cascade(label="File", menu=mnuFile)

        mnuHelp = Menu(mnuBar, background="gray")
        mnuHelp.add_command(label="About", command=self.onAboutMnu)
        mnuBar.add_cascade(label="Help", menu=mnuHelp)

        # Frame content
        frmBooks = Frame(self, style="TFrame")
        frmBooks.pack(side=LEFT, anchor=N+W, fill=BOTH, expand=1, padx=(self.padding, self.padding / 2), pady=self.padding)

        self.lstBooks = Listbox(frmBooks)
        self.lstBooks.config(background="lightgray", foreground="black", borderwidth=0)
        self.lstBooks.pack(fill=BOTH, expand=1)

        frmButtons = Frame(self)
        frmButtons.pack(anchor=N+E, padx=(self.padding / 2, self.padding), pady=self.padding)

        btnLoadBooks = Button(frmButtons, text="Load Books", style="TButton", command=self.onLoadBooksBtn)
        btnLoadBooks.pack(side=TOP, fill=X)

        btnGetNotes = Button(frmButtons, text="Get Notes", style="TButton", command=self.onGetNotesBtn)
        btnGetNotes.pack(side=TOP, fill=X)

        btnBackupBook = Button(frmButtons, text="Backup Book", style="TButton", command=self.onBackupBtn)
        btnBackupBook.pack(side=TOP, fill=X)

        btnBackupAllBooks = Button(frmButtons, text="Backup All Books", style="TButton", command=self.onBackupAllBtn)
        btnBackupAllBooks.pack(side=TOP, fill=X)

    def onLoadBooksBtn(self):
        books = self.py.getBooks()

        for book in books:
            self.lstBooks.insert(END, book["name"])

    def onBackupBtn(self):
        pass

    def onBackupAllBtn(self):
        pass

    def onGetNotesBtn(self):
        notes = self.py.getNotes()

        for note in notes:
            self.lstBooks.insert(END, note)

    def onAboutMnu(self):
        pass

    def onExitMnu(self):
        self.onExit()

    def onExit(self):
        self.quit()


def main():
    root = Tk()
    # root.geometry("300x300+300+300")
    app = App(root)
    root.mainloop()

main()

