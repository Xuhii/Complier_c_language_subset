''' 
因为后续需要实现类似 Lex 的自动构建状态转换图的方法
所以采用状态转换矩阵的方法实现状态机
状态矩阵定义[
    {'a':1, 'b':2, 'c':3},
    {'a':2, 'b':1, 'c':1},
    {'a':1, 'b':2, 'c':2},
]
'''
from WordParser.StateMachine import StateMa
from WordParser.config import matrix, final
from WordParser import tools
import os
import json
import copy

# 测试
def w_parser(filename):
    ma = StateMa(matrix, final)
    source = tools.EXFILE(filename)
    
    result = tools.resultList(filename)
    while not source.EOF():
        while ma.move(source.get()):
            source.next()
        # if not source.EOF():source.back()
        result.append(copy.deepcopy(source.pos), ma)
        # print(source.pos)
        ma.initialize()
    result.save()
    return result


# app模块
import typer

def main(filename: str):
    # filename = "source/light.c"
    light = filetest(filename)
    typer.echo(light.__str__())
    


if __name__ == "__main__":
    typer.run(main)