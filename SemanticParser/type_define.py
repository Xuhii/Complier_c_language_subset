# type 类型提供内存分配， 等操作
class Type:
    def __init__(self, name = 'int'):
        
        self.name = name
        if self.name == 'int':
            self.width = 4
        if self.name == 'float':
            self.width = 4
        if self.name == 'void':
            self.width = 0
        if self.name == 'char':
            self.width = 1
        if self.name == 'boolen':
            self.width = 1

class FuncType:
    def __init__(self,  param_num =None, param_width=None, return_type=None, domain_width=None):

            self.return_type = return_type
            self.param_num = param_num
            self.param_width = param_width
            self.domain_width = domain_width