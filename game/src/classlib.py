class Player:
    def __init__(self, name: str = "player"):
        self.name = name
        self.location = 'home'
        self.stage_lv = 0  # 關卡等級
        self.lv = 0  # 人物等級
        self.language = "zh-tw"
        self.money = 100
        self.bag = my_dict(dict(), default=0)

    def update(self, data):
        for k, v in data.items():
            if k == "bag":
                self.bag = my_dict(v, default=0)
            else:
                self.__dict__[k] = v

    def serialize(self):
        temp = {}
        for k, v in self.__dict__.items():
            if k == "bag":
                temp[k] = self.bag.dict()
            else:
                temp[k] = v
        return temp


class my_dict(dict):
    def __init__(self, *dicts, default=None):
        super().__init__()
        self.dicts = dicts
        self.default = default

    def __getitem__(self, key):
        for dictionary in self.dicts:
            if key in dictionary:
                return dictionary[key]
        if self.default is None:
            return f"text ['{key}'] not found"
        return self.default

    def renew(self):
        for k, v in list(self.items()):
            if v <= 0:
                del self[k]
    
    def dict(self):
        temp = self.dicts[0]
        for d in self.dicts:
            temp.update(d)
        return temp
