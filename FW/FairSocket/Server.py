from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from pyngrok import ngrok
from pyngrok.ngrok import NgrokTunnel

import F
from F import OS
from F.CLASS import FairClass
from FW.FairSocket.Message import FairMessage


"""
    -> Two Way Communication between Server/Clients.
        - This Server is opened up and waiting for outside messages.
"""
ngrokToken = ""

class FairServer(FairClass):
    serverID = F.get_uuid()
    serverName = f"FairServer:{OS.get_username()}"
    app = None
    socket = None
    host = '0.0.0.0'
    port = 3671
    tunnel = ngrok
    ngrokToken = None
    publicURL: NgrokTunnel = ""
    #->
    clients = []
    subscribed_users = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = Flask(__name__)
        self.socket = SocketIO(self.app)
        if self.get_arg("makePublic", kwargs, default=False):
            self.make_public()
        self.event_binder()

    def make_public(self):
        if not self.ngrokToken:
            return
        self.tunnel.set_auth_token(self.ngrokToken)
        self.publicURL = self.tunnel.connect(self.port, "http")
        print(f"\n{self.publicURL}\n")

    def event_binder(self):
        funcs = self.get_method_names(self)
        for func in funcs:
            if str(func).startswith("on"):
                eventName = str(func)
                eventFunc = self.get_func(func)
                self.register_event(eventName, eventFunc)

    def register_event(self, eventName, eventFunction):
        self.socket.on(eventName)(eventFunction)

    def start(self):
        self.socket.run(app=self.app, host=self.host, port=self.port, debug=False)

    def onConnect(self, data):
        print("ON CONNECTED!!!", data, self)
        user = self.get_arg("userName", data, default=False)
        fromEventName = self.get_arg("fromEventName", data)
        if fromEventName:
            self.clients.append(fromEventName)
        self.emit('onResponse', f"Welcome to the Game. {user}")

    def onStartProcess(self, data):
        pass

    def onStopProcess(self, data):
        pass

    def onMessage(self, data):
        messageObj = FairMessage().fromJson(data)
        print(f" IN -> {messageObj.message}")
        sent = []
        for c in self.clients:
            if c in sent:
                continue
            sent.append(c)
            self.sendFairMessage(c, messageObj)

    def onGetUsers(self, data):
        fromEventName = self.get_arg("fromEventName", data, default=False)
        self.emit(fromEventName, self.clients)

    def onPrinter(self, data):
        print(f"Printer-> {data} ")

    def emit(self, eventName:str, eventMessage:{}):
        self.socket.emit(eventName, eventMessage)

    def sendFairMessage(self, eventName:str, fairMessage:FairMessage):
        self.socket.emit("onMessage", fairMessage.toJson())

def startWebSocketServer():
    socket = FairServer()
    socket.start()
    return socket


if __name__ == '__main__':
    socket = FairServer(initNgrok=True)
    socket.start()