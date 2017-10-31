city_dic={
    '北京':{
        "昌平":{
            "沙河":["oldboy","test"],
            "天通苑":["链家地产","我爱我家"]
        },
        "朝阳":{
            "望京":["奔驰","陌陌"],
            "国贸":{"CICC","HP"},
            "东直门":{"Advent","飞信"},
        },
        "海淀":{},
    },
    '山东':{
        "德州":{},
        "青岛":{},
        "济南":{}
    },
    '广东':{
        "东莞":{'女子会所'},
        "常熟":{},
        "佛山":{},
    },
}
# while True:
for i in city_dic:
    print('\t',i)
city = input('哪个城市：')
for g in city_dic[city]:
    print(g)
regin = input('区：')
for j in city_dic[city][regin]:
    print(j)
place = input('地点：')
for k in city_dic[city][regin][place]:
    print(k)
