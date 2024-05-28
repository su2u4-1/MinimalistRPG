a = ["初級", "中級", "高級"]
b = "乾坤震巽坎離艮兌"
c = "金木水火土"
d = ["粉末", "結晶", "寶石"]
out = []
n = 0
for i in a:
    for j in b:
        for k in c:
            for l in d:
                out.append(f'    "material_{n}": "{i+j+k+l}",')
                n += 1
    out.append("")
with open("素材.txt", "w+") as f:
    f.write("\n".join(out))
