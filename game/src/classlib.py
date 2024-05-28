import os, json


def init(data, save, default):
    global data_dir, save_dir, default_language, TEXT, ITEM
    data_dir = data
    save_dir = save
    default_language = default
    with open(data_dir + "\\" + default_language + "\\text.json", "r") as f:
        TEXT = my_dict(json.load(f))
    with open(data_dir + "\\" + default_language + "\\itemList.json", "r") as f:
        ITEM = my_dict(json.load(f))
    return TEXT


class Player:
    def __init__(self, name: str = "player"):
        self.name = name
        self.location = "home"
        self.stage_lv = 0  # 關卡等級
        self.lv = 0  # 人物等級
        self.language = "zh-tw"
        self.money = 100
        self.bag = Bag(dict(), default=0)
        self.account = BankAccount(self.name)

    def update(self, data: dict):
        for k, v in data.items():
            if k == "bag":
                self.bag = Bag(v, default=0)
            else:
                self.__dict__[k] = v

    def serialize(self):
        temp = {}
        for k, v in self.__dict__.items():
            if k == "bag":
                temp[k] = self.bag
            else:
                temp[k] = v
        return temp


class my_dict(dict):
    def __init__(self, *dicts: dict, default=None):
        di = dicts[0]
        for d in dicts:
            for k, v in d.items():
                if k not in di:
                    di[k] = v
        super().__init__(di)
        self.default = default

    def __getitem__(self, key: str):
        if key in self:
            return super().__getitem__(key)
        if self.default is None:
            return f"text ['{key}'] not found"
        return self.default


class Bag(my_dict):
    def __init__(self, *dicts: dict, default=None):
        super().__init__(*dicts, default=default)

    def renew(self):
        for k, v in list(self.items()):
            if v <= 0:
                del self[k]

    def getItem(self):
        self.show()
        while True:
            item = input(TEXT["store_item_0"])
            if item == "-1":
                break
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

    def show(self):
        if len(self) != 0:
            l0 = len(str(len(self)))
            l1 = max(len(k.name) for k in self)
            l2 = max(len(str(v)) for v in self.values())
            i = 1
            print(f"{TEXT['show_0']:^{l0+2}}{TEXT['show_1']:^{l1+2}}{TEXT['show_2']:^{l2+2}} {TEXT['show_3']}")
            for k, v in self.items():
                print(f"[{str(i)+'.':<{l0+1}}][{k:<{l1}}][{v:<{l2}}][{k.price}]")
                i += 1
        else:
            print(f"{TEXT['show_0']} {TEXT['show_1']} {TEXT['show_2']} {TEXT['show_3']}")


class PlayerManager:
    def __init__(self):
        self.switch_language(default_language)

    def switch_language(self, language: str):
        global TEXT
        with open(data_dir + "\\" + language + "\\text.json", "r") as f:
            data = json.load(f)
        if language != default_language:
            with open(data_dir + "\\" + default_language + "\\text.json", "r") as f:
                TEXT = my_dict(data, json.load(f))
        else:
            TEXT = my_dict(data)

    def create_role(self):
        def load_archive():
            while True:
                inp = input(TEXT["create_role_0"])
                if inp == "-1":
                    return
                path = save_dir + "\\" + inp + ".json"
                if os.path.isfile(path):
                    player = Player()
                    with open(path, "r") as f:
                        player.update(json.load(f))
                    self.switch_language(player.language)
                    return player
                else:
                    print(TEXT["create_role_1"])

        while True:
            option = input(f"[1.{TEXT['create_role_2']}][2.{TEXT['create_role_3']}][3.{TEXT['create_role_4']}]:")
            if option == "1":
                player = load_archive()
                if player is None:
                    continue
                return player
            elif option == "2":
                return Player(input(TEXT["create_role_5"]))
            elif option == "3":
                return
            else:
                print(TEXT["input_error"])

    def save_archive(self, player: Player, path=None):
        if path is None:
            path = save_dir + f"\\{player.name}.json"
        while True:
            if os.path.isfile(path):
                inp = input(f"{TEXT['save_archive_0']}\t[1.{TEXT['save_archive_1']}][2.{TEXT['save_archive_2']}][3.{TEXT['save_archive_3']}]:")
                match inp:
                    case "1":
                        path = save_dir + "\\" + input(TEXT["save_archive_4"]) + ".json"
                        continue
                    case "2":
                        pass
                    case _:
                        return
            with open(path, "w+") as f:
                f.write(json.dumps(player.serialize()))
                return


class BankAccount:
    def __init__(self, account: str):
        self.money = 0
        self.name = account
        self.bag = Bag(dict(), default=0)
        self.credit = 100

    def deposit(self, amount: int):
        self.money += amount
        return self.money

    def withdraw(self, amount: int):
        if self.money <= amount:
            self.money -= amount
            return self.money
        else:
            return -1


class CreatItem:
    def __init__(self, id):
        self.id = id
        data = ITEM[id]
        self.name = data["name"]
        self.price = data["price"]
        self.decoration = data["decoration"]

    def __str__(self):
        if self.decoration == 0:
            return self.name
        elif self.decoration == 1:
            name = self.name
            name.replace(TEXT["creat_item_0"], f"\033[32m{TEXT['creat_item_0']}\033[0m")
            name.replace(TEXT["creat_item_1"], f"\033[34m{TEXT['creat_item_1']}\033[0m")
            name.replace(TEXT["creat_item_2"], f"\033[35m{TEXT['creat_item_2']}\033[0m")
            name.replace(TEXT["creat_item_3"], f"\033[47m{TEXT['creat_item_3']}\033[0m")
            name.replace(TEXT["creat_item_4"], f"\033[43m{TEXT['creat_item_4']}\033[0m")
            name.replace(TEXT["creat_item_5"], f"\033[42m{TEXT['creat_item_5']}\033[0m")
            name.replace(TEXT["creat_item_6"], f"\033[46m{TEXT['creat_item_6']}\033[0m")
            name.replace(TEXT["creat_item_7"], f"\033[44m{TEXT['creat_item_7']}\033[0m")
            name.replace(TEXT["creat_item_8"], f"\033[41m{TEXT['creat_item_8']}\033[0m")
            name.replace(TEXT["creat_item_9"], f"\033[40m{TEXT['creat_item_9']}\033[0m")
            name.replace(TEXT["creat_item_10"], f"\033[45m{TEXT['creat_item_10']}\033[0m")
            name.replace(TEXT["creat_item_11"], f"\033[47m{TEXT['creat_item_11']}\033[0m")
            name.replace(TEXT["creat_item_12"], f"\033[42m{TEXT['creat_item_12']}\033[0m")
            name.replace(TEXT["creat_item_13"], f"\033[40m{TEXT['creat_item_13']}\033[0m")
            name.replace(TEXT["creat_item_14"], f"\033[41m{TEXT['creat_item_14']}\033[0m")
            name.replace(TEXT["creat_item_15"], f"\033[43m{TEXT['creat_item_15']}\033[0m")
            name.replace(TEXT["creat_item_16"], f"\033[32m{TEXT['creat_item_16']}\033[0m")
            name.replace(TEXT["creat_item_17"], f"\033[36m{TEXT['creat_item_17']}\033[0m")
            name.replace(TEXT["creat_item_18"], f"\033[31m{TEXT['creat_item_18']}\033[0m")
            return name

    def __format__(self, format_space):
        return self.__str__()
