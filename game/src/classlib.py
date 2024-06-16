import os, json5, wcwidth, zlib
from typing import Any, Callable


class Player:
    def __init__(self, name: str = "player") -> None:
        self.name = name
        self.location = "home"
        self.stage_lv = 0  # 關卡等級
        self.lv = 0  # 人物等級
        self.language = "zh-tw"
        self.money = 100
        self.bag = Bag(dict(), default=0)
        self.account = BankAccount(self.name)
        self.modifier = abs(zlib.adler32(name.encode()) - 4294967295) / 8589934590 + 0.5

    def update(self, data: dict) -> None:
        for k, v in data.items():
            if k == "bag":
                self.bag = Bag({}, default=0)
                self.bag.loadItem(v)
            elif k == "account":
                self.account = BankAccount(self.name)
                self.account.money = v[0]
                self.account.bag = Bag({}, default=0)
                self.account.bag.loadItem(v[1])
            else:
                self.__dict__[k] = v

    def serialize(self) -> dict:
        temp = {}
        for k, v in self.__dict__.items():
            if k == "bag":
                t = {}
                for k0, v0 in self.bag.items():
                    t[k0.id] = v0
                temp[k] = t
            elif k == "account":
                t = {}
                for k0, v0 in self.account.bag.items():
                    t[k0.id] = v0
                temp[k] = [self.account.money, t]
            else:
                temp[k] = v
        return temp

    def save_archive(self, path: str = None) -> None:
        if path is None:
            path = save_dir + f"\\{self.name}.json5"
        while True:
            if os.path.isfile(path):
                option = input(f"{TEXT['save_archive_0']}\n[1.{TEXT['save_archive_1']}][2.{TEXT['save_archive_2']}][3.{TEXT['save_archive_3']}]:")
                match option:
                    case "1":
                        path = save_dir + "\\" + input(TEXT["save_archive_4"]) + ".json5"
                        continue
                    case "2":
                        pass
                    case "3":
                        break
                    case _:
                        print(TEXT["input_error"])
                        continue
            with open(path, "w+") as f:
                t = json5.dumps(self.serialize())
                if isinstance(t, str):
                    f.write(t)
                else:
                    raise TypeError("The output of json5.dumps is not a string.")
                break


class my_dict(dict):
    def __init__(self, *dicts: dict, default=None) -> None:
        if len(dicts) > 0:
            di = dicts[0]
            for d in dicts:
                for k, v in d.items():
                    if k not in di:
                        di[k] = v
        else:
            di = dict()
        super().__init__(di)
        self.default = default

    def __getitem__(self, key: str) -> str | Any:
        if key in self:
            return super().__getitem__(key)
        if self.default is None:
            return f"text ['{key}'] not found"
        return self.default


class BankAccount:
    def __init__(self, account: str) -> None:
        self.money = 0
        self.name = account
        self.bag = Bag(dict(), default=0)
        self.credit = 100

    def withdraw(self, amount: int) -> int:
        if self.money <= amount:
            self.money -= amount
            return self.money
        else:
            return -1


class Item:
    def __init__(self, id: str) -> None:
        data = ITEM[id]
        self.name = ITEMNAME[id][0]
        self.id = id
        self.price = data["price"]
        self.decoration = ITEMNAME[id][1]
        self.type = data["type"]
        if "content" in data:
            self.content = data["content"]

    def __str__(self) -> str:
        if self.decoration == 1 or self.decoration == 2:
            name = self.name
            name = name.replace(TEXT["creat_item_0"], f"\033[32m{TEXT['creat_item_0']}\033[0m")
            name = name.replace(TEXT["creat_item_1"], f"\033[34m{TEXT['creat_item_1']}\033[0m")
            name = name.replace(TEXT["creat_item_2"], f"\033[35m{TEXT['creat_item_2']}\033[0m")
            name = name.replace(TEXT["creat_item_3"], f"\033[47m{TEXT['creat_item_3']}\033[0m")
            name = name.replace(TEXT["creat_item_4"], f"\033[43m{TEXT['creat_item_4']}\033[0m")
            name = name.replace(TEXT["creat_item_5"], f"\033[42m{TEXT['creat_item_5']}\033[0m")
            name = name.replace(TEXT["creat_item_6"], f"\033[46m{TEXT['creat_item_6']}\033[0m")
            name = name.replace(TEXT["creat_item_7"], f"\033[44m{TEXT['creat_item_7']}\033[0m")
            name = name.replace(TEXT["creat_item_8"], f"\033[41m{TEXT['creat_item_8']}\033[0m")
            name = name.replace(TEXT["creat_item_9"], f"\033[40m{TEXT['creat_item_9']}\033[0m")
            name = name.replace(TEXT["creat_item_10"], f"\033[45m{TEXT['creat_item_10']}\033[0m")
            name = name.replace(TEXT["creat_item_11"], f"\033[47m{TEXT['creat_item_11']}\033[0m")
            name = name.replace(TEXT["creat_item_12"], f"\033[42m{TEXT['creat_item_12']}\033[0m")
            name = name.replace(TEXT["creat_item_13"], f"\033[40m{TEXT['creat_item_13']}\033[0m")
            name = name.replace(TEXT["creat_item_14"], f"\033[41m{TEXT['creat_item_14']}\033[0m")
            name = name.replace(TEXT["creat_item_15"], f"\033[43m{TEXT['creat_item_15']}\033[0m")
            name = name.replace(TEXT["creat_item_16"], f"\033[32m{TEXT['creat_item_16']}\033[0m")
            name = name.replace(TEXT["creat_item_17"], f"\033[36m{TEXT['creat_item_17']}\033[0m")
            name = name.replace(TEXT["creat_item_18"], f"\033[31m{TEXT['creat_item_18']}\033[0m")
            return name
        else:
            return self.name

    def __format__(self, format_space) -> str:
        return self.__str__()


