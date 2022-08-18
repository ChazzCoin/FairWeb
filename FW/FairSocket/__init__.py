from FW.FairSocket.Message import FairMessage
# from Server import FairServer
# from Client import FairClient
from pyngrok import ngrok

def openNgrokPort(port, ngrokToken):
    if not ngrokToken:
        return
    tunnel = ngrok
    tunnel.set_auth_token(ngrokToken)
    publicURL = tunnel.connect(port, "http")
    print(f"\n{publicURL}\n")
    return tunnel


# def getWebSocketServer():
#     return FairServer()
#
# def startWebSocketServer():
#     socket = FairServer()
#     socket.start()
#     return socket


# def getWebSocketClient(serverUrl=None):
#     return FairClient(serverUrl=serverUrl)
#
# def startWebSocketClient(serverUrl=None):
#     socket = FairClient(serverUrl=serverUrl)
#     socket.connect()
#     return socket
#
# sock = FairClient(userName="chace")
# messObj = FairMessage()
# sock.connect()
# messObj.message = "you are gay?"
# messObj.senderEventName = "onMessage"
# sock.emit("onConnect", messObj.toJson())
# sock.emit("onGetUsers", {"fromEventName": "chace"})