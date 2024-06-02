from classlib import *


@locationDecorator
def blacksmith_shop():
    pass


@locationDecorator
def bank():
    f = True
    while f:
        player.location = "bank"
        print(TEXT["bank_0"])
        option = input(f"[1.{TEXT['bank_1']}][2.{TEXT['bank_2']}][3.{TEXT['bank_3']}][4.{TEXT['bank_4']}][5.{TEXT['bank_5']}][6.{TEXT['bank_6']}]:")
        if option == "1":
            while True:
                amount = input(TEXT["bank_7"])
                try:
                    amount = int(amount)
                except TypeError:
                    print(TEXT["bank_8"])
                    continue
                if amount < 1:
                    print(TEXT["bank_9"])
                    continue
                if amount > player.money:
                    print(TEXT["bank_10"].format(player.money))
                    continue
                player.account.money += amount
                player.money -= amount
                print(TEXT["bank_11"].format(amount, player.money, player.account.money))
                break
        elif option == "2":
            while True:
                amount = input(TEXT["bank_12"])
                try:
                    amount = int(amount)
                except TypeError:
                    print(TEXT["bank_8"])
                    continue
                if amount < 1:
                    print(TEXT["bank_9"])
                    continue
                balance = player.account.withdraw(amount)
                if balance == -1:
                    print(TEXT["bank_13"].format(player.account.money))
                    continue
                print(TEXT["bank_14"].format(amount, player.money, balance))
                break
        elif option == "3":
            item, quantity = player.bag.getItem()
            if item == -1 and quantity == -1:
                continue
            player.bag[item] -= quantity
            player.bag.renew()
            player.account.bag[item] += quantity
            player.account.bag.renew()
        elif option == "4":
            item, quantity = player.account.bag.getItem()
            if item == -1 and quantity == -1:
                continue
            player.account.bag[item] -= quantity
            player.account.bag.renew()
            player.bag[item] += quantity
            player.bag.renew()
        elif option == "5":
            print(TEXT["bank_15"].format(player.money, player.account.money))
            print(TEXT["bank_16"])
            player.bag.show()
            print(TEXT["bank_17"])
            player.account.bag.show()
        elif option == "6":
            f = False
        else:
            print(TEXT["input_error"])


@locationDecorator
def gym():
    pass


@locationDecorator
def task_wall():
    pass


@locationDecorator
def setting():
    pass


@locationDecorator
def explore():
    pass


@locationDecorator
def next_lv(lv: int):
    pass


def main():
    print(TEXT["player_name"], player.name)
    while True:
        if player.location == "lv":
            print(TEXT["current_location"], TEXT[player.location] + str(player.stage_lv))
        else:
            print(TEXT["current_location"], TEXT[player.location])
        if player.location == "home":
            option = input(f"[1.{TEXT['go_out']}][2.{TEXT['material_shop']}][3.{TEXT['equipment_shop']}][4.{TEXT['prop_shop']}][5.{TEXT['blacksmith_shop']}][6.{TEXT['bank']}][7.{TEXT['gym']}][8.{TEXT['task_wall']}][9.{TEXT['setting']}]:")
            match option:
                case "1":
                    player.location = "lv"
                case "2":
                    material_shop.run()
                case "3":
                    equipment_shop.run()
                case "4":
                    prop_shop.run()
                case "5":
                    blacksmith_shop()
                case "6":
                    bank()
                case "7":
                    gym()
                case "8":
                    task_wall()
                case "9":
                    setting()
                case _:
                    print(TEXT["input_error"])
        else:
            option = input(f"[1.{TEXT['go_home']}][2.{TEXT['explore']}][3.{TEXT['next_level']}][4.{TEXT['setting']}]:")
            match option:
                case "1":
                    player.location = "home"
                case "2":
                    explore()
                case "3":
                    next_lv(player.stage_lv)
                case "4":
                    setting()
                case _:
                    print(TEXT["input_error"])


if __name__ == "__main__":
    data_dir = "\\".join(__file__.split("\\")[:-2] + ["data"])
    save_dir = "\\".join(__file__.split("\\")[:-2] + ["save"])
    TEXT, player = init(data_dir, save_dir)
    material_shop = Shop("material", 3)
    equipment_shop = Shop("equipment", 3)
    prop_shop = Shop("prop", 1)
    main()
