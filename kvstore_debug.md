# KV store Debug



+  public and private keys
+  public keys of all other clients
+  A copy of the replicated log and other states needed for Raft（ (e.g. currentTerm & votedFor)）





+ **Create dictionary**（dictionary id, dictionary member client ids, dictionary public key, encrypted versions of the dictionary private key with the members’ public keys）
+ **Put operation**（dictionary id, the issuing client’s client id, and the key-value pair (to be put into the dictionary) encrypted with the dictionary’s public key）
+ **Get operation**（dictionary id, the issuing client’s client id, and the key (to get a corresponding value from the dictionary) encrypted with the dictionary’s public key）
+ raft data





```
blockchain 
print bl
bl:
set()
print bc
bc:
[Block(Operation('put', key=1, value=1), 'rQwKardgzf', None, (0, 7001), 'decided'),
 Block(Operation('get', key=1, value=None), 'yAVizWRNiW', '80769a6960', (1, 7001), 'decided'),put 
 Block(Operation('put', key=2, value=2), 'EtGpzGYhEL', 'bc8535c128', (2, 7001), 'decided'),
 Block(Operation('get', key=2, value=None), 'sEzTNznkKi', 'c86cb2e762', (3, 7001), 'decided')]
print kv
kv:
{1: 1, 2: 2}
print rq
rq:
deque([])
print sl
sl:
[('192.168.56.1', 8001), ('192.168.56.1', 8002), ('192.168.56.1', 8003)]
print depth
depth:
4
print
```



debug

```
Received message "None" from machine at ('172.30.144.1', 8001)
[CLIENT 1] Received query response: None
```

```
newMessage
[b'gAAAAABkFAJehtx-ULavDIVj85VtAsGb9Z-tagyjR7J0WU0tJqXpO4mJfX_l03Zge-DD4SyJcyMb16bxOTwYedgFNyJD7A0YZvSBTd9T7Fw24qj1Suvd6lnF2Lfv5O35WV_QiH3BaTmbyjH9b0c8WkNOiNu0aC2LRrXcUjQzl1FWiivL3aR2C88QC75RlJwav_FviWwWfMBQ', 1]
```



debug

```
create 3 (x,y,z)
create 4 (x,y,z,w)
create 5 (x,y,z,w,r)
create 2 (x,y)
create 2 (w,r)

create 2 (x,y)
create 3 (x,r,w)


put 1 98 4
put 0 97 4
get 0 4
put 1 1 1
get 3 2
get 1 1
put 3 'abc' 5
put 3 'xyz' 2
get 2 3
failLink x
fixLink x
failProcess

        Telling Leader...

Commands:
        See log: b
        See kvstore: k
        Do failProcess: failProcess
        Do failLink: failLink
        Do fixLink: fixLink
        Quit: q
Enter command: Message recieved: {'type': 'create', 'result': 'Success', 'clientPort': 7400}
```





```
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.8/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "server.py", line 448, in setupListeningSocket
    self.currentState.sendReqVoteMessage(self, reqVoteMsg)
TypeError: sendReqVoteMessage() takes 2 positional arguments but 3 were given
```



```
Traceback (most recent call last):
  File "server.py", line 634, in <module>
    server = Server(sys.argv[1], state)
  File "server.py", line 128, in __init__
    self.run()
  File "server.py", line 134, in run
    self.setupCommandTerminal()
  File "server.py", line 179, in setupCommandTerminal
    self.handle_input(command)
  File "server.py", line 296, in handle_input
    self.myselfExcute(data)
  File "server.py", line 359, in myselfExcute
    elif (len(data["data"]) == 4) and (data["data"][0] == 'create'):
TypeError: list indices must be integers or slices, not str
```





```
Enter command: create 2 (x,y)
Calculated nonce MNJzIfTUOQ such that h = 3162614061
Message recieved: {'type': 'create', 'result': 'Not in subset'}

Block(Operation('create', key=b'FvnrECZCRFUoOv1oIWGwWfmw68dmL2XJiU5aFYpbnm4=', value='(x,y)', aim=5), 'MNJzIfTUOQ', None, 0, 0 , 'tentative')
Length of blockchain: 1
```





```
put 1 abc 6


Traceback (most recent call last):
  File "server.py", line 634, in <module>
    state = Follower()
  File "server.py", line 128, in __init__
    self.run()
  File "server.py", line 134, in run
    self.setupCommandTerminal()
  File "server.py", line 179, in setupCommandTerminal
    else:
  File "server.py", line 204, in handle_input
    key = eval(data[1])
  File "<string>", line 1, in <module>
NameError: name 'abc' is not defined
```



```
Enter command: Sending HEARTBEAT
put 1 2 1
put 1 'abc' 1
Calculated nonce FtdwJIcJcN such that h = 4120325812
Message recieved: {'type': 'put', 'result': 'For now server, dicID is not exist'}Enter command: Sending HEARTBEAT
put 1 'abc' 1
Calculated nonce FtdwJIcJcN such that h = 4120325812
Message recieved: {'type': 'put', 'result': 'For now server, dicID is not exist'}


put 1 2 1
Calculated nonce CCkOlXrBSo such that h = 8937206610
Message recieved: {'type': 'put', 'result': 'For now server, dicID is not exist'}
```





