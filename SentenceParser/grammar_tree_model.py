# 多叉树 ASCII 显示实现
# 目的实现一个多叉树， 并且要将其能展示在命令行窗口
#              🌹           
#              |           
#   +-----+---+-----+-----+
#   ℋ     ℯ   ℒ     ℒ     ℴ
#   |     |         |      
# +---+   +       +---+    
# W   o   r       l   d   
# 思路如下：
# 1.首先计算一个子树需要多大的画布 canvas
# 2.已知叶节点需要大小为 1 的画布
# TODO 根据 1，2 可以对树进行 后序遍历 ， 计算得到每个 子树 需要多大额画布，实现 Node.compute_size() 函数
# 
# 再考虑如何确定一个子树在一个画布的位置呢 ？
# 1.可以考虑求一个子树的根节点的 位置
# 2.如果已知画布大小， 可以很容易的求出每个画布的左上角的坐标（只需累加一个节点的子节点画布宽度， 加上预先设定好的宽度）
# TODO 实现 Node.compute_left_up_position()
# 
# 现在已经确定了每个画布的 left-up 坐标， 
# 1. 显然的叶节点的 left-up 坐标就是叶节点的节点坐标（边界）
# 1. 由此， 可以想到 一个子树的根节点坐标， 等于其最远的两个直接子节点的中点， 那么我们就可以递归的求到每个根节点的坐标
# TODO 实现 Node.compute_node_position() 函数

from SentenceParser.expression_model import Symbol
import random
class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "<{}, {}>".format(self.x, self.y)
    def __repr__(self):
        return self.__str__()

class Size:
    def __init__(self, x, y):
        self.w = x
        self.h = y
    def __str__(self):
        return "<{}, {}>".format(self.w, self.h)
    def __repr__(self):
        return self.__str__()

# 如果要为节点添加新内容， 只需要在 val 的 Symbol 中添加， 而不是在 Node 类中添加
class Node:    
    def __init__(self, val = None, inner = 3):
        # 公有成员变量
        # 这里的 val 是一个 Symbol 类型， 其中包含了 Pos ， 与用来画分析树的 Pos 不冲突
        self.next = []
        self.val = val

        # 私有成员变量
        self.__size = Size(0, 0)
        self.__pos = Pos(0, 0) 
    def __len__(self):
        return len(self.val)
    def __str__(self):
        return Node.draw(self)

    @staticmethod
    def compute_size(root, inner):
        if not root.next:
            root.__size = Size(1, 1)
            return root.__size
        s = Size(0, 0)
        for node in root.next:
            tmp = Node.compute_size(node, inner)
            s.h = max(s.h, tmp.h)
            s.w += tmp.w
        s.h += len(root.val.name) + 4
        s.w += (len(root.next)-1) * inner
        root.__size = s
        return s
    
    @staticmethod
    def compute_position(root, inner, offset):
        if not root.next:
            root.__pos.x += offset
            return root.__pos

        # 先顺
        for i, node in enumerate(root.next[::-1]):
            if not i:
                node.__pos = Pos(root.__pos.x, root.__pos.y + len(root.val.name) + 4)
            else:
                node.__pos = Pos(
                    root.next[::-1][i-1].__pos.x 
                        + root.next[::-1][i-1].__size.w 
                        + inner, 
                    root.next[::-1][i-1].__pos.y)
        
        # 递归调用
        left, right = None, None
        for i, node in enumerate(root.next[::-1]):
            tmp= Node.compute_position(node, inner, offset)
            left = tmp if not i else left
            right = tmp if i == len(root.next) - 1 else tmp
        
        # 后序
        root.__pos.x = (left.x + right.x)//2   
        return root.__pos
        
    @staticmethod
    def draw(root):
        # test
        # dfs(root)
        inner = 3
        S = Node.compute_size(root, inner)
        # Node.compute_left_up_position(root, inner,)
        _ = Node.compute_position(root, inner, inner * 2)
        canvs = [[' ' for _ in range(S.w + 20)] for _ in range(S.h + 20)]
        def _lane_vertical(node):
            nonlocal canvs
            if node.next:
                for i in range(node.next[-1].__pos.x, node.next[0].__pos.x + 1):
                    if len(node.next) > 1:
                        canvs[node.__pos.y + len(node.val.name)][i] = ' '
                        canvs[node.__pos.y + len(node.val.name) + 1][i] = '┆'
                    else:
                        canvs[node.__pos.y  + len(node.val.name)][i] = ' '
                        canvs[node.__pos.y  + len(node.val.name) + 1][i] = '┄'

            if node.__pos.y - 1 >= 0:
                canvs[node.__pos.y - 2][node.__pos.x]= '┄'
                canvs[node.__pos.y - 1][node.__pos.x]= ' '

            for i, ch in enumerate(node.val.name):
                canvs[node.__pos.y + i][node.__pos.x]= ch
        def _draw(r):
            nonlocal canvs
            if not r:
                return
            _lane_vertical(r)
            for node in r.next[::-1]:
                _draw(node)
        _draw(root)
        res = ''
        for j in range(len(canvs[0])):
            for i in range(len(canvs)):
                res += canvs[i][j]
            res += '\n'
        return res
            
def dfs(root):
    if not root.next:
        return
    for node in root.next:
        print(node.val.info())
        dfs(node)
    

if __name__ == "__main__":
    root = Node(Symbol('🌹'))
    L = [Node(Symbol('ℋ')),Node(Symbol('ℯ')),Node(Symbol('ℒ')),Node(Symbol('ℒ')),Node(Symbol('ℴ')),][::-1]
    l11 = [Node(Symbol('W')), Node(Symbol('o'))][::-1]
    l12 = [Node(Symbol('r'))]
    l13 = [Node(Symbol('l')), Node(Symbol('d'))][::-1]

    L[1].next = l13
    L[3].next = l12
    L[4].next = l11
    root.next = L
    print(root)
    print()











