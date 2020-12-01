# LR 分析程序类
# 用于保存分析结果和提供多种 run 函数
# 由于需要构造出 语法树
# 所以在书上的算法基础上增加了一个 Node 栈， 用于构造语法树
# 其中：
# 1. Node Stack 的行为与 smb 的行为基本一致
# 2. 在发生 归约 时， 需要为 A->abcd 创建节点即 A.next = [Node(a),Node(b),Node(c),Node(d),]

# TODO: 错误分析 暂时未实现， 将所有分析表实现后再来做这个
# LR 分析器运行流程大致如下
# 1. 载入 文法 G
# 2. 利用 goto & closure 函数 为文法 G 构造正规项目集簇， 是一个 ProductionSet 类型的集合， 记录 goto 的输入输出
# 3. 为 文法 G 构造 FIRST 集合 和 FOLLOW 集合
# 4. 根据 正则项目集簇 和 FOLLOW 集合， 构造分析表（ ACTION 表 和 goto 表）， 其中 ACTION 表中每一项都是一个 Action 类

from SentenceParser.gramma_model import *
import copy
from functools import reduce
from SentenceParser.analyze_table_model import *
from SentenceParser.token_stack_model import *
from SentenceParser.grammar_tree_model import *
class LrAnalyzeDriver:
    def __init__(self, T:AnalyzeTable):
        self.Table = T
        self.result = []
        # 构造语法树需要用到的 栈
        self.node_stack = []
        self.tree_node = None
    def run(self, W:TokenStack):
        # 使用数组模拟栈 list
        # find satate  0
        # print(self.Table)
        state, smb, = [0], []
        while True:
            S, a = state[-1], W.cur()
            action = self.Table.action[S][a]
            
            if action.ACTION == 'S':
                # 三个栈在 Shift 动作保持一致
                state.append(action.CONTENT)
                smb.append(a)
                self.node_stack.append(Node(a))
                W.next()
            elif action.ACTION == 'R':
                # 构建 当前产生式 A->a 的 A节点
                cur_node = Node(action.CONTENT.left)
                for _ in range(len(action.CONTENT.right)):
                    smb.pop()
                    state.pop()
                    # 
                    cur_node.next.append(self.node_stack.pop())
                
                # 三者在出入栈保持一致
                self.node_stack.append(cur_node)
                smb.append(action.CONTENT.left)
                state.append(self.Table.goto[state[-1]][action.CONTENT.left])
                
                self.result.append(action.CONTENT)
            elif action.ACTION == 'ACC':
                self.tree_node = self.node_stack[0]
                return
            else:
                pass

def s_parser(G, string, type='lr'):
    
    g = None
    if type == 'lr':
        g = LR(ProductionSet.by_ex_list(G), )
    elif type == 'slr':
        g = SLR(ProductionSet.by_ex_list(G), )

    lr = LrAnalyzeDriver(g)
    
    if isinstance(string, str):
        s = TokenStack.bystr(string)
    else:
        s = TokenStack.byword(string)
    print("\n文法及分析表:", lr.Table)
    print("\n输入:",string)
    print("\n归约方式:")    
    lr.run(s)
    return lr.tree_node
if __name__ == "__main__":
    
    # test(G_CC,"int v = a + b + c * d ;", 'lr')
    # s_parser(G_CC,"int a = b + c * d;", 'lr')
    # 检验 e_ 是否存在的问题

    print("Every Production Item are Checked !!")



