# 语法翻译制导程序的设计
# 首先需要 对文法的语义进行定义
# 输入： 语法制导定义
# 输出： 语法制导翻译程序
# 方法： 为每一个非终结符 A 建立一个函数
# 1. 函数头
#       函数名： A
#       参数： 当前分析树节点， A 的每一个继承属性
#       返回值： A 的综合属性（ python 的特性是可以返回多个 S 属性）
# 2. 局部变量
#       为 A 的每一个属性声明一个相应的局部变量
# 3. 分支代码
#       为 A 的每一个候选式 设计一个分支
# 4. 分支代码细节
#       根据 语义规则 & 属性依赖关系 来确定访问子节点的顺序
#       1. 叶子节点: 若对应记号 X 有属性 x, 则把它的值保存到相应的局部变量中
#       2. 内部节点: 先计算 继承属性 B.i 然后计算 B 的综合属性 c = B(node, B.1, B.2, B.3, .. , B.k)

# TODO:好像不需要使用 getattr(SemanticFunctionSet 来映射, 因为每个函数的调用对象都是固定的
# 类型检查的语义：
# 1. 类型表达式
# 2. 类型等价（怎样的类型是等价的 - 关于这一点， 如果语言没有实现 struct/class 的情况是不需要考虑的）
# 如何实现一个类型检查程序
# 1. 过程中的声明语句
# 2. 过程的定义处理
# 3. 记录声明的处理(类似于 c结构体)
# 4. 表达式类型检查
# 5. 语句类型检查 
# 6. 类型转换（在该 c语言子集上不需要做这个）

from SemanticParser.type_define import *
from SemanticParser.symbol_table import *
import time
# 定义全局符号表, 哈希 mod = 100 
# def insert(record:Record)
# def find(name:str)
# def location()
# def relocation()

smb_t = SymbolTable(100)

