import os
import json
from WordParser.config import kwrd
# from Complier.SentenceParser.expression import Symbol
# 字典 - 识别 任意一个 token 是什么类型的 
class DICT:
    def __init__(self):
        self.kwrd = kwrd
    def get(self, ch):
        if not ch:
            return "None"
        if ch in self.kwrd:
            return ch
        elif ch[0].isdigit():
            return "NUM"
        else:
            return "id"

dic = DICT()

# 将字母或者数字转化为 letter or digit
def type(ch):
    if ch.isdigit():
        return 'digit'
    elif ch.isalpha():
        return 'letter'
    else:
        return ch


# 位置类， 记录每个 Token 的  postion
class POS:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __str__(self):
        return "<postion object : {}, {}>".format(self.row, self.col)
    def __repr__(self):
        return self.__str__()


# 将打开文件处理成方便处理的形式
class EXFILE:
    def __init__(self, filename):
        self.content = []
        with open(filename, "r") as f:
            for line in f.readlines():
                line = list(line.replace("\n", '').replace("\t", '    '))
                if line:
                    line.append(' ')
                    self.content.append(line)
        self.content[-1].append(' ')
        self.content[-1].append('$')
        self.pos = POS(0, 0)

    # 状态机进入下一个状态
    def next(self):
        line = self.content[self.pos.row]
        if self.pos.col != len(line) - 1:
            self.pos.col += 1
        else:
            if self.pos.row != len(self.content) - 1:
                self.pos.col = 0
                self.pos.row += 1

    # def back(self):
    #     if self.pos.col != 0:
    #         self.pos.col -= 1
    #     else:
    #         if self.pos.row != 0:
    #             self.pos.row -= 1
    #             self.pos.col = len(self.content[self.pos.row]) - 1

    # 获取当前位置的 ch
    def get(self):
        return self.content[self.pos.row][self.pos.col]

    # 判断是否到达文件末尾
    def EOF(self):
        return self.get() == '$'

    # 序列化文件
    def __str__(self):
        return str(self.content)

# 存储词法分析结果的数据结构
class resultList:
    def __init__(self, path):
        self.data = []
        self.path = path

    # 将结果序列化到文件
    def save(self):
        filename = self.path.replace('.c', '.json').replace('source/', 'target/')
        with open(filename, "w+", encoding = "UTF-8") as f:
            for item in self.data:
                line = '{} {} {} {}\n'.format(item[0].row, item[0].col, item[1], item[2])
                f.write(line)

    # 添加一项 Item
    def append(self, pos, ma):
        item= [pos, dic.get(ma.path) if not ma.wrong() else "wrong", ma.path]
        self.data.append(item)
    def check(self):
        tmp = []
        for item in self.data:
            if item[1] != 'wrong':
                tmp.append(item) 
        return tmp
    # 序列化结果输出
    def __str__(self):
        tmp = ''
        for item in self.data:
            line = '[{}\t{}\t \'{}\' ]'.format(item[0].__str__(), item[1], item[2])
            tmp += line + '\n'
        return tmp


if __name__ == "__main__":
    f = EXFILE("demo.c")
    print(f)