```
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.8/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "server.py", line 464, in setupListeningSocket
    op = Operation.Create(data[1], data[2], data[3])
IndexError: list index out of range
```



```
['create', b'vm8_23XGm91C4307GZfPhPVTm9iKCepNbLFNTYLjqOU=', '(x,y)', 5]
data:
{'data': [b'gAAAAABkFDTNo_9PVpw0sz27xGgs5FcgnLvrMNf5MpL51pYJ8XoLMCZiX85lxKRB7k21CmVpmNv872MEAh8w5nVRyPsZVVlhriYVxp7j2fBepQUeenPNchFBOq7lBHVUNn62yDXB_faklnm5vZ_43aVRmZoGVcpPpC8QsvL-zHy2UhK-zZKGHwWaZysHrNIewNGOv44AFp2X', ['create', b'vm8_23XGm91C4307GZfPhPVTm9iKCepNbLFNTYLjqOU=', '(x,y)', 5], 5], 'clientPort': 7500}
```



```
++++++++++++++debug get into get answer wrong
++++++++++++++debug now operation.aim(10)
<class 'str'>
++++++++++++++debug now dic list:10
<class 'int'>
<class 'DictServer.KVStore'>
Calculated nonce eqeuiCmQrW such that h = 1285333950
Message recieved: {'type': 'put', 'result': 'For now server, dicID is not exist'}
```



```
Traceback (most recent call last):
  File "server.py", line 667, in <module>
    server = Server(sys.argv[1], state)
  File "server.py", line 128, in __init__
    self.run()
  File "server.py", line 134, in run
    self.setupCommandTerminal()
  File "server.py", line 180, in setupCommandTerminal
    self.handle_input(command)
  File "server.py", line 219, in handle_input
    self.myselfExcute(data)
  File "server.py", line 350, in myselfExcute
    curr_result = self._getAnswer(op)  # 如果能访问dic，getAnswer这里面会put key value
  File "server.py", line 621, in _getAnswer
    self.kvdic[operation.aim].put(operation.key, operation.value)
KeyError: '11'
```



```
t 1 12
Calculated nonce eUVBtNfsCs such that h = 0423984280
Message recieved: {'type': 'get', 'result': 'KEY_DOES_NOT_EXIST'}
Sending HEARTBEAT
Traceback (most recent call last):
  File "server.py", line 668, in <module>
    server = Server(sys.argv[1], state)
  File "server.py", line 128, in __init__
    self.run()
  File "server.py", line 134, in run
    self.setupCommandTerminal()
  File "server.py", line 180, in setupCommandTerminal
    self.handle_input(command)
  File "server.py", line 243, in handle_input
    if aim in self.kvdic and key in self.kvdic[aim]:
TypeError: argument of type 'KVStore' is not iterable
```

```
receive data[b'gAAAAABkFEQHA0z445-O8wwOQAj4W4H2OTfr6pBTbmMXhUCcLaANl3FGKML9AKEtOw12T0sG3Tejb9mY6il9-Y3sF-pnvEuk993GYLgEc4tqBeXYzoe9brz6wNSD_fdz4E_71qTXUqOv', ['put', '1', '1', '13', 13], 13]
b'\x80\x04\x95\x18\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c\x03put\x94\x8c\x011\x94h\x02\x8c\x0213\x94K\re.'
['put', '1', '1', '13', 13]
```



```
{'data': [b'gAAAAABkFEZVXxd_rZjE-KmTYbuCDNLoTZFlZ6H1wr1Lwr0s87Tws6L9wiUVi1xgwwMGmtKoGT-nuSb_jfN1ynvbvwG1AK8oXtp-uMiPQzVIYpPGKS-o4xTHyc2r6u6T4TzccMfzMg0lPkEhQqdRlsgsalx7xYyQYdO3AN5vAHGC8epEngAw3kR0oX-VjL48H4RwX5_IDFWS', ['create', b'm-X_PlZC7TV8PL6NNwkxnjTNubh08q3eleYHCMujjts=', '(x,y)', 15], 15], 'clientPort': 7500}
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.8/threading.py", line 932, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.8/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "server.py", line 523, in setupListeningSocket
    op = Operation.Create(data[1], data[2], data[3])
IndexError: list index out of range
```



```
Traceback (most recent call last):
  File "server.py", line 700, in <module>
    if __name__ == '__main__':
  File "server.py", line 138, in __init__
    self.run()
  File "server.py", line 144, in run
    self.blockchain = Blockchain.read(saveFileName)
  File "server.py", line 176, in setupCommandTerminal
    print(block)
  File "server.py", line 327, in sendtoAllBeforeCrush
    for recID in serverConfig.SERVER_PORTS.keys():
NameError: name 'server' is not defined
```



