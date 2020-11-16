import sys

sys.path.append( "WordParser" );
from StateMachine import StateMa
from config import matrix, final
import tools as tools

import os
import json


# 内置函数
def _wordparser(filename):
    
    ma = StateMa(matrix, final)
    source = tools.EXFILE(filename)
    
    result = tools.resultList(filename)
    while not source.EOF():
        while ma.move(source.get()):
            source.next()
        # if not source.EOF():source.back()
        result.append(source.pos, ma)
        ma.initialize()
    result.save()
    return result

# app模块
import click


@click.group()
def cli():
    pass

# 1。 word parse command
@click.command()
@click.option('--filename', type=str)
@click.option('-r', type=bool, default = False)
def wordparser(filename, r):
    light = _wordparser(filename)
    if r:
        print(light)


# Add Command in cli Program
cli.add_command(wordparser)
if __name__ == "__main__":
    # 主程序启动
    cli()

