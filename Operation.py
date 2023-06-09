class Operation:
    def __init__(self, operationType, **kwargs):
        self.type = operationType
        self.key = None
        self.value = None
        self.aim = None

        if 'key' in kwargs:
            self.key = kwargs['key']

        if 'value' in kwargs:
            self.value = kwargs['value']
        if 'aim' in kwargs:
            self.aim = kwargs['aim']

    def __hash__(self):
        return hash((self.type, self.key, self.value,
                     self.aim))

    def __eq__(self, other):
        if self.type == other.type:
            if self.type == "get":
                return self.key == other.key and self.aim == other.aim
            elif self.type == "put":
                return self.key == other.key and self.value == other.value and self.aim == other.aim
            elif self.type == "create":
                return self.key == other.key and self.value == other.value and self.aim == other.aim
        return False

    @classmethod
    def Put(cls, key, value, aim):
        return cls("put", key=int(key), value=value, aim=int(aim))

    @classmethod
    def Get(cls, key, aim):
        return cls("get", key=int(key), aim=int(aim))

    @classmethod
    def Create(cls, key, value, aim):
        return cls("create", key=key, value=value, aim=int(aim))

    def __repr__(self):
        rep = f"Operation({repr(self.type)}"

        for k, v in vars(self).items():
            if k != "type":
                rep += f", {k}={repr(v)}"

        rep += ")"
        return rep
