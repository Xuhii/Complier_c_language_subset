# Function Set 这个部分应该整合进入 [分析表类]
# 算法部分， 之后需要整合成类
# 输入 项目集合 I
# 输出 集合 J = closure(I)
# 构造 closure 集合的前提条件是 在某个文法 G 下

# 这里构建的是项目集簇， 但是分析表需要知道的信息是已知 状态I 和 符号 a 能够确定一个 go(I, a)
# 那么我们用一个 [{}]的结构来存储状态转移信息
# [
# {'A':4, "c":5, 'd':6},
# {symbol:index of C, , , },
# ]
# 所以 分析表可以构建如下

# action 类可以提供 操作针对三种不同的类
from SentenceParser.expression_model import *
from SentenceParser.production_model import *
from SentenceParser.production_set_model import *
from SentenceParser.gramma_model import *



class Action:
    # Action 3 种状态 S R ACC - >
    def __init__(self, action, content):
        assert action == 'R' or action == 'S' or action == 'ACC'
        self.ACTION = action
        # Content 可能是 Symbol 类型也可能是 Product 类型
        self.CONTENT = content
    def __str__(self):
        return "<{},{}>".format(self.ACTION, self.CONTENT)
    def __repr__(self):
        return self.__str__()
class AnalyzeTable:
    def __init__(self, G:ProductionSet):
        # 文法
        self.G = G
        self.G.extend()
        self.action = None
        self.goto = None

        global Nonfinal
        # 项目集簇
        self.C = list()
        # 状态转移
        self.T = [{}]
        self.exStartItemProduct = None
        
    def closure(self):
        pass
    def go(self, I:ProductionSet, X:Symbol):
        J = ProductionSet()
        for item in I.iter():
            if item[1] == X:
                J.add(item << 1)
        return self.closure(J)
    def build_regular_item_set(self):
        # C using to store the State Info
        # T using to store 
        # 计算 Folloew 集合时已经 拓展
        self.C.append(self.closure(ProductionSet([self.exStartItemProduct])))
        size = 0
        while len(self.C) - size:
            size = len(self.C)
            for s, itemSet in enumerate(self.C):
                for sbm in itemSet.symbol():
                    tmp = self.go(itemSet, sbm)
                    if len(tmp) > 0:
                        if tmp not in self.C:
                            self.C.append(tmp)
                            self.T.append({})
                            self.T[s][sbm] = len(self.C) - 1
                        else:
                            self.T[s][sbm] = self.C.index(tmp)
        # print(self.C)
    def __str__(self):
        action_str = "\n".join(map(lambda x:str(x), self.action))
        goto_str = "\n".join(map(lambda x:str(x), self.goto))
        return "Action Table:\n{0}\n\nGoto Table:\n{1}".format(action_str, goto_str)
    # closure 和 go 和 reItemSet 方法是所有分析表通用的方法， 应该放到父类中， 但是是否应该写为 classmethod 方便外部调用呢？ 应该没必要
    
class SLR(AnalyzeTable):
    def __init__(self, G:ProductionSet):
        super().__init__(G)
        self.exStartItemProduct = ItemProduction.bystr("S_->·S")
        self.build_regular_item_set()
        self.action = [{} for _ in range(len(self.C))]
        self.goto = [{} for _ in range(len(self.C))]
        self.G.build_first()
        self.G.build_follow()
        self.build_analyze_table()
        
    # To build a Fellow(A) iter and First Set
    # 用什么方式存储First集合和Follow集合， First集合可以由{set()}的方式存储，它与集合类有关它应该是属于产生式集合的一部分， 应该放到 ProductionSet中实现
    
    def closure(self, I:ProductionSet)->ProductionSet:
        J = copy.deepcopy(I)
        J_new = ProductionSet()
        while(len(J) != len(J_new)):
            J_new = copy.deepcopy(J)
            # 此处的双重循环可以改变 Set 集合的存储方式得到优化
            for item in J_new.iter():
                for product in self.G.iter():
                    # go through all item(A -> a·Bb) in J_new, find all B -> n in g  
                    if item[1] == product.left:
                        # Because of the need changing B -> n into B -> ·n,  the function design for Procuction is needed
                        # TODO 检查到错误， 这里之前没转换
                        # 不在 goto 中引入 e_ 用产生式 A->· 代替
                        if product.right == Expression([Symbol('e_')]):
                            J.add(ItemProduction(product.left, DotExpression.bystr('·')))
                        else:
                            J.add(product.to_item(0))
        return J

    def build_analyze_table(self):
        for i, I in enumerate(self.C):
            for item in I.iter():
                # if S_ -> S· in I_i  then make action[i, $] = ACC
                if item == ItemProduction.bystr("S_->S·"):
                    self.action[i][Symbol('$')] = Action("ACC", -1)
                 
                # if A->c·ab in I_i and go(I_i, a) = I_j and a is final , then action[i, a] = Sj
                
                elif item[1].final and item[1]:
                    # final 表示非空且是终结符号
                    self.action[i][item[1]] = Action(
                                                            "S", 
                                                            self.T[i][item[1]]
                    )
                # if A->b· in I_i, then all a in Fellow(A) make action[i, a] = R A->b (A != A_)
                elif not item[1]:
                    # 如果是空的那么需要构造 Fellow 集合
                    # 这里要求 A != S_ ， 因为文法 G 只有 S_ -> S， 所以前面的 if 处理了 ACC 情况
                    for a in self.G.FOLLOW[item.left]:
                        self.action[i][a] = Action(
                            "R",
                            item.to_normal()
                        )
            # if go[i, A] = j, A if not in final set, then make goto[i, A] = j
            for smb in self.T[i].keys():
                if not smb.final:self.goto[i][smb] = self.T[i][smb]

