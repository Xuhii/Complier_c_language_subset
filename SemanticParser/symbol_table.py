# 符号表类实现
# 功能描述：
# 1. 用于存储用户自定义变量， 在分析用户声明语句时向符号表中插入符号 和 尽可能多的添加信息
# 2. 在进入作用域 时创建子表， 退出作用域的时候 drop 子表（但是子表是否不应该删除？， 用于后续的分析）

# 实现细节：
# 1. 作用域 问题，所以符号表需要实现 子表
# 2. 实现插入的 insert() 方法
# 3. 实现删除的 remove() 方法
# 4. 创建子表的 create() 方法
# 5. 删除子表的 drop()   方法
# 那么符号表以什么样的存储结构来保存数据呢 ？

# 创建时机
# 

# 记录结构
# 分析树的 节点 中有一个 val:Symbol
# Symbol -> name, final, val, pos(x,y)
# 我们只取 name == id and final 的数据记录进符号表

import time
from prettytable import PrettyTable
# 符号表结构：栈式哈希符号表
class Record(object):
    def __init__(
        self, name,         type_ = None,           blkn = None, 
        offset = None,      count = None,           declare_line = None, 
        ref_line_list = [], link_field = -1):
        self.NAME = name
        self.TYPE = type_
        self.ADDR = (blkn, offset)
        self.COUNT = count
        self.DECLARE_LINE = declare_line
        self.REF_LINE_LIST = ref_line_list
        self.LINK_FIELD = link_field
    def __repr__(self):
        return [self.NAME,str(self.TYPE),str(self.ADDR),str(self.COUNT),str(self.DECLARE_LINE),str(self.REF_LINE_LIST),str(self.LINK_FIELD)]
    def __str__(self):
        return str(self.NAME) + str(self.TYPE)

class SymbolTable(object):
    def __init__(self, hash_table_length = 100):
        self.hash_table_length = hash_table_length
        self.hash_list = [-1 for _ in range(hash_table_length)]
        self.record_stack = list()
        self.index_list = list()
    def print(self):
        table = PrettyTable(['index','Name','Type','Addr','Count', "Dec_line", 'Ref_list', 'line_filed'])
        for index, item in enumerate(self.record_stack):
            table.add_row([index] + item.__repr__())
        print(table)
        t2 = PrettyTable(['index', 'Block index'])
        for index, i in enumerate(self.index_list[::-1]):
            t2.add_row([index, str(i)])
        print(t2)
        print('\n'*2)
        print("-"*100)
        print('\n'*4)

    # 插入一条符号记录
    # TODO 逻辑不对， 冲突不代表名字相同
    def insert(self, record:Record):
        index_in_hash_list = hash(record.NAME)%self.hash_table_length
        # 如果不冲突
        if self.hash_list[index_in_hash_list] != -1:
            tmp = self.hash_list[index_in_hash_list]
            # 这里不写 while tmp:因为 tmp 可能为 0
            while tmp != -1:
                if self.record_stack[tmp].LINK_FIELD >= self.index_list[-1] and self.record_stack[tmp].NAME == record.NAME:
                    raise Exception("标识符重定义")
                tmp = self.record_stack[tmp].LINK_FIELD
            record.LINK_FIELD = self.hash_list[index_in_hash_list]
            
        self.record_stack.append(record)
        self.hash_list[index_in_hash_list] = len(self.record_stack) - 1
    # 查找元素, 
    # TODO： 以 name:str 的形式还是 Symbol 的形式传进来都是可以的
    def find(self, name:str):
        try:name = name.NAME
        except:pass
        index_in_hash_list = hash(name)%self.hash_table_length
        if self.hash_list[index_in_hash_list] != -1:
            tmp = self.hash_list[index_in_hash_list]
            while tmp != -1:
                if self.record_stack[tmp].NAME == name:
                    # 除了返回记录， 还需要返回是否是局部变量
                    return self.record_stack[tmp], tmp >= self.index_list[-1]
                tmp = self.record_stack[tmp].LINK_FIELD  
        # 包含两种情况：1. 为空  2. 不为空找不到
        raise Exception("标识符未定义")

    # 一般在需要重定位的 insert 之后使用
    def location(self):
        self.index_list.append(len(self.record_stack) - 1)

    def relocation(self):

        while len(self.record_stack) - 1 >= self.index_list[-1]:
            # 删除时需要考虑改记录是否是 head, 从上往下一定是头
            self.hash_list[hash(self.record_stack[-1].NAME)%self.hash_table_length] = -1 if self.record_stack[-1].LINK_FIELD == -1 else self.record_stack[-1].LINK_FIELD
            self.record_stack.pop()

        self.index_list.pop()

    def _gen_var_name(self):
        return "_var_" + str(time.time()).replace('.', '_')
    def random_insert(self, type_):
        tmp = Record(self._gen_var_name(), type_ = type_)
        self.insert(tmp)
        return tmp

if __name__ == "__main__":
    # 符号表测试
    t = SymbolTable(hash_table_length = 5)
    t.insert(Record("i"))
    t.location()
    print(t)
    print("-"*100)
    t.insert(Record("j"))
    t.insert(Record("k"))
    t.insert(Record("l"))
    t.insert(Record("m"))
    t.insert(Record("n"))
    # t.insert(Record("n"))
    print(t)
    print("-"*100)
    print(t.find('i'))
    print(t.find('j'))
    print(t.find('k'))
    print(t.find('l'))
    print(t.find('m'))
    print(t.find('n'))
    # print(t.find('cc'))
    print(t)
    print("-"*100)
    t.insert(Record("domain"))
    t.location()
    
    t.insert(Record("a"))
    t.insert(Record("b"))
    t.insert(Record("c"))
    t.insert(Record("d"))
    t.insert(Record("e"))
    t.insert(Record("i"))
    print(t)
    print("-"*100)
    print(t.find("i"))
    print(t.find("j"))
    
    t.relocation()
    print(t)
    print("-"*100)


