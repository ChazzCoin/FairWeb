import time
import F
from F import OS
from F.CLASS import Thread, FairClass
from FW.FairSocket import Client, Server

"""
    -> Two Way Communication between Server/Clients.
        - This Server is opened up and waiting for outside messages.
"""
ngrokToken = ""

class FairSocket(FairClass):
    socketManagerId = F.get_uuid()
    socketManagerName = f"FairServer:{OS.get_username()}"
    server = None
    client = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server = Server.FairServer()
        Thread.runFuncInBackground(Server.FairServer().start)
        # self.server.start()
        print("Yep, we're still running.")
        time.sleep(5)
        # Client.startWebSocketClient(serverUrl="http://localhost:3671")
        self.client = Client.FairClient(serverUrl="http://localhost:3671")
        self.client.connect()
        self.client.emit("onPrinter", "What up!!!!!!!!")
        tester = input("Give me something: ")
        self.client.emit("onPrinter", tester)



if __name__ == '__main__':
    FairSocket()