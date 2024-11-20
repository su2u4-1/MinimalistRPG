import wcwidth
from classlib import *
from random import random
from typing import Literal


@locationDecorator
def shop(name: str, top_floor) -> None:
    def pad(s: Item | str, width, align: Literal[">", "<", "^"] = ">") -> str:
        if isinstance(s, Item):
            padding = width - wcwidth.wcswidth(s.name)
            s = s.__str__()
        else:
            padding = width - wcwidth.wcswidth(s)
        if align == ">":
            return " " * padding + s
        elif align == "<":
            return s + " " * padding
        elif align == "^":
            left_padding = padding // 2
            right_padding = padding - left_padding
            return " " * left_padding + s + " " * right_padding
        else:
            raise ValueError("Invalid alignment")

    f = True
    floor = 1
    while f:
        if 1 <= floor <= top_floor:
            print(TEXT[f"{name}_shop_{floor-1}"])
            player.location = f"{name}_shop_f{floor}"
        else:
            print(TEXT["shop_0"].format(floor))
            if floor > top_floor:
                floor = top_floor
            elif floor < 1:
                floor = 1
            continue
        with open(data_dir + "\\product_list.json5", "r") as f:
            product_list: list[Item] = list(map(Item, json5.load(f)[f"{name}_shop_f{floor}"]))
        player.bag.renew()
        while f:
            option = input(f"[1.{TEXT[f'shop_1']}][2.{TEXT[f'shop_2']}][3.{TEXT[f'shop_3']}][4.{TEXT[f'shop_4']}][5.{TEXT[f'shop_5']}]:")
            match option:
                case "1":
                    print(TEXT["shop_6"])
                    l1 = len(str(len(product_list))) + 1
                    l2 = max(wcwidth.wcswidth(v.name) for v in product_list)
                    l3 = max(len(str(v.price)) for v in product_list)
                    for i in range(len(product_list)):
                        print(f"[{str(i+1)+'.':<{l1}}][{pad(product_list[i], l2, '<')}][{product_list[i].price:>{l3}}$]")
                    while True:
                        choose = input(TEXT["shop_7"])
                        if choose == "-1":
                            break
                        try:
                            choose = int(choose)
                        except ValueError:
                            print(TEXT["shop_8"])
                            continue
                        if choose < 1 or choose > len(product_list):
                            print(TEXT["shop_9"])
                            continue
                        choose = product_list[choose - 1]
                        quantity = input(TEXT["shop_10"])
                        try:
                            quantity = int(quantity)
                        except TypeError:
                            print(TEXT["shop_8"])
                            continue
                        if quantity < 1:
                            print(TEXT["shop_11"])
                            continue
                        if player.money >= choose.price * quantity:
                            player.money -= choose.price * quantity
                            player.bag[choose] += quantity
                            print(TEXT["shop_12"].format(quantity, choose, choose.price * quantity, player.money))
                            break
                        else:
                            print(TEXT["shop_13"].format(player.money))
                case "2":
                    choose, quantity = player.bag.getItem()
                    if choose == -1 and quantity == -1:
                        continue
                    m = choose.price // 2 * quantity
                    player.money += m
                    player.bag[choose] -= quantity
                    player.bag.renew()
                    print(TEXT["shop_14"].format(quantity, choose, m, player.money))
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
def blacksmith_shop() -> None:
    def forge_result(d: dict[Item, int] | my_dict[Item, int] | Bag[Item, int]) -> tuple[float, dict]:
        if len(d) == 0:
            return 0.0, my_dict()
        t = []
        for k, v in d.items():
            t.append(k.price * v * zlib.adler32(k.name.encode()))
        rate = sum(t) / len(t) / max(t) * player.modifier
        result = my_dict(dict(), default=0)
        return rate, result

    f = True
    while f:
        print("歡迎來到鐵匠鋪")
        player.location = "blacksmith_shop"
        option = input("[1.打造裝備][2.鍛造素材][3.強化裝備][4.回收裝備][5.鍛造說明][6.離開]:")
        if option == "1":
            material = Bag(dict(), default=0)
            while True:
                rate, result = forge_result(material)
                print(rate, player.modifier)
                print(f"目前成功率{round(rate*100, 2)}%, 可能結果/機率:{result}")
                op = input("[1.添加素材][2.開始鍛造][3.取消]:")
                if op == "1":
                    item, quantity = player.bag.getItem()
                    if item == -1 and quantity == -1:
                        player.bag.loadItem(material)
                        continue
                    player.bag[item] -= quantity
                    player.bag.renew()
                    material[item] += quantity
                    material.renew()
                elif op == "2":
                    rate, result = forge_result(material)
                    if random() < rate:
                        print("成功")
                        material = Bag(dict(), default=0)
                    else:
                        print("失敗")
                        material = Bag(dict(), default=0)
                elif op == "3":
                    player.bag.loadItem(material)
                    break
                else:
                    print(TEXT["input_error"])
        elif option == "2":
            pass
        elif option == "3":
            pass
        elif option == "4":
            pass
        elif option == "5":
            print(TEXT["forge_manual"])
        elif option == "6":
            f = False
        else:
            print(TEXT["input_error"])


@locationDecorator
def bank() -> None:
    f = True
    while f:
        player.location = "bank"
        print(TEXT["bank_0"])
        option = input(
            f"[1.{TEXT['bank_1']}][2.{TEXT['bank_2']}][3.{TEXT['bank_3']}][4.{TEXT['bank_4']}][5.{TEXT['bank_5']}][6.{TEXT['bank_6']}]:"
        )
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
def gym() -> None:
    pass


@locationDecorator
def task_wall() -> None:
    pass


@locationDecorator
def setting() -> None:
    pass


@locationDecorator
def explore() -> None:
    pass


@locationDecorator
def next_lv(lv: int):
    pass


def main() -> None:
    print(TEXT["player_name"], player.name)
    while True:
        if player.location == "lv":
            print(TEXT["current_location"], TEXT[player.location] + str(player.stage_lv))
        else:
            print(TEXT["current_location"], TEXT[player.location])
        if player.location == "home":
            option = input(
                f"[1.{TEXT['go_out']}][2.{TEXT['material_shop']}][3.{TEXT['equipment_shop']}][4.{TEXT['prop_shop']}][5.{TEXT['blacksmith_shop']}][6.{TEXT['bank']}][7.{TEXT['gym']}][8.{TEXT['task_wall']}][9.{TEXT['setting']}]:"
            )
            match option:
                case "1":
                    player.location = "lv"
                case "2":
                    shop("material", 3)
                case "3":
                    shop("equipment", 3)
                case "4":
                    shop("prop", 1)
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
    main()
