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
from SentenceParser.production_model import *
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
        # 初始化符号表
        smb_t.insert(Record('Program start'))
        smb_t.location()

        num, width = SemanticFunctionSet.sentence_list(node.next[0], 0)

        return num, width
        
    

    
    @staticmethod
    def type_declare_sentence(node, offset):

        t = SemanticFunctionSet.type_statement(node.next[-1])
        ids, width = SemanticFunctionSet.id_list(node.next[-2], t, offset)
        return len(ids), width
        

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

            ids, width = SemanticFunctionSet.id_list(node.next[0], T, offset)
            
            return ids + [node.next[-1].val.val], width + T.width
        
        elif node.production == Production.bystr("id_list->id"):
            # 此处是参数列表的第一个参数， 从此开始是函数体作用域了， 故使用 location 进行定位

            smb_t.insert(Record(node.next[-1].val.val, type_=T, offset=offset))

            offset += T.width
            return [node.next[-1].val.val], T.width
    @staticmethod
    def initialize(node,):
        # 这是关于 初始化列表 的定义， 
        # 在类型检查中， 需要检查 初始化的变量类型与值是否匹配
        pass

    # 函数的声明
    # 函数的名字应该在外部声明， 包含（名字， 参数数量， 参数宽度， 返回值类型， 局部数据区总宽度）
    # 参数的名字应该在内部声明， 包含？
    @staticmethod
    def func_define(node, ):
        # TODO：在此处发现了词法分析的 bug 标识符不能出现下划线
        # 1. 添加函数头部， 进入函数（名字， 参数数量， 参数宽度， 返回值类型， 局部数据区总宽度）
        # 我们需要将函数头部的定义放到函数外部的区域， 内部的进行重定位

        # 1. 建立record 
        return_type = SemanticFunctionSet.type_statement(node.next[-1])
        function_name = node.next[-2].val.val

        smb_t.insert(Record(function_name, type_ = FuncType(param_num =None, param_width=None, return_type=return_type, domain_width=None)))
        
        smb_t.insert(Record("Enter domain"))
        smb_t.location()

        # 这里的 0 是函数参数列表开始的偏移量
        param_num, param_width = SemanticFunctionSet.list_e(node.next[-4], 0)

        record, _ = smb_t.find(function_name)
        record.TYPE.param_num = param_num
        record.TYPE.param_width = param_width
        
        # 处理函数体, 要求返回函数体中的变量宽度
        # 便于调用函数时， 分配内存， 由于参数是传递的， 是在调用处作用域的变量， 无需分配
        domain_num, domain_width = SemanticFunctionSet.complex_sentence(node.next[0], param_width, forward = 'function')
        record.TYPE.domain_width = domain_width

        # 到这里， 使用该产生式 进行规约的时候已经处理完函数， 要进行重定位

        print("Touch The end of domain Symbol Table will be relocation")
        smb_t.print()
        smb_t.relocation()

        # func_declare 作为一个 sentence 元素因该返回 该调用 的总变量长度和数量
        # 但是函数的局部变量是 在函数执行完成后 回收的
        return param_num + domain_num, param_width + domain_width




    @staticmethod
    def list_e(node, offset):

        if node.production == Production.bystr("list->list@,@parameter"):
            param_num, param_width = SemanticFunctionSet.list_e(node.next[-1], offset)

            record = SemanticFunctionSet.parameter(node.next[0], param_width)
            smb_t.insert(record)

            return param_num + 1, param_width + record.TYPE.width         
        
        elif node.production == Production.bystr("list->parameter"):
            record = SemanticFunctionSet.parameter(node.next[-1], offset)
            smb_t.insert(record)

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
    def complex_sentence(node, offset, forward = 'domain'):
        if node.production == Production.bystr("complex_sentence->{@sentence_list@}"):
            # 这里的返回值是两个
            if forward == 'domain':
                smb_t.location()
            num, width = SemanticFunctionSet.sentence_list(node.next[1], offset)

            if forward == 'domain':
                print("Touch The end of domain Symbol Table will be relocation")
                smb_t.print()
                
                smb_t.relocation()
            return num, width
        
    
    @staticmethod
    def sentence_list(node, offset):

        if node.production == Production.bystr("sentence_list->sentence@sentence_list"):
            # 处理第一个句子偏移量不变
            
            num1, width1 = SemanticFunctionSet.sentence(node.next[-1], offset)
            offset += width1
            # 处理句子列表 偏移量从
            num2, width2 = SemanticFunctionSet.sentence_list(node.next[0], offset)

            return num1 + num2, width1 + width2
        
        elif node.production == Production.bystr("sentence_list->sentence"):
            num, width = SemanticFunctionSet.sentence(node.next[0], offset)
            return num, width 

        # 其他情况无论是 ->e_ 还是什么的都做 0，0 处理

        return 0, 0

    @staticmethod
    def sentence(node, offset):
        # 一下的每种句子都需要记录分配变量的宽度
        # func_define|if_sentence|for_sentence|while_sentence|go_sentence|expression_sentence|type_declare_sentence|complex_sentence
        # sentence 的返回值 是 2 个综合属性    1. 变量数目  2. 变量宽度
        # sentence 需要传入变量 offset， 但是函数定义的是特殊的， 他的入口偏移量固定为 0 ，根据不同的调用点 动态的分配变量空间 
        print(node.production)
        if node.production == Production.bystr("sentence->func_define"):
            # 函数声明不分配变量
            SemanticFunctionSet.func_define(node.next[0], )

            # 需要为函数名 在当前作用域 分配一个变量
            return 1, 0
        
        elif node.production == Production.bystr("sentence->if_sentence"):
            n,w = SemanticFunctionSet.if_sentence(node.next[0], offset)
            return n,w

        elif node.production == Production.bystr("sentence->for_sentence"):
            n,w = SemanticFunctionSet.for_sentence(node.next[0], offset)
            return n,w
        
        elif node.production == Production.bystr("sentence->while_sentence"):
            n,w = SemanticFunctionSet.while_sentence(node.next[0], offset)
            return n,w
        
        elif node.production == Production.bystr("sentence->go_sentence"):
            pass

        elif node.production == Production.bystr("sentence->expression_sentence"):
            _,_ = SemanticFunctionSet.expression_sentence(node.next[0])
            return 0, 0
        
        elif node.production == Production.bystr("sentence->type_declare_sentence"):
            num, width = SemanticFunctionSet.type_declare_sentence(node.next[0], offset)
            return num, width
        
        elif node.production == Production.bystr("sentence->complex_sentence"):
            num, width = SemanticFunctionSet.complex_sentence(node.next[0], offset)
            return num, width

    @staticmethod
    def expression_sentence(node):
        _, _ = SemanticFunctionSet.E1(node.next[-1])
        return 0, 0

    @staticmethod
    def E(node, ):
        # 'E->(@E1@)|id|NUM|STR|id@(@E1@)',
        if node.production == Production.bystr("E->(@E1@)"):
            t = SemanticFunctionSet.E(node.next[-2], )
            return t
        elif node.production == Production.bystr("E->id"):

            t = smb_t.find(node.next[0].val.val)[0].TYPE
            return t
        elif node.production == Production.bystr("E->NUM"):
            if '.' in node.next[0].val.val:
                t = Type('float', type_ = 'constant')
            else:
                t = Type('int', type_ = 'constant')
            return t
        elif node.production == Production.bystr("E->STR"):
            return Type('void')
        elif node.production == Production.bystr("E->id@(@E_dot_exp@)"):
            # param_type -> [Type, Type, ...]
            param_num, param_type = SemanticFunctionSet.E_dot_exp(node.next[-3], )
            

            func, _ = smb_t.find(node.next[-1].val.val)
            t = None
            if isinstance(func.TYPE, FuncType) and param_num == 0:
                t = func.TYPE.return_type
                return t
            # TODO： 这里涉及了如何 check 参数 和 类型， 这里我们需要定义 X 运算， 暂时不实现
            elif isinstance(func.TYPE, FuncType) and param_num == func.TYPE.param_num and func.TYPE.equal(param_type):
                t = func.TYPE.return_type
                return t
            else:
                raise Exception("type error in line {}".format(node.next[-1].val.pos))

        elif node.production == Production.bystr("E->(@E2@)"):
            t = SemanticFunctionSet.E2(node.next[-2], )
            return t
        elif node.production == Production.bystr("E->"):
            return Type('void')
        else:
            # print(node.production)
            raise Exception("No match production!")

    @staticmethod
    def E1(node, ):
        # 赋值表达式要求左边的类型是 变量
        if node.production == Production.bystr("E1->E1@F1@E_dot_exp"):
            n1, t1 = SemanticFunctionSet.E1(node.next[-1])
            n2, t2 = SemanticFunctionSet.E_dot_exp(node.next[-3])

            check = True
            if n1 != n2:check = False
            for t in t1:
                if t.type == 'constant':check = False
            for i in range(min(n1,n2)):
                if t1[i].name != t2[i].name:
                    check = False
            if check:
                return n1, t1

            else:
                raise Exception('Type Error!')

        elif node.production == Production.bystr("E1->E_dot_exp"):
            n, t_l = SemanticFunctionSet.E_dot_exp(node.next[-1])
            return n, t_l

    # 返回一个类型列表
    @staticmethod
    def E_dot_exp(node, ):
        # 需要返回 逗号表达式数量
        if node.production == Production.bystr("E_dot_exp->E_dot_exp@F_dot_exp@E2"):
            n1, t1 = SemanticFunctionSet.E_dot_exp(node.next[-1])
            t2 = SemanticFunctionSet.E2(node.next[-3])
            return n1 + 1, t1 + [t2]

        elif node.production == Production.bystr("E_dot_exp->E2"):
            t = SemanticFunctionSet.E2(node.next[-1])
            # print('*'*100)
            # print(t, type(t))


            if t.name == 'void':
                return 0, [t]
            else:
                return 1, [t]
            

    @staticmethod
    def E2(node, ):


        if node.production == Production.bystr("E2->E2@F2@E3"):
            t1 = SemanticFunctionSet.E2(node.next[-1])
            t2 = SemanticFunctionSet.E3(node.next[-3])
            if t1.TYPE.name == t2.TYPE.name == 'boolen':
                t = Type('boolen')
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E2->E3"):
            t = SemanticFunctionSet.E3(node.next[0])
            return t

    @staticmethod
    def E3(node, ):

        if node.production == Production.bystr("E3->E3@F3@E4"):
            t1 = SemanticFunctionSet.E3(node.next[-1])
            t2 = SemanticFunctionSet.E4(node.next[-3])
            if t1.TYPE.name == t2.TYPE.name == 'boolen':
                t = Type('boolen')
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E3->E4"):
            t = SemanticFunctionSet.E4(node.next[0])
            return t
    @staticmethod
    def E4(node, ):

        if node.production == Production.bystr("E4->E4@F4@E5"):
            t1 = SemanticFunctionSet.E4(node.next[-1])
            t2 = SemanticFunctionSet.E5(node.next[-3])
            if t1.name == t2.name:
                t = Type('boolen')
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E4->E5"):
            t = SemanticFunctionSet.E5(node.next[0])
            return t
    @staticmethod
    def E5(node, ):

        if node.production == Production.bystr("E5->E5@F5@E6"):
            t1 = SemanticFunctionSet.E5(node.next[-1])
            t2 = SemanticFunctionSet.E6(node.next[-3])
            if t1.name == t2.name:
                t = Type('boolen')
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E5->E6"):
            t = SemanticFunctionSet.E6(node.next[0])
            return t
    @staticmethod
    def E6(node, ):

        if node.production == Production.bystr("E6->E6@F6@E7"):
            t1 = SemanticFunctionSet.E6(node.next[-1])
            t2 = SemanticFunctionSet.E7(node.next[-3])
            if t1.name == 'int' and t2.name == 'int':
                t = Type('int')
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E6->E7"):
            t = SemanticFunctionSet.E7(node.next[0])
            return t
    @staticmethod
    def E7(node, ):

        if node.production == Production.bystr("E7->E7@F7@E8"):
            t1 = SemanticFunctionSet.E7(node.next[-1])
            t2 = SemanticFunctionSet.E8(node.next[-3])
            if t1.name == t2.name:
                t = t1
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E7->E8"):
            t = SemanticFunctionSet.E8(node.next[0])
            return t
    @staticmethod
    def E8(node, ):
        if node.production == Production.bystr("E8->E8@F8@E9"):
            t1 = SemanticFunctionSet.E8(node.next[-1])
            t2 = SemanticFunctionSet.E9(node.next[-3])
            if t1.name == t2.name:
                t = Type('int')
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))
        elif node.production == Production.bystr("E8->E9"):
            t = SemanticFunctionSet.E9(node.next[0])
            return t
    @staticmethod
    def E9(node, ):
        if node.production == Production.bystr("E9->E10@F9_1"):
            t = SemanticFunctionSet.E10(node.next[-1])
            return t

        # TODO：取地址 & 取值 & 取自身
        elif node.production == Production.bystr("E9->F9_2@E10"):
            t = SemanticFunctionSet.E9(node.next[0])
            return t
        
        elif node.production == Production.bystr("E9->F9_1@E10"):
            t = SemanticFunctionSet.E10(node.next[-2])
            return t
        
        elif node.production == Production.bystr("E9->E10"):
            t = SemanticFunctionSet.E10(node.next[0])
            return t
    
    @staticmethod
    def E10(node, ):
        if node.production == Production.bystr("E10->E10@[@E10@]"):
            t1 = SemanticFunctionSet.E10(node.next[-1])
            t2 = SemanticFunctionSet.E10(node.next[-3])
            if t2.TYPE == 'int' and t1.TYPE.name == 'pointer':
                return t
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))

        # TODO：取地址 & 取值 & 取自身
        elif node.production == Production.bystr("E10->E"):
            t = SemanticFunctionSet.E(node.next[0])
            return t
        

    @staticmethod
    def state(node, offset):
        n, width = 0, 0
        if node.production == Production.bystr("state->complex_sentence"):
            n, width = SemanticFunctionSet.complex_sentence(node.next[0], offset)
            
        elif node.production == Production.bystr("state->sentence"):
            n, width = SemanticFunctionSet.sentence(node.next[0], offset)
        return n, width
    @staticmethod
    def if_sentence(node, offset):
        # 'if_sentence -> if@(@E1@)@state@else@state|if@(@E1@)@state'
        n, width = 0, 0
        if node.production == Production.bystr("if_sentence -> if@(@E2@)@state@else@state"):
            t = SemanticFunctionSet.E2(node.next[-3])
            if t.name == 'boolen':
                # -5-7
                n1, w1 = SemanticFunctionSet.state(node.next[-5], offset)
                n2, w2 = SemanticFunctionSet.state(node.next[-7], offset + w1)
                n = n1 + n2
                width = w1 + w2
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))

            
            
        elif node.production == Production.bystr("if_sentence -> if@(@E2@)@state"):
            t = SemanticFunctionSet.E2(node.next[-3])
            if t.name == 'boolen':
                # -5-7
                n, width = SemanticFunctionSet.state(node.next[-5], offset)
            else:
                raise Exception("type error in line {}".format(node.next[0].val.pos))

        # 虽然有 变量数量和宽度， 但是在作用于结束的时候可以释放所以返回宽度不算
        return 0,0

    @staticmethod
    def for_sentence(node, offset):
        # 'for_sentence-> for@(@loop_control_sentence@loop_control_sentence@loop_control_sentence@)@complex_sentence
        #                 for@(@loop_control_sentence@)@sentence',
        # 此处由于 for 语句中可能有 变量声明， 所以一个 for 语句实际是两个 嵌套作用域
        smb_t.insert(Record('Enter for loop'))
        smb_t.location()

        n1, w1 = SemanticFunctionSet.loop_control_sentence(node.next[-3], offset)
        offset += w1
        n2, w2 = SemanticFunctionSet.loop_control_sentence(node.next[-4], offset)
        offset += w2
        n3, w3 = SemanticFunctionSet.loop_control_sentence(node.next[-5], offset)
        offset += w3
        
        if node.production == Production.bystr("for_sentence-> for@(@loop_control_sentence@loop_control_sentence@loop_control_sentence@)@complex_sentence"):
            # -3-4-5-7
            
            n4, w4 = SemanticFunctionSet.complex_sentence(node.next[-7], offset)
    
        elif node.production == Production.bystr("for_sentence-> for@(@loop_control_sentence@loop_control_sentence@loop_control_sentence@)@sentence"):
            
            n4, w4 = SemanticFunctionSet.sentence(node.next[0], offset)
            
        n, w = n1+n2+n3+n4, w1+w2+w3+w4
        smb_t.relocation()
        return 0, 0

    @staticmethod
    def loop_control_sentence(node, offset):
        n, w = 0, 0
        if node.production == Production.bystr("loop_control_sentence->expression_sentence"):
            n, w = SemanticFunctionSet.expression_sentence(node.next[0])
            
        elif node.production == Production.bystr("loop_control_sentence->type_declare_sentence"):
            n, w = SemanticFunctionSet.type_declare_sentence(node.next[0], offset)
        return n, w
    
    @staticmethod
    def while_sentence(node, offset):
        # while_sentence->while@(@E2@)@state
        t = SemanticFunctionSet.E2(node.next[-3])
        if t.name == 'boolen':
            n, w = SemanticFunctionSet.state(node.next[-5], offset)
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
        return 0, 0
    
    @staticmethod
    def go_sentence(node, ):
        # 'go_sentence->CONTINUE@;|BREAK@;|RETURN@;|RETURN@expression@;',
        if node.production == Production.bystr("go_sentence->CONTINUE@;"):
            pass
            
        elif node.production == Production.bystr("go_sentence->BREAK@;"):
            pass
        elif node.production == Production.bystr("go_sentence->RETURN@;"):
            pass
        elif node.production == Production.bystr("go_sentence->RETURN@E2@;"):
            pass
    


if __name__ == "__main__":
    getattr(SemanticFunctionSet,"test_demo")(1,2,3)
