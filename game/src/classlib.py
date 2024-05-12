import os, json


class Player:
    def __init__(self, name: str = "player"):
        self.name = name
        self.location = "home"
        self.stage_lv = 0  # 關卡等級
        self.lv = 0  # 人物等級
        self.language = "zh-tw"
        self.money = 100
        self.bag = my_dict(dict(), default=0)

    def update(self, data: dict):
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
    def __init__(self, *dicts: dict, default=None):
        super().__init__()
        self.dicts = dicts
        self.default = default

    def __getitem__(self, key: str):
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


class PlayerManager:
    def __init__(self, data_dir, save_dir, default_language):
        self.data_dir = data_dir
        self.save_dir = save_dir
        self.default_language = default_language
        self.switch_language(default_language)

    def switch_language(self, language: str):
        with open(self.data_dir + "\\" + language + "\\text.json", "r") as f:
            data = json.load(f)
        if language != self.default_language:
            with open(self.data_dir + "\\" + self.default_language + "\\text.json", "r") as f:
                self.TEXT = my_dict(data, json.load(f))
        else:
            self.TEXT = my_dict(data)

    def create_role(self):
        def load_archive():
            while True:
                inp = input(self.TEXT["create_role_0"])
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
                    print(self.TEXT["create_role_1"])

        while True:
            option = input(f"1.{self.TEXT['create_role_2']}\t2.{self.TEXT['create_role_3']}\t3.{self.TEXT['create_role_4']}:")
            if option == "1":
                player = load_archive()
                if player is None:
                    continue
            elif option == "2":
                return Player(input(self.TEXT["create_role_5"]))
            elif option == "3":
                return
            else:
                print(self.TEXT["input_error"])

    def save_archive(self, player: Player, path=None):
        if path is None:
            path = self.save_dir + f"\\{player.name}.json"
        while True:
            if os.path.isfile(path):
                inp = input(f"{self.TEXT['save_archive_0']}\t1.{self.TEXT['save_archive_1']}\t2.{self.TEXT['save_archive_2']}\t3.{self.TEXT['save_archive_3']}:")
                match inp:
                    case "1":
                        path = self.save_dir + "\\" + input(self.TEXT["save_archive_4"]) + ".json"
                        continue
                    case "2":
                        pass
                    case _:
                        return
            with open(path, "w+") as f:
                f.write(json.dumps(player.serialize()))
                return
