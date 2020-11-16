# package Production Model
from SentenceParser.expression_model import *

class _Production(object):
    count = 0
    def __init__(self, first:Symbol, second):
        self.left = first
        self.right = second
        _Production.count += 1
        self.id = self.count - 1     
    def __str__(self, ):
        return '[' + self.left.__str__() + ' -> ' + self.right.__str__() + "]"
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.__str__())
    def __eq__(self, other):
        return self.__str__() == other.__str__()
    # 产生式支持下标访问， dot 和 normal 的区别只是在于 expression 的实现不同
    def __getitem__(self, index):
        return self.right[index]
    
class ItemProduction(_Production):
    def __init__(self, left:Symbol, right:DotExpression):
        super().__init__(left, right)
    def __rshift__(self, other):
        assert type(other) == int
        print("这里暂时移不动")
    def __lshift__(self, other):
        assert type(other) == int
        return ItemProduction(self.left, self.right << other)
    @classmethod
    def bystr(cls, expression):
        item = expression.replace(' ', '').replace('\n', '').split("->")
        assert item[0] + item[1] != ''
        return cls(Symbol(item[0]), DotExpression.bystr(item[1]))
    def to_normal(self, ):
        assert self.right.TYPE == 'Dot'
        return Production(self.left, Expression.bydot(self.right))
    def iter(self):
        for item in self.right.merge():
            yield item

class Production(_Production):
    def __init__(self, left:Symbol, right:Expression):
        super().__init__(left, right)
    @classmethod
    def bystr(cls, expression):
        item = expression.replace(' ', '').replace('\n', '').split("->")
        assert item[0] + item[1] != ''
        return cls(Symbol(item[0]), Expression.bystr(item[1]))
    def to_item(self, position):
        assert self.right.TYPE == 'Normal'
        assert 0 <= position <= len(self.right)
        return ItemProduction(self.left, DotExpression.bynormal(self.right, position))
    def iter(self):
        for item in self.right.data:
            yield item

# 工厂方法
class ProductionFactory:
    @staticmethod
    def create(item:str):
        if '·' in item:
            return ItemProduction.bystr(item)
        else:
            return Production.bystr(item)

# 大多数语言而言 k 取 1 即可, 所以待约串 为一个Symbol, 这里还是用列表存储
# 由于拓展了 Item 的定义， 那么， 活前缀的有效性也是 拓展的 定义 4.13
class ExItemProduction(ItemProduction):
    def __init__(self, left, right, forward:Symbol):
        super().__init__(left, right)
        self.forward = forward
    # 序列化函数可以不变, 就是不展示 forward 列表
    def __str__(self, ):
        return '[' + self.left.__str__() + ' -> ' + self.right.__str__() + "," + self.forward.name + "]"
    @classmethod
    def byitem(cls, item, sbm):
        return cls(item.left, item.right, sbm)
    def __lshift__(self, other):
        assert type(other) == int
        return ExItemProduction(self.left, self.right << other, self.forward)