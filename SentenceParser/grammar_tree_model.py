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

class Node:    
    def __init__(self, val = None, inner = 3):
        self.next = []
        self.val = val
        self.size = Size(0, 0)
        self.pos = Pos(0, 0) 
    def __len__(self):
        return len(self.val)
    def __str__(self):
        return Node.draw(self)

    @staticmethod
    def compute_size(root, inner):
        if not root.next:
            root.size = Size(1, 1)
            return root.size
        s = Size(0, 0)
        for node in root.next:
            tmp = Node.compute_size(node, inner)
            s.h = max(s.h, tmp.h)
            s.w += tmp.w
        s.h += len(root.val.name) + 4
        s.w += (len(root.next)-1) * inner
        root.size = s
        return s
    
    @staticmethod
    def compute_position(root, inner, offset):
        if not root.next:
            root.pos.x += offset
            return root.pos

        # 先顺
        for i, node in enumerate(root.next[::-1]):
            if not i:
                node.pos = Pos(root.pos.x, root.pos.y + len(root.val.name) + 4)
            else:
                node.pos = Pos(
                    root.next[::-1][i-1].pos.x 
                        + root.next[::-1][i-1].size.w 
                        + inner, 
                    root.next[::-1][i-1].pos.y)
        
        # 递归调用
        left, right = None, None
        for i, node in enumerate(root.next[::-1]):
            tmp= Node.compute_position(node, inner, offset)
            left = tmp if not i else left
            right = tmp if i == len(root.next) - 1 else tmp
        
        # 后序
        root.pos.x = (left.x + right.x)//2   
        return root.pos
        
    @staticmethod
    def draw(root):
        inner = 3
        S = Node.compute_size(root, inner)
        # Node.compute_left_up_position(root, inner,)
        _ = Node.compute_position(root, inner, inner * 2)
        canvs = [[' ' for _ in range(S.w + 20)] for _ in range(S.h + 20)]
        def _lane_vertical(node):
            nonlocal canvs
            if node.next:
                for i in range(node.next[-1].pos.x, node.next[0].pos.x + 1):
                    if len(node.next) > 1:
                        canvs[node.pos.y + len(node.val.name)][i] = ' '
                        canvs[node.pos.y + len(node.val.name) + 1][i] = '┆'
                    else:
                        canvs[node.pos.y  + len(node.val.name)][i] = ' '
                        canvs[node.pos.y  + len(node.val.name) + 1][i] = '┄'

            if node.pos.y - 1 >= 0:
                canvs[node.pos.y - 2][node.pos.x]= '┄'
                canvs[node.pos.y - 1][node.pos.x]= ' '

            for i, ch in enumerate(node.val.name):
                canvs[node.pos.y + i][node.pos.x]= ch
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