# LR(1)分析表是为了解决如下情况：
# Case：某项目集合 I_k 含有项目 A -> b, 状态 k 下输入符号 a in FOLLOW(A) 就可以使用 A -> b进行规约
# 在某些情况下， 符号串 cb 不能使用 A->b 归约， 因为可能没有一个有效的句型 有前缀 cba 
# 为了实现 LR 表需要拓展 ItemExpression 的定义添加 look_forward 项
TIMES = 1
class LR(AnalyzeTable):
    def __init__(self, G):
        super().__init__(G)
        self.exStartItemProduct = ExItemProduction.byitem(ItemProduction.bystr("S_->·S"), Symbol("$"))
        self.G.build_first()
        self.build_regular_item_set()
        self.action = [{} for _ in range(len(self.C))]
        self.goto = [{} for _ in range(len(self.C))]
        # self.G.build_first()
        # self.G.build_follow()
        self.build_analyze_table()
    def str_first(self,s_list:list):
        # 对于文法G的任何符号串α = X1 X2 … Xn 构造集合FIRST(α)：
        # 1.置FIRST(α) = FIRST(X1) \ {ε} .即把X1的FIRST集合元素去掉ε后给α的FIRST集合来作为其第一批元素.
        # 2.若对于任何 1 <= j <= i-1 ,ε∈ FIRST(Xj)，则把FIRST(Xi) \ {ε}加入到FIRST(α)中.

        # 特别的：
        # 若所有的FIRST(Xj)均含有ε，其中1 <= j <= n，那么把ε也加入到FIRST(α)中.
        # 显然：若α = ε，则FIRST(α) = {ε}.
        assert len(s_list) >= 2
        s = set()
        Nullable = True
        for i in range(0, len(s_list)):
            s  |= (self.G.FIRST[s_list[i]] - set([Symbol("e_")]))
            if Symbol('e_') not in self.G.FIRST[s_list[i]]:
                Nullable = False
                break
        if Nullable:s |= set([Symbol('e_')])
        return s
    def closure(self, I:ProductionSet)->ProductionSet:

        J = copy.deepcopy(I)
        J_new = ProductionSet()
        while(len(J) != len(J_new)):
            J_new = copy.deepcopy(J)
            # 此处的双重循环可以改变 Set 集合的存储方式得到优化
            for item in J_new.iter():
                for product in self.G.iter():
                    # go through all item(A -> a·Bb) in J_new, find all B -> n in g  
                    if item[1] == product.left:
                        # TODO FIRST(), 
                        str_first = list(self.str_first([*item[2:] , item.forward])) if item[2:] else self.G.FIRST[item.forward]
                        for b in str_first :
                            if b.final:
                                if product.right == Expression([Symbol('e_')]):
                                    J.add(ExItemProduction.byitem(ItemProduction(product.left, DotExpression.bystr('·')), b))
                                else:
                                    J.add(ExItemProduction.byitem(product.to_item(0), b))
        return J

    def build_analyze_table(self):
        
        for i, I in enumerate(self.C):
            for item in I.iter():

                if item == ExItemProduction.byitem(ItemProduction.bystr("S_->S·"), Symbol("$")):
                    self.action[i][Symbol('$')] = Action("ACC", -1)
                 
                # if A->c·ab in I_i and go(I_i, a) = I_j and a is final , then action[i, a] = Sj
                
                elif item[1].final and item[1]:
                    # final 表示非空且是终结符号
                    # if item[1] == Symbol('c'):print(i, item[1])
                    self.action[i][item[1]] = Action("S", self.T[i][item[1]])
                # if A->b· in I_i, then all a in Fellow(A) make action[i, a] = R A->b (A != A_)
                elif not item[1]:
                    # if item.forward == Symbol('c'):print(i, item.forward)
                    self.action[i][item.forward] = Action("R",item.to_normal())
            # if go[i, A] = j, A if not in final set, then make goto[i, A] = j
            for smb in self.T[i].keys():
                if not smb.final:self.goto[i][smb] = self.T[i][smb]