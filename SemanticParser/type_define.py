# type 类型提供内存分配， 等操作
class Type:
    def __init__(self, name = 'int', type_='var'):
        
        self.type = type_

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
        
    def __repr__(self):
        return "<type:{}>".format(self.name)

    def __str__(self):
        return self.__repr__()


class FuncType:
    def __init__(self,  param_num =None, param_width=None, return_type=None, domain_width=None, param_type=None):

            self.return_type = return_type
            self.param_num = param_num
            self.param_width = param_width
            self.domain_width = domain_width
            self.param_type = param_type
    def __repr__(self):
        return "<function:rtype:{}>".format(self.return_type)

    def __str__(self):
        return self.__repr__()
    # TODO: 实现类型比较
    def equal(self, t_:list):
        return True