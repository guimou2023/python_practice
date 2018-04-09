#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# AUTHOR:Howard hao
import re

def main():
    a = input('输入算式：')
    while '(' in a:
        print('a = ',a)
        b = re.search('\(([^()]+)\)',a).groups()[0]
        print('b = ',b)
        a = re.sub('\([^()]+\)',str(calculate(b)),a,1)
        print('替换后a = ',a)
    else:
        print('The result is',calculate(a))


#计算乘除加减(分步计算乘除)
def md(e):
    if '*' in e:
        E = re.split('\*', e,1)
        E1 = E[0].replace(' ','')
        E2 = E[1].replace(' ','')
        return float(E1)*float(E2)
    elif '/' in e:
        E = re.split('/', e,1)
        E1 = E[0].replace(' ', '')
        E2 = E[1].replace(' ', '')
        return float(E1)/float(E2)
    else:
        e = e.replace(' ', '').replace('++', '+').replace('+-', '-').replace('--','+')
        e = re.findall('[+-]?\d+\.?\d*', e)
        l = []
        for i in e:
            if '.' in i:
                l.append(float(i))
            else:
                l.append(int(i))
        else:
            return sum(l)

#截取一段计算传回md函数计算
def calculate(c):
    while '*' in c or '/' in c:
        print('c = ',c)
        d = re.search('\s*[+-]?\s*\d+\.?\d*\s*[*/]\s*[+-]?\s*\d+\.?\d*',c).group()
        print('d = ',d)
        # 替换
        c = re.sub('\s*[+-]?\s*\d+\.?\d*\s*[*/]\s*[+-]?\s*\d+\.?\d*','''+''' + str(md(d)),c,1)
        print('c = ',c)
    else:
        return md(c)
main()
