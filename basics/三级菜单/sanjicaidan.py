#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
place1 = {
    '北京':{
        '朝阳': {
            '小关':["对外经贸大学","彩虹科技"],
            '天通苑':["长庚医院","地下小吃城"],
            '天安门': ["故宫","毛主席纪念堂"],
        },
        '房山': {
            '篱笆房': ["奥特莱斯","菜市场"],
            '广阳城': ["双语幼儿园","温泉会议中心"],
            '苏庄': ["超级蜂巢","佳世苑"],
        }
    },
    '天津': {
        '滨海': {
            '新港': ["瑞湾大酒店","新港公园"],
            '东海路': ["国家超级计算中心","S11海滨高速"],
        },
        '宝坻': {
            '西台渠': ["台湾小火锅","点点快餐城"],
            '五里铺': ["多得福快餐","川北小吃"],
        }
    }
}
f = open('place','w',encoding='utf-8')
f.write('%s' %place1)
f.flush()
while True:
    for i in place1:
        print("\t",i)
    city = input("你想去哪个城市：")
    if city in place1:
        while True:
            for j in place1[city]:
                print("\t",j)
            region = input("你想去哪个区：")
            if region in place1[city]:
                while True:
                    for k in place1[city][region]:
                        print("\t",k)
                    p = input("你想去什么地方：")
                    if p in place1[city][region]:
                        print("这里有",place1[city][region][p],"祝你玩得愉快！")
                    elif p == 'q':
                        exit()
                    elif p == 'b':
                        break
                    elif p == 'q':
                        exit()
                    else:
                        print("这个地方不存在。","键入 b 返回上一层。","键入 q 退出。")
            elif region == 'b':
                break
            elif region == 'q':
                exit()
            else:
                print("这个区不存在。","键入 b 返回上一层。" )
    elif city == 'q':
        exit()
    else:
        print("输入错误，请重新选择。","键入 q 退出。")