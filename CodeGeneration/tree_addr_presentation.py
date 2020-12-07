class Quaternion(object):
    def __init__(self, ID:int, op:str, arg1 = None, arg2 = None, result = None):
        # 这里的参数类型应该是什么呢
        self.id = ID
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    def __repr__(self):
        return [self.id, self.op, self.arg1, self.arg2, self.result]
    def __str__(self):
        return "${} <op:{}>, <arg1:{}>, <arg2:{}>, <result:{}>".format(self.id, self.op, self.arg1, self.arg2, self.result)