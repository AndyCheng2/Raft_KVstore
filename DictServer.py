import socket
import threading
import sys
import pickle
import hashlib
import string
import random
from Operation import Operation


class KVStore:
    def __init__(self, dicID):
        self._dict = dict()
        self.dictID = dicID

    def __repr__(self):
        return repr(self._dict)

    def get(self, key):
        try:
            return self._dict[key]
        except TypeError:
            return None

    def put(self, key, value):
        self._dict[key] = value

    def processBlock(self, block):
        # print("+++++++++++++++++debug++++++++++ get into processBlock?" )
        op = block.operation
        if op.type == "put":
            self.put(op.key, op.value)


class Block:

    @classmethod
    def _successfulNonceHash(cls, _hash):
        if _hash == None:
            return False
        else:
            return _hash % 10 <= 2

    @classmethod
    def _calculateNonce(cls, operation_n):
        "Returns Nonce_n such that SHA256(Operation_n|Nonce_n) satisfies cls._successfulNonceHash()"
        _hash = None
        while not(cls._successfulNonceHash(_hash)):
            # Generating random string of size 10 for nonce
            nonce = ''.join(random.choice(string.ascii_letters)
                            for i in range(10))
            hashFunc = hashlib.sha256()
            hashFunc.update(repr(operation_n).encode() + nonce.encode())
            # Convert from hex to decimal
            _hash = int(hashFunc.hexdigest(), 16)

        print(f"Calculated nonce {nonce} such that h = {str(_hash)[-10:]}")
        return nonce

    @classmethod
    def _calculateHashPointer(cls, prevBlock):
        "Returns HashPointer_n+1 = SHA256(Operation_n|Nonce_n|HashPointer_n) as a hexadecimal string"
        if prevBlock is None:
            return None
        else:
            hashFunc = hashlib.sha256()
            hashFunc.update(repr(prevBlock.operation).encode() +
                            prevBlock.nonce.encode())
            if prevBlock.hashPointer:
                hashFunc.update( prevBlock.hashPointer.encode() )
            return hashFunc.hexdigest()[-10:]


    def __init__(self, operation, nonce, hashPointer, requestID, currentTerm, status="commited"):
        self.currentTerm = currentTerm
        self.operation = operation
        self.hashPointer = hashPointer
        self.nonce = nonce
        self.requestID = requestID
        self.status = status

    def __hash__(self):
        return hash( (self.operation, self.hashPointer, self.nonce, self.requestID, self.currentTerm) )

    def __eq__(self, other):
        return  self.operation == other.operation and\
                self.hashPointer == other.hashPointer and\
                self.nonce == other.nonce and\
                self.requestID == other.requestID and\
                self.currentTerm == other.currentTerm

    @classmethod
    def Create(cls, operation, requestID, currentTerm, prevBlock):
        nonce = cls._calculateNonce(operation)
        hashPointer = cls._calculateHashPointer(prevBlock)
        return cls(operation, nonce, hashPointer, requestID, currentTerm)

    def __repr__(self):
        return f"Block({repr(self.operation)}, {repr(self.nonce)}, {repr(self.hashPointer)}, {repr(self.requestID)}, {repr(self.requestID)} , {repr(self.status)})"


class Blockchain:
    def __init__(self, serverID):
        self._list = list()
        self.depth = 0  # Next index that is either empty or has a tentative block
        self.serverID = serverID
        self.lastAcceptedRequestID = None
        self.lastDecidedRequestID = None

    def __repr__(self):
        return repr(self._list)

    def append(self, block):
        self._list.append(block)

    def resize(self, size):
        self._list = self._list[:size]

    def accept(self, block, index):
        if self.lastAcceptedRequestID == block.requestID or self.lastDecidedRequestID == block.requestID:
            # Do nothing, already accepted/decided this request
            return
        if index == len(self._list):
            self._list.append(block)
        else:
            self._list[index] = block
        self.lastAcceptedRequestID = block.requestID

    def decide(self, block, index):
        if self.lastDecidedRequestID == block.requestID:
            # Do nothing, already decided this request
            return
        block.status = "decided"
        self._list[index] = block
        self.depth += 1
        self.lastDecidedRequestID = block.requestID

    def generateKVStore(self):
        "Returns the KVStore generated from performing the blockchain's operations in order"
        kvdic = dict()
        for block in self._list:
            op = block.operation
            if op.type == "put":
                if int(op.aim) in kvdic:
                    kvdic[int(op.aim)].put(op.key, op.value)
                else:
                    # print(f"Aimed kvstore{op.aim} is not exist")
                    pass
            elif op.type == "get":
                pass
            elif op.type == "create":
                for ID in op.value:
                    if self.serverID == ID:
                        kvstore = KVStore(int(op.aim))
                        kvdic[int(op.aim)] = kvstore
            else:
                raise Exception(f"Invalid operation type: {op.type}")
        return kvdic

    @ classmethod
    def read(cls, filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError as e:
            print(e)
            return cls()

    def write(self, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @property
    def list(self):
        return self._list
