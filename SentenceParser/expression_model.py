# Package production
# 由于之前做词法分析时没有用到产生式一步一步推
# 所以现在 符号类 和 产生式 类作为语法分析器最基础的模型
# TODO： 实现 Symbol 类
# 1. 保存文法符号
# 2. 提供文法符号类型的信息
# 3. 提供有好的 print 方法

# TODO： 实现产生式类
# 1. 产生式 和 项目具有相似的形式 和 操作
# 2. 设计实现 _Production 类用于提供两者共有的方法和成员
# 3. 设计实现 ItemProduction 类
# 4. 设计实现 Production 类
# 需要实现， 集合接口， 下标访问， 多种构造函数 以便从文件或者数据结构 中构造
# 需要实现 Production 和 ItemProduction 的转换
#  需要实现 python 的一些关键字操作 例如 in， for...
import copy
from SentenceParser.gramma_model import *

class Symbol:
    def __init__(self, name:str, val=None, pos = None):
        self.name  = name
        self.final = False if name in Nonfinal else True
        self.val = val
        # 该 symbol 在原文件中的位置（行， 列）
        self.pos = pos
    def __str__(self, ):
        return self.name
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)
    def __len__(self):
        return len(self.name)
    def __add__(self, other):
        if isinstance(str, other):
            return self.name + other
        elif isinstance(Symbol, other):
            return self.name + other.name
    def info(self):
        return '  '.join([str(self.name), str(self.final), str(self.val), self.pos.__str__()])
class _Expression(object):
    def __init__(self, TYPE:str, data:list):
        self.TYPE = TYPE
        self.data = data

class Expression(_Expression):
    def __init__(self, data:list):
        super().__init__("Normal", data)
    def __str__(self, ):
        return ' '.join(map(str,self.data))
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.data)
    def __eq__(self, other):
        return self.__str__() == other.__str__()
    def __getitem__(self, index):
        return self.data[index]
    # 为 expression 添加新的构造函数， 由于底层存储方式是List 所以这里直接写一个 
    @classmethod
    def bystr(cls, data:str):
        return cls(list(map(lambda x:Symbol(x), data.split("@"))))
    @classmethod
    def bydot(cls, dot):
        return cls(dot.merge())

    
# DotExpression 类有两部分组成所以一定需要一个 left 函数和 right 函数
class DotExpression(_Expression):
    # The expression List is a Symbol List
    def __init__(self, expression:list):
        super().__init__(
                "Dot",
                expression
            )
    def __str__(self, ):
        return ' '.join(map(str,self.data[0])) + ' · ' + ' '.join(map(str,self.data[1]))
    def __repr__(self):
        return self.__str__()
    def __len__(self):
        return len(self.data[0]) + len(self.data[1])
    def __getitem__(self, index):
        # 支持切片操作
        if isinstance(index, slice):
            if index.start > 0 or index.stop < 0:
                return self.data[1][index.start - 1:index.stop if not index.stop else index.stop - 1]
            else:
                return [Symbol('')]

        elif isinstance(index, int):
            if -len(self.data[0]) <= index <= len(self.data[1]):
                if index < 0:return self.data[0][index]
                elif index == 0:return Symbol('·')
                else:return self.data[1][index - 1]
            else:return Symbol('')
    
    # 该运算定义 为 dot 左边第一个往右移动， 或者右边第一个往左移动
    def __rshift__(self, other):
        assert type(other) == int
        print("这里暂时移不动")
    def __lshift__(self, other):
        assert type(other) == int
        tmp_data = copy.deepcopy(self.data)
        for _ in range(other):
            tmp_data[0].append(tmp_data[1].pop(0))
        return DotExpression(tmp_data)
    @classmethod
    def bystr(cls, expression:str):
        item = expression.split("·")
        return cls([
                    list(map(lambda x:Symbol(x), item[0].split("@"))) if item[0] else [], 
                    list(map(lambda x:Symbol(x), item[1].split("@"))) if item[1] else []
                ])
    @classmethod
    def bynormal(cls, normal, position):
        return cls([normal.data[0:position], normal.data[position:]])

    def merge(self):
        return self.data[0] + self.data[1]
    # 重新定义 [] 访问， 规定 0 为 dot 往左为负， 往右为正, 出错返回空
    