class Bag(my_dict):
    def __init__(self, *dicts: dict, default=None) -> None:
        super().__init__(*dicts, default=default)

    def renew(self) -> None:
        for k, v in list(self.items()):
            if v <= 0:
                del self[k]

    def getItem(self) -> tuple[Item, int]:
        self.show()
        while True:
            item = input(TEXT["store_item_0"])
            if item == "-1":
                return -1, -1
            try:
                item = int(item)
            except ValueError:
                print(TEXT["store_item_1"])
                continue
            if item < 1 or item > len(self):
                print(TEXT["store_item_2"])
                continue
            item = list(self)[item - 1]
            quantity = input(TEXT["store_item_3"])
            if quantity == "-1":
                return -1, -1
            try:
                quantity = int(quantity)
            except TypeError:
                print(TEXT["store_item_1"])
                continue
            if quantity < 1:
                print(TEXT["store_item_4"])
                continue
            if quantity > self[item]:
                print(TEXT["store_item_5"])
                continue
            return item, quantity

    def show(self) -> None:
        if len(self) != 0:
            l0 = max(len(str(len(self))), len(TEXT["show_1"]))
            l1 = max(max(len(k.name) for k in self), len(TEXT["show_1"]))
            l2 = max(max(len(str(v)) for v in self.values()), len(TEXT["show_1"]))
            i = 1
            print(f"{TEXT['show_0']:^{l0+2}}{TEXT['show_1']:^{l1+2}}{TEXT['show_2']:^{l2+2}} {TEXT['show_3']}")
            for k, v in self.items():
                print(f"[{str(i)+'.':<{l0+1}}][{k:<{l1}}][{v:<{l2}}][{k.price}]")
                i += 1
        else:
            print(f"{TEXT['show_0']} {TEXT['show_1']} {TEXT['show_2']} {TEXT['show_3']}")
            print(TEXT["show_4"])

    def loadItem(self, itemDict: dict | my_dict) -> None:
        for k, v in itemDict.items():
            if isinstance(k, str):
                k = Item(k)
            self[k] += v


def init(data: str, save: str) -> tuple[my_dict[str:str], Player]:
    global data_dir, save_dir, default_language, ITEM, TEXT, CONFIG, ITEMNAME, player

    def switch_language(language: str) -> None:
        global TEXT
        with open(data_dir + "\\" + language + "\\text.json5", "r") as f:
            data = json5.load(f)
        if language != default_language:
            with open(data_dir + "\\" + default_language + "\\text.json5", "r") as f:
                TEXT = my_dict(data, json5.load(f))
        else:
            TEXT = my_dict(data)

    def load_archive() -> Player | None:
        while True:
            option = input(TEXT["create_role_0"])
            if option == "-1":
                break
            path = save_dir + "\\" + option + ".json5"
            if os.path.isfile(path):
                p = Player()
                with open(path, "r") as f:
                    p.update(json5.load(f))
                switch_language(p.language)
                return p
            else:
                print(TEXT["create_role_1"])

    def create_role() -> Player | None:
        while True:
            option = input(f"[1.{TEXT['create_role_2']}][2.{TEXT['create_role_3']}][3.{TEXT['create_role_4']}]:")
            if option == "1":
                p = load_archive()
                if p is None:
                    continue
                return p
            elif option == "2":
                return Player(input(TEXT["create_role_5"]))
            elif option == "3":
                return
            else:
                print(TEXT["input_error"])

    data_dir = data
    save_dir = save
    with open(data_dir + "\\config.json5", "r") as f:
        CONFIG = my_dict(json5.load(f))
    default_language = CONFIG["default_language"]
    with open(data_dir + "\\" + default_language + "\\text.json5", "r") as f:
        TEXT = my_dict(json5.load(f))
    with open(data_dir + "\\" + default_language + "\\item_name.json5", "r") as f:
        ITEMNAME = my_dict(json5.load(f))
    with open(data_dir + "\\item_list.json5", "r") as f:
        ITEM = my_dict(json5.load(f))
    switch_language(default_language)
    print(TEXT["hello_message"])
    player = create_role()
    if player is None:
        exit()
    return TEXT, player


def locationDecorator(fn) -> Callable:
    def f(*args, **kwargs) -> Any:
        location = player.location
        result = fn(*args, **kwargs)
        player.location = location
        return result

    return f
