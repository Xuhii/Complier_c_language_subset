# 集合类， 在文法分析中 涉及许多集合操作
# 需要封装便于操作的方法， 和 python 支持的魔法方法
# TODO：
# 1. 多构造函数
# 2. 拓展集合方法
# 3. 迭代方法
# 4. 统计文法符号
# 5. 由于 FIRST 集合 和 FOLLOW 集合仅与文法无关， 而在该项目中 一个文法G 也是以一个集合G的形式表现， 所以还需实现：
    # 1. build_first()
    # 2. build_second()

from SentenceParser.gramma_model import *
def size(X:dict):
    s = 0
    for t in X.values():
        s += len(t)
    return s
from SentenceParser.production_model import *
class ProductionSet:
    def __init__(self, L = []):
        self.set = set()
        for production in L:
            self.set.add(production)
        self.FIRST = dict([(smb, set()) for smb in self.symbol()])
        self.FOLLOW = dict([(smb, set()) for smb in self.symbol()])

    def __str__(self):
        return "\n" + self.set.__str__().replace('],', '],\n')
    def __repr__(self):
        return self.__str__()
    def __contains__(self, item):
        return item in self.set
    # 由于在构建项目集簇的时候需要将将集合放入集合 ？？？？？所以集合需要实现对比的方法？？？？怎么搞
    # 添加 __eq__ 方法
    def __eq__(self, other):
        return self.set == other.set
    def __nonzero__(self):
        return True if self.set else False
    def __len__(self):
        return len(self.set)
    
    @classmethod
    def byfile(cls, filename:str):
        tmp = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                if line[0] != '#':
                    tmp.append(ProductionFactory.create(line))
            f.close()
        return cls(tmp)
    @classmethod
    def bylist(cls, l:list):
        return cls(map(lambda x:ProductionFactory.create(x), l))
    @classmethod
    def by_ex_list(cls, g:list):
        tmp = []
        global Nonfinal
        for line in g:
            left, right = line.replace(' ', '').split('->')
            Nonfinal.append(left)
            for e in right.split('|'):
                tmp.append(left + '->' + e)
        return cls(map(lambda x:ProductionFactory.create(x), tmp))

    def add(self, item):
        self.set.add(item)
    def extend(self):
        self.set.add(ProductionFactory.create("S_ -> S"))
        self.FOLLOW[Symbol('S_')] = set()
        self.FIRST[Symbol('S_')] = set()

    # 之后将 iter 改为 __iter__ 的写法 更优雅
    def iter(self):
        for k in self.set:
            yield k
    def symbol(self)->set:
        t = set()
        for item in self.set:
            t.add(item.left)
            # 这里需要一个 迭代器返回 item.right的所有元素
            for smb in item.iter():
                if smb:t.add(smb)
        return t            
    # TODO: 
    def build_first(self):
        # 将所有终结符 添加到 它自己 的FIRST 集合
        for X in self.symbol():
            if X.final:self.FIRST[X].add(X)
        self.FIRST[Symbol('$')] = set([Symbol('$')])


        # 重复直到集合不再变大 
        length = -1
        while size(self.FIRST) != length:
            length = size(self.FIRST)
            # 便利 文法 G 的每一个产生式
            for production in self.set:
                X = production.left
                # 对于 A->a..., A非终结， a终结， 将a添加到 FIRST(A)
                if not X.final and production.right[0].final:
                    self.FIRST[X].add(production.right[0])
                # A—>e， 那么将 e 添加到 FIRST(A)
                if production.right == Expression.bystr("e_"):
                    self.FIRST[X].add(production.right[0])
                # A->Bas 那么把 FIRST(B) - {e} 添加到 FIRST(A) 中
                if not production.right[0].final:
                    self.FIRST[X] |= (self.FIRST[production.right[0]] - set([Symbol("e_")]))

                # A->C1 C2 C3 C4.....这需要考虑把第一个非 e 的 C_i 前边的所有可能约掉的情况
                Nullable = True
                for i in range(len(production.right)):
                    self.FIRST[X]  |= (self.FIRST[production.right[i]] - set([Symbol("e_")]))
                    if Symbol('e_') not in self.FIRST[production.right[i]]:
                        Nullable = False
                        break
                if Nullable:self.FIRST[X] |= set([Symbol('e_')])
    def str_first(self,s_list:list):
        # 对于文法G的任何符号串α = X1 X2 … Xn 构造集合FIRST(α)：
        # 1.置FIRST(α) = FIRST(X1) \ {ε} .即把X1的FIRST集合元素去掉ε后给α的FIRST集合来作为其第一批元素.
        # 2.若对于任何 1 <= j <= i-1 ,ε∈ FIRST(Xj)，则把FIRST(Xi) \ {ε}加入到FIRST(α)中.

        # 特别的：
        # 若所有的FIRST(Xj)均含有ε，其中1 <= j <= n，那么把ε也加入到FIRST(α)中.
        # 显然：若α = ε，则FIRST(α) = {ε}.
        if isinstance(s_list, Symbol):
            return self.FIRST[s_list]
        else:
            s = set()
            Nullable = True
            for i in range(0, len(s_list)):
                s  |= (self.FIRST[s_list[i]] - set([Symbol("e_")]))
                if Symbol('e_') not in self.FIRST[s_list[i]]:
                    Nullable = False
                    break
            if Nullable:s |= set([Symbol('e_')])
            return s

    def build_follow(self):
        # 设置结束条件
        self.FOLLOW[Symbol('S')].add(Symbol('$'))

        # 保证重复直到集合不再增大
        length = -1
        while size(self.FOLLOW) != length:
            length = size(self.FOLLOW)
            for production in self.set:
                A = production.left
                X = production.right
                # 右部非空， A-> ...Bd, B非终结， 那么 需要将 FIRST(d) - {e} 加入 FOLLOW(B)
                for i in range(0, len(X)-1):
                    if not X[i].final:
                        self.FOLLOW[X[i]] |= (self.str_first(X[i+1:]) - set([Symbol('e_')]))

                if not X[-1].final:
                    self.FOLLOW[X[-1]] |= self.FOLLOW[A]

                for i in range(0, len(X)-1):
                    if not X[i].final and Symbol('e_') in self.str_first(X[i+1:]):
                        self.FOLLOW[X[i]] |= self.FOLLOW[A]
