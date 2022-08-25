from flask import Flask
from flask_socketio import SocketIO
from pyngrok import ngrok
from pyngrok.ngrok import NgrokTunnel
# import schedule
import F
from F import OS
from F.CLASS import FairClass
from F.CLASS.Process import FairProcess
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

    def start_server(self):
        self.socket.run(app=self.app, host=self.host, port=self.port, debug=False)

    """ Master Connection Handler """
    def onConnect(self, data):
        print("ON CONNECTED!!!", data, self)
        user = self.get_arg("userName", data, default=False)
        fromEventName = self.get_arg("fromEventName", data)
        if fromEventName:
            self.clients.append(fromEventName)
        self.emit('onResponse', f"Welcome to the Game. {user}")

    """ Global Messenger for All Clients """
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

    def onFairCommand(self, data):
        commands = self.get_arg("commands", data, default=False)
        result = OS.run_command(commands)
        self.emit("onMessage", result)

    def onPrinter(self, data):
        print(f"Printer-> {data} ")

    def emit(self, eventName:str, eventMessage:{}):
        self.socket.emit(eventName, eventMessage)

    def sendFairMessage(self, eventName:str, fairMessage:FairMessage):
        self.socket.emit("onMessage", fairMessage.toJson())

    def sendResponse(self, eventMessage=None):
        if eventMessage is None:
            eventMessage = {}
        self.socket.emit("onResponse", eventMessage)

    def onStartProcess(self, data):
        """ Override This for Process Handling. """
        pass

    def onStopProcess(self, data):
        """ Override This for Process Handling. """
        pass

def startWebSocketServer():
    socket = FairServer()
    socket.start_server()
    return socket


class ProcessServer(FairServer):
    """ Runs a websocket server for remote control over local processes. """

    target_function = None
    target_arguments = None
    serverName = F.OS.get_username()
    socket = FairServer()
    fairProcess = FairProcess()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        start_process = self.get_arg("start_process", kwargs, default=False)
        if start_process:
            self.onStartProcess()

    def add_Target_Arguments(self, target, args):
        self.target_function = target
        self.target_arguments = args

    def onStartProcess(self, data=None):
        if self.target_arguments:
            self.fairProcess.set_process(self.target_function, self.target_arguments)
        else:
            self.fairProcess.set_process(self.target_function)
        self.fairProcess.start_process()
        self.sendResponse("Crawler has been Started.")

    def onStopProcess(self, data=None):
        self.fairProcess.stop_process()
        self.sendResponse("Crawler has been terminated.")

    def onIsRunning(self, data=None):
        if self.fairProcess.isRunning:
            self.sendResponse({"processIsRunning":"True"})
        else:
            self.sendResponse({"processIsRunning":"False"})

    def onGetServerName(self, data=None):
        self.sendResponse({"serverName":self.serverName})


# class ScheduleProcessServer(FairServer):
#     """ Runs a websocket server for remote control over local processes. """
#
#     target_function = None
#     target_arguments = None
#     serverName = F.OS.get_username()
#     socket = FairServer()
#     fairProcess = FairProcess()
#     fairSchedule = schedule
#     scheduledHours = 1
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.setSchedule()
#         while True:
#             self.fairSchedule.run_pending()
#
#     def setSchedule(self):
#         self.fairSchedule.every(self.scheduledHours).minute.do(self.__start_process)
#
#     def __start_process(self):
#         self.fairProcess.set_process(self.target_function, self.target_arguments)
#         self.fairProcess.start_process()
#
#     def isRunning(self):
#         if self.fairProcess.isRunning:
#             return True
#         else:
#             return False
#
#     def add_Target_Arguments(self, target, args):
#         self.target_function = target
#         self.target_arguments = args
#
#     def onStartProcess(self, data):
#         self.fairProcess.set_process(self.target_function, self.target_arguments)
#         self.fairProcess.start_process()
#         self.sendResponse("Crawler has been Started.")
#
#     def onStopProcess(self, data):
#         self.fairProcess.stop_process()
#         self.sendResponse("Crawler has been terminated.")
#
#     def onIsRunning(self, data):
#         if self.fairProcess.isRunning:
#             self.sendResponse({"processIsRunning":"True"})
#         else:
#             self.sendResponse({"processIsRunning":"False"})
#
#     def onGetServerName(self, data):
#         self.sendResponse({"serverName":self.serverName})


if __name__ == '__main__':
    socket = FairServer(makePublic=True)
    socket.start_server()