from WordParser import tools
class State(object):
    def __init__(self, dic = {}, state = -1, isFinal = False):
        super().__init__()
        # int present the state and the index of state_matrix
        self.edges = dic
        self.state = state
        self.isFinal = isFinal
        
    def isFinal(self):
        return self.isFinal
    
    # 对于优先级的确定： 1. 字符本身   2. 字符代表的类型    3. 在射出边是否有any
    def next(self, s):
        if s in self.edges:
            return self.edges[s]
        elif tools.type(s) in self.edges:
            return self.edges[tools.type(s)]
        elif "any" in self.edges:
            return self.edges["any"]
        raise Exception('No Fit Edge.')


class StateMa(object):
    # 访问到 -1 的状态时抛出 NoFinalStateError
    def __init__(self, matrix = [], final = []):
        super().__init__()
        # int present the state and the index of state_matrix
        self.state = 0
        self.final = final
        self.matrix = []
        self.path = ""

        for i in range(len(matrix)):
            self.matrix.append(State(matrix[i], i, True if i in final else False))

    
    # 用于合并初态
    def extend(self, states = []):
        # 返回一个状态机， 其中
        pass

    # 初始化状态机， 识别得到一个 token 后， 识别下一个 token 的时候， 使用
    def initialize(self):
        self.state = 0
        self.path = ""

    # 状态转移
    def move(self, ch):
        try:
            self.state = self.matrix[self.state].next(ch)
        except:
            self.state = float('inf') if self.state not in self.final else self.state
            return False
        self.path += ch if ch != ' ' else ''
        return True

    # 如果是以 inf 状态结束的， 说明发生了错误
    def wrong(self):
        return self.state == float('inf')