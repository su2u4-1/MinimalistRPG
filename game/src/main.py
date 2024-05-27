import json
from classlib import *


def locationDecorator(fn):
    def f(*args, **kwargs):
        location = player.location
        result = fn(*args, **kwargs)
        player.location = location
        return result

    return f


@locationDecorator
def material_shop(floor):
    f = True
    while f:
        if 1 <= floor <= 3:
            print(TEXT[f"material_shop_{floor-1}"])
            player.location = f"material_shop_f{floor}"
        else:
            print(f"")
            if floor > 3:
                floor = 3
            elif floor < 1:
                floor = 1
            continue
        with open(data_dir + "\\" + default_language + "\\product_list.json", "r") as f:
            product_list = json.load(f)[f"material_shop_f{floor}"]
        player.bag.renew()
        while f:
            option = input(f"[1.{TEXT['material_shop_4']}][2.{TEXT['material_shop_5']}][3.{TEXT['material_shop_6']}][4.{TEXT['material_shop_7']}][5.{TEXT['material_shop_8']}]:")
            match option:
                case "1":
                    print(TEXT["material_shop_9"])
                    for i in range(len(product_list)):
                        print(f"[{str(i+1)+'.':<4}][{product_list[i][0]}][{product_list[i][1]:<5}$]")
                    while True:
                        choose = input(TEXT["material_shop_10"])
                        if choose == "-1":
                            break
                        try:
                            choose = int(choose)
                        except ValueError:
                            print(TEXT["material_shop_11"])
                            continue
                        if choose < 1 or choose > len(product_list):
                            print(TEXT["material_shop_12"])
                            continue
                        choose = product_list[choose - 1]
                        quantity = input(TEXT["material_shop_13"])
                        try:
                            quantity = int(quantity)
                        except TypeError:
                            print(TEXT["material_shop_11"])
                            continue
                        if quantity < 1:
                            print(TEXT["material_shop_14"])
                            continue
                        if player.money >= choose[1] * quantity:
                            player.money -= choose[1] * quantity
                            player.bag[choose[0]] = [player.bag[choose[0]][0] + quantity, choose[1] // 2]
                            print(TEXT["material_shop_15"].format(quantity, choose[0], choose[1] * quantity, player.money))
                            break
                        else:
                            print(TEXT["material_shop_16"].format(player.money))
                case "2":
                    player.show_bag()
                    while True:
                        choose = input(TEXT["material_shop_10"])
                        if choose == "-1":
                            break
                        try:
                            choose = int(choose)
                        except ValueError:
                            print(TEXT["material_shop_11"])
                            continue
                        if choose < 1 or choose > len(player.bag):
                            print(TEXT["material_shop_12"])
                            continue
                        choose = list(player.bag)[choose - 1]
                        quantity = input(TEXT["material_shop_17"])
                        try:
                            quantity = int(quantity)
                        except TypeError:
                            print(TEXT["material_shop_11"])
                            continue
                        if quantity < 1:
                            print(TEXT["material_shop_14"])
                            continue
                        if quantity > player.bag[choose][0]:
                            print(TEXT["material_shop_18"])
                            continue
                        m = player.bag[choose][1] * quantity
                        player.money += m
                        player.bag[choose][0] -= quantity
                        player.bag.renew()
                        print(TEXT["material_shop_19"].format(quantity, choose, m, player.money))
                        break
                case "3":
                    floor += 1
                    break
                case "4":
                    floor -= 1
                    break
                case "5":
                    f = False
                case _:
                    print(TEXT["input_error"])


@locationDecorator
def prop_shop():
    pass


@locationDecorator
def blacksmith_shop():
    pass


@locationDecorator
def bank():
    f = True
    while f:
        player.location = "bank"
        print("歡迎來到銀行")
        option = input("[1.存錢][2.取錢][3.借錢][4.還錢][5.查看資訊][6.離開]:")
        if option == "1":
            while True:
                amount = input("要存多少:")
                try:
                    amount = int(amount)
                except TypeError:
                    print("輸入非數字")
                    continue
                if amount < 1:
                    print("金額過小")
                    continue
                if amount > player.money:
                    print(f"金額過多，你只有{player.money}塊")
                    continue
                balance = player.account.deposit(amount)
                print("你存了{amount}塊，你還剩{player.money}塊，帳戶餘額為{balance}")
                break
        elif option == "2":
            while True:
                amount = input("要取多少:")
                try:
                    amount = int(amount)
                except TypeError:
                    print("輸入非數字")
                    continue
                if amount < 1:
                    print("金額過小")
                    continue
                balance = player.account.withdraw(amount)
                if balance == -1:
                    print(f"金額過多，你帳戶裡只有{player.account.money}塊")
                    continue
                print("你取了{amount}塊，你手邊有{player.money}塊，帳戶餘額為{balance}")
                break
        elif option == "3":
            pass
        elif option == "4":
            pass
        elif option == "5":
            pass
        elif option == "6":
            f = False
        else:
            print(TEXT['input_error'])


@locationDecorator
def gym():
    pass


def task_wall():
    pass


@locationDecorator
def setting():
    pass


def explore():
    pass


def next_lv(lv: int):
    pass


def main():
    global player
    print(TEXT["hello_message"])
    player = playerManager.create_role()
    if player is None:
        exit()
    print(TEXT["player_name"], player.name)
    while True:
        if player.location == "lv":
            print(TEXT["current_location"], TEXT[player.location] + str(player.stage_lv))
        else:
            print(TEXT["current_location"], TEXT[player.location])
        if player.location == "home":
            option = input(f"[1.{TEXT['go_out']}][2.{TEXT['material_shop']}][3.{TEXT['prop_shop']}][4.{TEXT['blacksmith_shop']}][5.{TEXT['bank']}][6.{TEXT['gym']}][7.{TEXT['task_wall']}][8.{TEXT['setting']}]:")
            match option:
                case "1":
                    player.location = "lv"
                case "2":
                    material_shop(1)
                case "3":
                    prop_shop()
                case "4":
                    blacksmith_shop()
                case "5":
                    bank()
                case "6":
                    gym()
                case "7":
                    task_wall()
                case "8":
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
    default_language = "zh-tw"
    playerManager = PlayerManager(data_dir, save_dir, default_language)
    TEXT = playerManager.TEXT
    main()
