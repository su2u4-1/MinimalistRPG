import json, zlib


def naming():
    a = ["初級", "中級", "高級"]
    b = [
        ["乾", "戰甲", "戰靴", "劍"],
        ["坤", "騎甲", "騎靴", "槍"],
        ["震", "布甲", "布靴", "弓"],
        ["巽", "皮甲", "皮靴", "匕"],
        ["坎", "聖袍", "聖靴", "經"],
        ["離", "法袍", "法靴", "杖"],
        ["艮", "重甲", "重靴", "盾"],
        ["兌", "巫袍", "巫靴", "符"],
    ]
    c = "金木水火土"
    out = []
    n = 0
    for i in a:
        for j in b:
            for k in c:
                for l in range(1, 4):
                    out.append(
                        '    "equipment_'
                        + str(n)
                        + '": {"type": "material", "id": "equipment_'
                        + str(n)
                        + '", "name": "'
                        + str(i + j[0] + k + j[l])
                        + '", "price": 10000, "decoration": 2},'
                    )
                    n += 1
    with open("裝備.txt", "w+") as f:
        f.write("\n".join(out))


def price():
    # 設定基礎價格、等級係數和類型係數
    base_price = 10

    # 定義等級係數
    level_coefficients = {"初級": 1, "中級": 10, "高級": 100}

    # 定義形態係數
    type_coefficients_1 = {"粉末": 1, "結晶": 5, "寶石": 10}

    type_coefficients_0 = {
        "戰甲": 9,
        "戰靴": 4,
        "劍": 8,
        "騎甲": 10,
        "騎靴": 5,
        "槍": 7,
        "布甲": 3,
        "布靴": 2,
        "弓": 6,
        "皮甲": 4,
        "皮靴": 3,
        "匕": 1,
        "聖袍": 8,
        "聖靴": 4,
        "經": 7,
        "法袍": 9,
        "法靴": 5,
        "杖": 6,
        "重甲": 10,
        "重靴": 5,
        "盾": 8,
        "巫袍": 7,
        "巫靴": 3,
        "符": 2,
    }

    # 讀取 JSON 檔案
    with open("game\data\zh-tw\item_list.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    def nn(n):
        return ((zlib.crc32(n.encode()) - 13887577) / 2139491734 + 9) / 10

    # 更新每個裝備的價格
    for item in data.values():
        if item["type"] == "equipment":
            # 從名稱中提取等級和類型
            name = item["name"]
            for level in level_coefficients.keys():
                if level in name:
                    level_coefficient = level_coefficients[level]
                    break
            for type_ in type_coefficients_0.keys():
                if type_ in name:
                    type_coefficient = type_coefficients_0[type_]
                    break
            # 計算價格
            price = base_price * level_coefficient * type_coefficient * nn(name)
            item["price"] = int(price)
        if item["type"] == "material":
            # 從名稱中提取等級和類型
            name = item["name"]
            for level in level_coefficients.keys():
                if level in name:
                    level_coefficient = level_coefficients[level]
                    break
            for type_ in type_coefficients_1.keys():
                if type_ in name:
                    type_coefficient = type_coefficients_1[type_]
                    break
            # 計算價格
            price = base_price * level_coefficient * type_coefficient * nn(name)
            item["price"] = int(price)

    # 將更新後的資料寫回到 JSON 檔案
    with open("updated_item_list.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
