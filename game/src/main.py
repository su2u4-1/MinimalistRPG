import json
from classlib import *


def material_shop():
    player.location = "material_shop"
    with open(data_dir + "\\" + default_language + "\\text.json", "r") as f:
        product_list = json.load(f)["material_shop"]
    print("歡迎來到素材商店")
    player.bag.renew()
    while True:
        option = input("1.買東西\t2.賣東西\t3.離開:")
        match option:
            case "1":
                for i in range(len(product_list)):
                    print(f"{i+1}.\t品名:{product_list[i][0]}\t價錢:{product_list[i][1]}")
                while True:
                    try:
                        choose = input("請輸入商品編號(輸入-1取消):")
                        if choose == "-1":
                            break
                        choose = product_list[int(choose) - 1]
                        quantity = int(input("買的數量:"))
                        if quantity < 1:
                            print("數量過少")
                            continue
                    except ValueError:
                        print("輸入非數字")
                        continue
                    except IndexError:
                        print("編號不存在")
                        continue
                    if player.money >= choose[1] * quantity:
                        player.money -= choose[1] * quantity
                        player.bag[choose[0]] += quantity
                        break
                    else:
                        print("錢不夠喔")
            case "2":
                pass
            case "3":
                break
            case _:
                print(TEXT["input_error"])


def prop_shop():
    pass


def blacksmith_shop():
    pass


def bank():
    pass


def gym():
    pass


def task_wall():
    pass


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
            option = input(f"1.{TEXT['go_out']}\t2.{TEXT['material_shop']}\t3.{TEXT['prop_shop']}\t4.{TEXT['blacksmith_shop']}\t5.{TEXT['bank']}\t6.{TEXT['gym']}\t7.{TEXT['task_wall']}\t8.{TEXT['setting']}:")
            match option:
                case "1":
                    player.location = "lv"
                case "2":
                    material_shop()
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
            option = input(f"1.{TEXT['go_home']}\t2.{TEXT['explore']}\t3.{TEXT['next_lv']}\t4.{TEXT['setting']}:")
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
