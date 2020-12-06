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

import copy
from SentenceParser.gramma_model import *
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
            # action = self.Table.action[S][a]
            try:
                action = self.Table.action[S][a]
            except:
                raise Exception("<Symbol:'{}',{}>".format(a.val, a.pos))

            if action.ACTION == 'S':
                # 三个栈在 Shift 动作保持一致
                state.append(action.CONTENT)
                smb.append(a)
                self.node_stack.append(Node(a))
                W.next()
            elif action.ACTION == 'R':
                # 构建 当前产生式 A->a 的 A节点
                cur_node = Node(action.CONTENT.left, action.CONTENT)
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
import hashlib
import pickle
def hash_check(g):
    md5 = hashlib.md5()
    in_data = str(g).split(',')
    for d in in_data:
        md5.update(d.encode('UTF-8'))
    return md5.hexdigest()

def write(filename, data):
    with open(filename, 'w') as f:
        f.write(data.__str__())

def s_parser(G, string, type='lr'):
    # 计算 G 的哈希值
    # 如果该文法的哈希值与已有记录一致， 那么采用该分析表
    # 如果不一致， 那么重新计算
    hash_current_value, g = hash_check(G), None
    try:
        with open('SentenceParser/{}.pkl'.format(type), 'rb') as f:
            data = pickle.load(f)
            assert hash_current_value == data['HashValue']
            g = data['AnalyzeTable']
    except:
        if type == 'lr':
            g = LR(ProductionSet.by_ex_list(G), )
        elif type == 'slr':
            g = SLR(ProductionSet.by_ex_list(G), )
        with open('SentenceParser/{}.pkl'.format(type),'wb') as f:
            pickle.dump({'AnalyzeTable':g, 'HashValue':hash_current_value}, f, pickle.HIGHEST_PROTOCOL)

    # 构建分析器
    lr = LrAnalyzeDriver(g)
    
    # 构建符号栈
    s = TokenStack.bystr(string) if isinstance(string, str) else TokenStack.byword(string)

    print("\n归约方式:\n")    
    lr.run(s)
    return lr.tree_node, lr.Table
if __name__ == "__main__":
    
    # test(G_CC,"int v = a + b + c * d ;", 'lr')
    # s_parser(G_CC,"int a = b + c * d;", 'lr')
    # 检验 e_ 是否存在的问题

    print("Every Production Item are Checked !!")