class SemanticFunctionSet:
    # Function Demo In Semantic Analyze
    # @staticmethod
    # def test_demo(production,  *args, **kwargs):
    #     if production == value_1:
    #         pass
    #     elif production == value_2:
    #         pass
    #     elif production == value_3:
    #         pass
    #     elif production == value_4:
    #         pass
    @staticmethod
    def test_demo(a, b, c):
        print(a,b,c)
    

    # 注意：子节点列表的顺序 都是与 产生式右部符号 顺序相反
    # Tips: 设计语义函数可以从下往上设计， 不容易漏掉细节
    @staticmethod
    def S(node):
        # 在初始节点有一个 offset 变量用于存储变量的偏移量
        # 这个值可能不是 0 可能源于启动该程序时的内存区？？？（后续可以改为 S 的输入值）
        
        
    
    # 变量的声明处理
    @staticmethod
    def sentence_list(node):
        pass
    
    @staticmethod
    def sentence(node):
        pass
    
    @staticmethod
    def type_declare_sentence(node, offset):
        t = SemanticFunctionSet.type_statement(node.next[-1])
        ids = SemanticFunctionSet.id_list(node.next[-2], t, offset)
        # 
        

    @staticmethod
    def type_statement(node):
        # int float voit char boolen, 这里可以直接抽象表达， 直接用产生式右边第一个字符的 name， 为了统一书写形式， 就写成 if
        # TODO：这里存在的问题是   分配结构体的内存 && 定义结构体类型
        # TODO： 列表类型暂时不考虑， 之后回慢慢完善类型
        if node.production == Production.bystr("type_statement->int"):
            return Type(name='int')
           
        elif node.production == Production.bystr("type_statement->float"):
            return Type(name='float')
        
        elif node.production == Production.bystr("type_statement->void"):
            return Type(name='void')
        
        elif node.production == Production.bystr("type_statement->char"):
            return Type(name='char')
        
        elif node.production == Production.bystr("type_statement->boolen"):
            return Type(name='int')
    
    @staticmethod
    def id_list(node, T:Type, offset):

        # 约定声明语句会返回声明变量的列表 & 初始化列表一一匹配
        if node.production == Production.bystr("id_list->id@,@id_list"):
            # 先将 id 添加到符号表
            smb_t.insert(Record(node.next[-1].val.val, type_=T, offset = offset))
            offset += T.width
            
            return SemanticFunctionSet.sentence_list(node.next[0], T, offset) + [node.next[-1].val.val]
        
        elif node.production == Production.bystr("id_list->id"):
            # 此处是参数列表的第一个参数， 从此开始是函数体作用域了， 故使用 location 进行定位
            smb_t.insert(Record(node.next[-1].val.val, type_=T, offset=offset))
            smb_t.location()
            offset += T.width
            return [node.next[-1].val.val] 
    @staticmethod
    def initialize(node,):
        # 这是关于 初始化列表 的定义， 
        # 在类型检查中， 需要检查 初始化的变量类型与值是否匹配
        pass

    # 函数的声明
    # 函数的名字应该在外部声明， 包含（名字， 参数数量， 参数宽度， 返回值类型， 局部数据区总宽度）
    # 参数的名字应该在内部声明， 包含？
    @staticmethod
    def func_declare(node, ):
        # TODO：在此处发现了词法分析的 bug 标识符不能出现下划线
        # 1. 添加函数头部， 进入函数（名字， 参数数量， 参数宽度， 返回值类型， 局部数据区总宽度）
        # 我们需要将函数头部的定义放到函数外部的区域， 内部的进行重定位

        # 1. 建立record 
        return_type = SemanticFunctionSet.type_statement(node.next[-1])
        function_name = node.next[-2].val.val

        smb_t.insert(Record(function_name, type_ = FuncType(param_num =None, param_width=None, return_type=return_type, domain_width=None)))

        param_num, param_width = SemanticFunctionSet.list_(node.next[-4], 0)

        record = smb_t.find(function_name)
        record.TYPE.param_num = param_num
        record.TYPE.param_width = param_width
        
        # 处理函数体, 要求返回函数体中的变量宽度
        domain_width = SemanticFunctionSet.complex_sentence(node.next[0])
        record.TYPE.domain_width = domain_width




    @staticmethod
    def list_(node, offeset):
        if node.production == Production.bystr("list@,@parameter"):
            param_num, param_width = list_(node.next[-1], offset)

            record = parameter(node.next[0], param_width)
            smb_t.insert(record)

            return  param_num + 1, param_width + record.TYPE.width         
        
        elif node.production == Production.bystr("list@parameter"):
            record = parameter(node.next[-1], offset)
            smb_t.insert(t)
            return  1, record.TYPE.width
    @staticmethod
    def parameter(node, offset):
        if node.production == Production.bystr("parameter->type_statement@id"):
            t = SemanticFunctionSet.type_statement(node.next[-1])
            return Record(node.next[-2].val.val, type_=t, offset=offset)
        elif node.production == Production.bystr("parameter->type_statement"):
            t = SemanticFunctionSet.type_statement(node.next[-1])
            return Record(str(time.time()), type_=t, offset=offset)
    # 统计作用域中的参数宽度
    @staticmethod
    def complex_sentence(node, ):
        if node.production == Production.bystr("complex_sentence->{@sentence_list@}"):
            pass
        
    
    @staticmethod
    def sentence_list(node, ):
        if node.production == Production.bystr("sentence_list->sentence@sentence_list"):
            pass
        if node.production == Production.bystr("sentence_list->sentence_list"):
            pass
        if node.production == Production.bystr("sentence_list->e_"):
            pass

    @staticmethod
    def sentence(node, ):
        # 一下的每种句子都需要记录分配变量的宽度
        # func_define|if_sentence|for_sentence|while_sentence|go_sentence|expression_sentence|type_declare_sentence|complex_sentence

        if node.production == Production.bystr("sentence->func_define"):
            pass
        if node.production == Production.bystr("sentence->if_sentence"):
            pass

        if node.production == Production.bystr("sentence->for_sentenc"):
            pass
        if node.production == Production.bystr("sentence->while_sentence"):
            pass
        if node.production == Production.bystr("sentence->go_sentence"):
            pass

        if node.production == Production.bystr("sentence->expression_sentence"):
            pass
        if node.production == Production.bystr("sentence->type_declare_sentence"):
            pass
        if node.production == Production.bystr("sentence->complex_sentence"):
            pass

if __name__ == "__main__":
    getattr(SemanticFunctionSet,"test_demo")(1,2,3)
