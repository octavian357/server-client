#!/usr/bin/python

from os import close
import tkinter
from tkinter.constants import *
from typing import Text

from client import myClient

class clientApp():
    def __init__(self):
        self.port = None
        self.ipaddy = ''
        self.username = ''
        self.root = tkinter.Tk()
        self.messages = tkinter.StringVar()
        self.client = myClient()
        self.messageSet = set()
        
        self.welcomeLabel = tkinter.Label(self.root, text='Welcome to the server.', bd=1, relief=SUNKEN, anchor=W)
        self.errorLabel = tkinter.Label(self.root, text='Error! Please fill out all the fields.')
        #port stuff
        self.portLabel = tkinter.Label(self.root, text="Enter Port:")
        self.portEntry = tkinter.Entry(self.root, width=20, borderwidth=3)
        #ipaddy stuff
        self.ipaddyLabel = tkinter.Label(self.root, text="Enter IP Address:")
        self.ipaddyEntry = tkinter.Entry(self.root, width=20, borderwidth=3)
        #username stuff
        self.usernameLabel = tkinter.Label(self.root, text="Enter Username:")
        self.usernameEntry = tkinter.Entry(self.root, width=20, borderwidth=3)
        #self.usernameButton = tkinter.Button(self.root, text='Enter', command=self.enterUser)
        self.closeButton = tkinter.Button(self.root, text='Close', command= quit, anchor=E)
        #message stuff
        self.messageMessage = tkinter.Message(self.root, textvariable=self.messageSet, width=20)
        self.messageEntry = tkinter.Entry(self.root, width=20, borderwidth=3)

    def quit(self):
        self.root.destroy()
        
    def enter(self, meh):
        print(meh)
        if (self.usernameEntry.get() == '') | (self.portEntry.get() == '') | (self.ipaddyEntry.get() == ''):
            self.errorLabel.grid(row=2,column=2)
        else:
            self.port = int(self.portEntry.get())
            self.ipaddy = self.ipaddyEntry.get()
            self.username = self.usernameEntry.get()
            self.usernameEntry.delete(0,'end')
            self.errorLabel.destroy()
        
        if (self.username != '') & (self.port != '') & (self.ipaddy != ''):
            #destroy port
            self.portEntry.destroy()
            self.portLabel.destroy()
            #destroy ipaddy
            self.ipaddyEntry.destroy()
            self.ipaddyLabel.destroy()
            #destroy username
            self.usernameEntry.destroy()
            self.usernameLabel.destroy()
            
            self.welcomeLabel.config(text='Welcome ' + self.username + ' to the server.')
            
            self.client.clientConnect(self.port, self.ipaddy, self.username)
            self.client.stratClient()
            
            self.message()
    
    def message(self):
        self.root.geometry('640x280')
        self.messageMessage.grid(row=1)
        self.messageEntry.grid(row=2)
        self.messageEntry.bind('<Return>', self.packMessage)

    def packMessage(self, meh):
         self.messages.set(self.messageEntry.get())  
    
    def startApp(self):
        self.root.title("Client")
        
        self.welcomeLabel.grid(row=0, column=0, sticky=E+W)  
        #get port number
        self.portLabel.grid(row=3,column=0,pady=10)
        self.portEntry.grid(row=3,column=1,pady=10)
        self.portEntry.bind('<Return>', self.enter)
        #get ipaddy
        self.ipaddyLabel.grid(row=4,column=0,pady=10)
        self.ipaddyEntry.grid(row=4,column=1,pady=10)
        self.ipaddyEntry.bind('<Return>', self.enter)
        #username stuff     
        self.usernameLabel.grid(row=1,column=0,pady=10)
        self.usernameEntry.grid(row=1,column=1,pady=10)
        self.usernameEntry.bind('<Return>', self.enter)
        #self.usernameButton.grid(row=1,column=3,pady=10)
        #Close the App
        self.closeButton.grid(row=5, sticky=E)
        self.root.mainloop()

if __name__ == '__main__':            
    myApp = clientApp()
    myApp.startApp()