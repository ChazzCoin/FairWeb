import time

import socketio

from F import DATE
from F.CLASS import FairClass
from FW.FairSocket.Message import FairMessage
import F


"""
    -> For Connecting to a Server.
    -> One Way Communication to Server.
        - This Client is not opened up and waiting for outside messages.
"""

class FairClient(FairClass):
    serverUrl = 'http://localhost:3671'
    clientId = F.get_uuid()
    socket = socketio.Client()
    userName = "FairClient"
    messages = {}
    callback = False
    eventName = "onMessage"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.serverUrl:
            self.serverUrl = input("Server Url -> ")
        self.event_binder()
        # firstInput = input("Who do you want to message?")

    def connect(self):
        self.socket.connect(self.serverUrl)

    def event_binder(self):
        funcs = self.get_method_names(self)
        for func in funcs:
            if str(func).startswith("on"):
                eventName = str(func)
                eventFunc = self.get_func(func)
                self.register_event(eventName, eventFunc)
        self.register_user_event()

    def register_event(self, eventName, eventFunction):
        self.socket.on(eventName)(eventFunction)

    def register_user_event(self):
        if self.userName:
            eventFunc = self.get_func("onMessage")
            self.register_event(self.userName, eventFunc)

    def emitOnConnect(self):
        self.socket.emit("onConnect", { "fromEventName": self.eventName, "userName": self.userName })

    def emit(self, eventName:str, eventMessage):
        self.socket.emit(eventName, eventMessage)

    def onMessage(self, data):
        fm = FairMessage().fromJson(data)
        if not fm:
            print(f"-> {data} ")
        else:
            if fm.userName == self.userName:
                return
            self.addToMessages(fm)
            print(f"{fm.userName}-> {fm.message}")
        self._sendCallback(data=data)

    def addToMessages(self, fairMessage):
        dateTime = DATE.get_log_date_time_dt()
        self.messages[dateTime] = fairMessage

    def onResponse(self, data):
        print(data)  # {'from': 'server'}

    def _sendCallback(self, data):
        if self.callback:
            self.callback(data)

def startWebSocketClient(serverUrl=None):
    socket = FairClient(serverUrl=serverUrl)
    socket.connect()
    return socket


if __name__ == '__main__':
    sock = FairClient(userName="terminal")
    messObj = FairMessage()
    sock.connect()
    sock.emitOnConnect()
    sock.emit("onGetUsers", {"fromEventName": "onMessage"})
    while True:
        time.sleep(1)
        mess = input("\n$ ")
        fm = FairMessage(message=mess, userName="terminal")
        sock.emit("onMessage", fm.toJson())
        time.sleep(1)