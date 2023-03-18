import pickle

from messages.appendEntry import AppendEntry
from messages.serverToClient import ServerToClient
import socket
import serverConfig

class Leader:

    def __init__(self):
        self.nextIndex = 0
        self.liveProcess = 5

    def initiateLeader(self, server):
        self.nextIndex = server.lastLogIndex + 1
        self.sendHeartbeatToAll(server)
        print("\nAnnouncement HEARTBEAT sent to servers")
        for clientID in serverConfig.SERVER_PORTS.keys():
            if server.id != clientID:
                message = ServerToClient(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[clientID], serverConfig.SERVER_PORTS[server.id]
                )
                self.sendMessageToSocket(message)
            else:
                server.serverPort = serverConfig.SERVER_PORTS[server.id]
        print("Announcement sent to servers")
        server.currentInterval = server.defaultInterval

    def sendHeartbeatToAll(self, server):
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != server.id):
                heartbeat = AppendEntry(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[recID], server.id, server.lastLogTerm, server.lastLogIndex, [], 0
                )
                self.sendMessageToSocket(heartbeat)

    def sendMessageToSocket(self, appendEntryMessage):
        try:
            s = socket.socket()
            s.connect(("127.0.0.1", appendEntryMessage.receiver))
            dataString = pickle.dumps(appendEntryMessage)
            s.send(dataString)
            s.close()
        except socket.error as e:
            for id, port in serverConfig.SERVER_PORTS.items():
                if port == appendEntryMessage.receiver:
                    print("\tServer"+ str(id).upper()+" is down")

    def startAppendEntry(self, server, block):
        sender = server.id
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != sender):
                apmessage = AppendEntry(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[recID], server.id,
                    server.lastLogTerm, server.lastLogIndex-1, [block], 0
                )
                print("Sending APPENDENTRY to " + str(apmessage.receiver))
                self.sendMessageToSocket(apmessage)
        print("Sent AppendEntries to all servers")

    def sendWholeBlockchain(self, server: object, data: object) -> object:
        try:
            s = socket.socket()
            s.connect(("127.0.0.1", serverConfig.SERVER_PORTS[data.sender]))
            fname = server.backupBlockchainFileName
            flist = [fname, server.id]
            dataString = pickle.dumps(flist)
            s.send(dataString)
            s.close()
        except socket.error as e:
            print("Wrong happen")
