import os, json


class Player:
    def __init__(self, name: str = "player"):
        self.name = name
        self.location = "home"
        self.stage_lv = 0  # 關卡等級
        self.lv = 0  # 人物等級
        self.language = "zh-tw"
        self.money = 100
        self.bag = my_dict(dict(), default=[0, 0])
        self.account = BankAccount(self.name)

    def update(self, data: dict):
        for k, v in data.items():
            if k == "bag":
                self.bag = my_dict(v, default=[0, 0])
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

    def show_bag(self):
        if len(self.bag) != 0:
            l0 = len(str(len(self.bag)))
            l1 = max(len(k) for k in self.bag)
            l2 = max(len(str(v[0])) for v in self.bag.values())
            l3 = max(len(str(v[1])) for v in self.bag.values())
            i = 1
            print(f"{TEXT['show_bag_0']:^{l0+2}}{TEXT['show_bag_1']:^{l1+2}}{TEXT['show_bag_2']:^{l2+2}}{TEXT['show_bag_3']:^{l3+2}}")
            for k, v in self.bag.items():
                print(f"[{str(i)+'.':<{l0+1}}][{k:<{l1}}][{v[0]:<{l2}}][{v[1]:<{l3}}]")
                i += 1
        else:
            print(f"{TEXT['show_bag_0']} {TEXT['show_bag_1']} {TEXT['show_bag_2']} {TEXT['show_bag_3']}")


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

    def renew(self):
        for k, v in list(self.items()):
            if v[0] <= 0:
                del self[k]


class PlayerManager:
    def __init__(self, data_dir, save_dir, default_language):
        self.data_dir = data_dir
        self.save_dir = save_dir
        self.default_language = default_language
        self.switch_language(default_language)

    def switch_language(self, language: str):
        global TEXT
        with open(self.data_dir + "\\" + language + "\\text.json", "r") as f:
            data = json.load(f)
        if language != self.default_language:
            with open(self.data_dir + "\\" + self.default_language + "\\text.json", "r") as f:
                TEXT = my_dict(data, json.load(f))
        else:
            TEXT = my_dict(data)
        self.TEXT = TEXT

    def create_role(self):
        def load_archive():
            while True:
                inp = input(TEXT["create_role_0"])
                if inp == "-1":
                    return
                path = self.save_dir + "\\" + inp + ".json"
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
            path = self.save_dir + f"\\{player.name}.json"
        while True:
            if os.path.isfile(path):
                inp = input(f"{TEXT['save_archive_0']}\t[1.{TEXT['save_archive_1']}][2.{TEXT['save_archive_2']}][3.{TEXT['save_archive_3']}]:")
                match inp:
                    case "1":
                        path = self.save_dir + "\\" + input(TEXT["save_archive_4"]) + ".json"
                        continue
                    case "2":
                        pass
                    case _:
                        return
            with open(path, "w+") as f:
                f.write(json.dumps(player.serialize()))
                return

class BankAccount:
    def __init__(self, account:str):
        self.money = 0
        self.name = account
        self.bag = my_dict(dict(), default=[0, 0])
        self.credit = 100

    def deposit(self, amount:int):
        self.money += amount
        return self.money

    def withdraw(self, amount:int):
        if self.money <= amount:
            self.money -= amount
            return self.money
        else:
            return -1
