
from SemanticParser.symbol_table import *
from CodeGeneration.tree_addr_presentation import *
from CodeGeneration.nasm_model import *

from SemanticParser.type_define import *
from SentenceParser.production_model import *

# 功能分析
# 1. 变量赋值
# 2. 表达式计算
# 3. 记录类型成员访问       (X)
# 4. 数组操作              (X)
# 5. 类型转换              (X)
# 6. 布尔表达式
# 7. 控制语句
# 8. 过程调用语句

# 生成四元码需要符号表
# find()
# insert()
# random_insert()
# relacation()
# location()
smb_t = SymbolTable(100)


# 生成四地址码输出类
# add()
# save()
# load()
# print(self)
nasm = Nasm()




    
def test_demo(a, b, c):
    print(a,b,c)


# 注意：子节点列表的顺序 都是与 产生式右部符号 顺序相反
# Tips: 设计语义函数可以从下往上设计， 不容易漏掉细节
class CodeGen:
    @staticmethod
    def S(node):
        # 在初始节点有一个 offset 变量用于存储变量的偏移量
        # 这个值可能不是 0 可能源于启动该程序时的内存区？？？（后续可以改为 S 的输入值）
        # 初始化符号表
        smb_t.insert(Record('Program start'))
        smb_t.location()

        num, width, l = sentence_list(node.next[0], 0)


        return num, width, nasm
    



# 变量声明语句
# CHECK
def type_declare_sentence(node, offset):

    t = type_statement(node.next[-1])
    ids, width = id_list(node.next[-2], t, offset)
    for ID in ids:
        nasm.add('=', smb_t.find(ID)[0], None, None)
    return len(ids), width, len(ids)
    

# 变量声明
# CHECK
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
        return Type(name='boolen')

def id_list(node, T:Type, offset):
    # 约定声明语句会返回声明变量的列表 & 初始化列表一一匹配
    if node.production == Production.bystr("id_list->id@,@id_list"):
        # 先将 id 添加到符号表
        smb_t.insert(Record(node.next[-1].val.val, type_=T, offset = offset))
        offset += T.width

        ids, width = id_list(node.next[0], T, offset)
        
        return ids + [node.next[-1].val.val], width + T.width
    
    elif node.production == Production.bystr("id_list->id"):
        # 此处是参数列表的第一个参数， 从此开始是函数体作用域了， 故使用 location 进行定位

        smb_t.insert(Record(node.next[-1].val.val, type_=T, offset=offset))

        offset += T.width
        return [node.next[-1].val.val], T.width

def initialize(node,):
    # 这是关于 初始化列表 的定义， 
    # 在类型检查中， 需要检查 初始化的变量类型与值是否匹配
    pass

# TODO 函数的声明
# 函数的名字应该在外部声明， 包含（名字， 参数数量， 参数宽度， 返回值类型， 局部数据区总宽度）
# 参数的名字应该在内部声明， 包含？
def func_define(node, ):
    # TODO：在此处发现了词法分析的 bug 标识符不能出现下划线
    # 1. 添加函数头部， 进入函数（名字， 参数数量， 参数宽度， 返回值类型， 局部数据区总宽度）
    # 我们需要将函数头部的定义放到函数外部的区域， 内部的进行重定位

    # 1. 建立record 
    return_type = type_statement(node.next[-1])
    function_name = node.next[-2].val.val

    smb_t.insert(Record(function_name, type_ = FuncType(param_num =None, param_width=None, return_type=return_type, domain_width=None)))
    
    smb_t.insert(Record("Enter domain"))
    smb_t.location()

    # 这里的 0 是函数参数列表开始的偏移量
    param_num, param_width = list_e(node.next[-4], 0)
    try:
        record, _ = smb_t.find(function_name)
    except:
        raise Exception("Id Undefine {}, {}".format(function_name, node.next[-2].val.pos))
    record.TYPE.param_num = param_num
    record.TYPE.param_width = param_width
    
    # 处理函数体, 要求返回函数体中的变量宽度
    # 便于调用函数时， 分配内存， 由于参数是传递的， 是在调用处作用域的变量， 无需分配
    domain_num, domain_width, l = complex_sentence(node.next[0], param_width, forward = 'function')
    record.TYPE.domain_width = domain_width

    # 到这里， 使用该产生式 进行规约的时候已经处理完函数， 要进行重定位

    smb_t.relocation()

    # func_declare 作为一个 sentence 元素因该返回 该调用 的总变量长度和数量
    # 但是函数的局部变量是 在函数执行完成后 回收的
    return param_num + domain_num, param_width + domain_width

def list_e(node, offset):

    if node.production == Production.bystr("list->list@,@parameter"):
        param_num, param_width = list_e(node.next[-1], offset)

        record = parameter(node.next[0], param_width)
        smb_t.insert(record)

        return param_num + 1, param_width + record.TYPE.width         
    
    elif node.production == Production.bystr("list->parameter"):
        record = parameter(node.next[-1], offset)
        smb_t.insert(record)

        return  1, record.TYPE.width

def parameter(node, offset):
    if node.production == Production.bystr("parameter->type_statement@id"):
        t = type_statement(node.next[-1])
        return Record(node.next[-2].val.val, type_=t, offset=offset)
    elif node.production == Production.bystr("parameter->type_statement"):
        t = type_statement(node.next[-1])
        return Record(str(time.time()), type_=t, offset=offset)
# 统计作用域中的参数宽度

# CHECK  
def complex_sentence(node, offset, forward = 'domain'):
    if node.production == Production.bystr("complex_sentence->{@sentence_list@}"):
        # 这里的返回值是两个
        if forward == 'domain':
            smb_t.insert(Record("Enter Domain"))
            smb_t.location() 
        
        num, width, l = sentence_list(node.next[1], offset)

        if forward == 'domain':
            smb_t.relocation()
        return num, width, l
 
# CHECK   
def sentence_list(node, offset):

    if node.production == Production.bystr("sentence_list->sentence@sentence_list"):
        # 处理第一个句子偏移量不变
        
        num1, width1, l1 = sentence(node.next[-1], offset)
        offset += width1
        # 处理句子列表 偏移量从
        num2, width2,l2= sentence_list(node.next[0], offset)

        return num1 + num2, width1 + width2, l1 + l2
    
    elif node.production == Production.bystr("sentence_list->sentence"):
        num, width, l = sentence(node.next[0], offset)
        return num, width, l

    # 其他情况无论是 ->e_ 还是什么的都做 0，0 处理

    return 0, 0, 0

def sentence(node, offset):
    # 一下的每种句子都需要记录分配变量的宽度
    # func_define|if_sentence|for_sentence|while_sentence|go_sentence|expression_sentence|type_declare_sentence|complex_sentence
    # sentence 的返回值 是 2 个综合属性    1. 变量数目  2. 变量宽度
    # sentence 需要传入变量 offset， 但是函数定义的是特殊的， 他的入口偏移量固定为 0 ，根据不同的调用点 动态的分配变量空间 

    # 函数调用先不管
    if node.production == Production.bystr("sentence->func_define"):
        # 函数声明不分配变量
        func_define(node.next[0], )

        # 需要为函数名 在当前作用域 分配一个变量
        return 1, 0, 0
    
    elif node.production == Production.bystr("sentence->if_sentence"):
        n,w,l = if_sentence(node.next[0], offset)
        return n,w,l

    elif node.production == Production.bystr("sentence->for_sentence"):
        n,w,l = for_sentence(node.next[0], offset)
        return n,w,l
    
    elif node.production == Production.bystr("sentence->while_sentence"):
        n,w,l = while_sentence(node.next[0], offset)
        return n,w,l
    
    elif node.production == Production.bystr("sentence->go_sentence"):
        pass

    elif node.production == Production.bystr("sentence->expression_sentence"):
        _,_,e, l = expression_sentence(node.next[0])
        return 0, 0,l
    
    elif node.production == Production.bystr("sentence->type_declare_sentence"):
        num, width,l = type_declare_sentence(node.next[0], offset)
        return num, width,l
    
    elif node.production == Production.bystr("sentence->complex_sentence"):
        num, width,l = complex_sentence(node.next[0], offset)
        return num, width,l

# CHECK
def expression_sentence(node):
    _, _,e, l = E1(node.next[-1])
    return 0, 0,e,l




# 赋值顺序应该从右往左
# CHECK
def E1(node, ):
    # 赋值表达式要求左边的类型是 变量
    if node.production == Production.bystr("E1->E1@F1@E_dot_exp"):
        n2, t2, e2, l2 = E_dot_exp(node.next[-3])
        n1, t1, e1, l1 = E1(node.next[-1])
        

        check = True
        print(t1, t2)
        if n1 != n2:check = False
        
        for t in t1:
            if t.type == 'constant':check = False
        
        for i in range(min(n1,n2)):
            if t1[i].name != t2[i].name:
                check = False


        if check:
            for i in range(len(e1)):
                nasm.add(node.next[-2].next[0].val.val, e1[i], e2[i], e1[i])

            return n1, t1, e1, l1+l2+len(e1)
        else:
            raise Exception('Type Error!')

    elif node.production == Production.bystr("E1->E_dot_exp"):
        n, t_l, e, l = E_dot_exp(node.next[-1])
        return n, t_l, e, l

# 返回一个num, 类型列表, entry列表
# CHECK
def E_dot_exp(node, ):
    # 需要返回 逗号表达式数量
    if node.production == Production.bystr("E_dot_exp->E_dot_exp@F_dot_exp@E2"):
        n1, t1, e1, l1 = E_dot_exp(node.next[-1])
        t2, e2, l2 = E2(node.next[-3])
        return n1 + 1, t1 + [t2], e1 + [e2], l1+l2

    elif node.production == Production.bystr("E_dot_exp->E2"):
        t, e, l = E2(node.next[-1])
        # print('*'*100)
        # print(t, type(t))


        if t.name == 'void':
            return 0, [t], [e], l
        else:
            return 1, [t], [e], l
        

# CHECK
def E2(node, ):


    if node.production == Production.bystr("E2->E2@F2@E3"):
        t1, e1, l1 = E2(node.next[-1])
        t2, e2,l2 = E3(node.next[-3])
        if t1.name == t2.name == 'boolen':
            t = Type('boolen')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            return t,e,l1+l2+1
        elif t1.name == t2.name == 'int':
            t = Type('int')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val+'_bit', e1, e2, e)
            return t,e,l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E2->E3"):
        t,e,l = E3(node.next[0])
        return t,e,l

# CHECK
def E3(node, ):

    if node.production == Production.bystr("E3->E3@F3@E4"):
        t1, e1,l1 = E3(node.next[-1])
        t2, e2,l2 = E4(node.next[-3])
        if t1.name == t2.name == 'boolen':
            t = Type('boolen')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            return t, e, l1+l2+1
        elif t1.name == t2.name == 'int':
            t = Type('int')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val + "_bit", e1, e2, e)
            return t,e , l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E3->E4"):
        t,e,l = E4(node.next[0])
        return t,e,l

# CHECK
def E4(node, ):

    if node.production == Production.bystr("E4->E4@F4@E5"):
        t1,e1,l1 = E4(node.next[-1])
        t2,e2,l2 = E5(node.next[-3])
        if t1.name == t2.name:
            t = Type('boolen')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            return t, e,l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E4->E5"):
        t,e,l = E5(node.next[0])
        return t,e,l

# CHECK
def E5(node, ):

    if node.production == Production.bystr("E5->E5@F5@E6"):
        t1, e1,l1 = E5(node.next[-1])
        t2, e2,l2 = E6(node.next[-3])
        if t1.name == t2.name:
            t = Type('boolen')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            return t, e,l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E5->E6"):
        t, e,l = E6(node.next[0])
        return t, e,l

# CHECK
def E6(node, ):

    if node.production == Production.bystr("E6->E6@F6@E7"):
        t1, e1, l1 = E6(node.next[-1])
        t2, e2, l2 = E7(node.next[-3])
        if t1.name == 'int' and t2.name == 'int':
            t = Type('int')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            
            return t, e, l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E6->E7"):
        t,e,l = E7(node.next[0])
        return t,e,l

# CHECK
def E7(node, ):

    if node.production == Production.bystr("E7->E7@F7@E8"):
        t1, e1, l1 = E7(node.next[-1])
        t2, e2, l2 = E8(node.next[-3])
        if t1.name == t2.name:
            t = t1
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            return t, e, l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E7->E8"):
        t, e, l = E8(node.next[0])
        return t, e, l

# CHECK
def E8(node, ):
    if node.production == Production.bystr("E8->E8@F8@E9"):
        t1, e1,l1 = E8(node.next[-1])
        t2, e2,l2 = E9(node.next[-3])
        if t1.name == t2.name:
            t = Type('int')
            e = smb_t.random_insert(t)
            nasm.add(node.next[-2].next[0].val.val, e1, e2, e)
            return t,e,l1+l2+1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))
    elif node.production == Production.bystr("E8->E9"):
        t, e, l = E9(node.next[0])
        return t, e, l

# CHECK
def E9(node, ):
    if node.production == Production.bystr("E9->E10@F9_1"):
        t, e, l = E10(node.next[-1])
        nasm.add(node.next[-2].next[0].val.val, e, None, e)
        return t, e, 1+l

    # TODO：取地址 & 取值 & 取自身
    elif node.production == Production.bystr("E9->F9_2@E10"):
        t, e, l = E9(node.next[0])
        nasm.add(node.next[-1].next[0].val.val, e, None, e)
        return t, e, 1+l
    
    elif node.production == Production.bystr("E9->F9_1@E10"):
        t, e, l = E10(node.next[-2])
        nasm.add(node.next[-1].val.val, e, None, e)
        return t, e, l+1
    
    elif node.production == Production.bystr("E9->E10"):
        t, e, l = E10(node.next[0])
        return t, e, l

# 不写这个！！
def E10(node, ):
    if node.production == Production.bystr("E10->E10@[@E10@]"):
        t1 = E10(node.next[-1])
        t2 = E10(node.next[-3])
        if t2.TYPE == 'int' and t1.TYPE.name == 'pointer':
            return t
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))

    # TODO：取地址 & 取值 & 取自身
    elif node.production == Production.bystr("E10->E"):
        t, e, l = E(node.next[0])
        return t, e, l

# TODO id(E) 
def E(node, ):
    # 'E->(@E1@)|id|NUM|STR|id@(@E1@)',
    if node.production == Production.bystr("E->(@E1@)"):
        t, entry, l = E(node.next[-2], )
        return t, entry, l
    elif node.production == Production.bystr("E->id"):
        # try:

        #     entry = smb_t.find(node.next[0].val.val)[0]
        #     return entry.type_, entry, 0
        # except:    
        #     raise Exception("{}, {}".format(node.next[0].val.val, node.next[0].val.pos))
        entry = smb_t.find(node.next[0].val.val)[0]
        return entry.TYPE, entry, 0
    
    elif node.production == Production.bystr("E->NUM"):
        if '.' in node.next[0].val.val:
            t = Type('float', type_ = 'constant')
        else:
            t = Type('int', type_ = 'constant')
        e = smb_t.random_insert(t)
        nasm.add('=', e, node.next[0].val.val, None)
        return t, e, 1
    
    elif node.production == Production.bystr("E->false"):

        t = Type('boolen', type_ = 'constant')
        e = smb_t.random_insert(t)
        nasm.add('=', e, node.next[0].val.val, None)
        return t, e, 1
    
    elif node.production == Production.bystr("E->true"):

        t = Type('boolen', type_ = 'constant')
        e = smb_t.random_insert(t)
        nasm.add('=', e, node.next[0].val.val, None)
        return t, e, 1

    elif node.production == Production.bystr("E->STR"):
        return Type('void'), None, 0

    # TODO 增加函数语义
    elif node.production == Production.bystr("E->id@(@E_dot_exp@)"):
        # param_type -> [Type, Type, ...]
        param_num, param_type, list, l = E_dot_exp(node.next[-3], )
        

        func, _ = smb_t.find(node.next[-1].val.val)
        t = None
        if isinstance(func.TYPE, FuncType) and param_num == 0:
            t = func.TYPE.return_type
            return t, None, 0
        # TODO： 这里涉及了如何 check 参数 和 类型， 这里我们需要定义 X 运算， 暂时不实现
        elif isinstance(func.TYPE, FuncType) and param_num == func.TYPE.param_num and func.TYPE.equal(param_type):
            t = func.TYPE.return_type
            return t, None, 0
        else:
            raise Exception("{} type error in line {}".format(node.next[-1].val.val, node.next[-1].val.pos))

    elif node.production == Production.bystr("E->(@E2@)"):
        t, entry, l = E2(node.next[-2], )
        return t, entry, l
    elif node.production == Production.bystr("E->"):
        return Type('void'), None, 0
    else:
        # print(node.production)
        raise Exception("No match production!")

# CHECK
def state(node, offset):
    n, width, l = 0, 0, 0
    if node.production == Production.bystr("state->complex_sentence"):
        n, width, l = complex_sentence(node.next[0], offset)
        
    elif node.production == Production.bystr("state->sentence"):
        n, width, l = sentence(node.next[0], offset)
    return n, width, l

# CHECK
def if_sentence(node, offset):
    # 'if_sentence -> if@(@E1@)@state@else@state|if@(@E1@)@state'
    n, width = 0, 0
    if node.production == Production.bystr("if_sentence -> if@(@E2@)@state@else@state"):
        t, e, l0 = E2(node.next[-3])
        if t.name == 'boolen':
            # -5-7

            nasm.add('if_not_go', e, 'k+l1+2', None)
            n1, w1, l1 = state(node.next[-5], offset)
            nasm.add('go', 'k+l1+l2+2', None, None)
            n2, w2, l2 = state(node.next[-7], offset + w1)
            
            # 由于 k+l1+l2+2 = index -->  k  = index - l1 - l2 -2
            # line1 = k, line2 = k+ l1 + 1
            # line1 = index - l1 - l2 -2, 
            # line2 = index - l2 - 1
            nasm[nasm.index - l1 - l2 - 2].arg2 = nasm.index - l2
            nasm[nasm.index - l2 - 1].arg1 = nasm.index

            n = n1 + n2
            width = w1 + w2
            return 0, 0, l1 + l2 + l0 + 2
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))

        
        
    elif node.production == Production.bystr("if_sentence -> if@(@E2@)@state"):
        t, e, l0 = E2(node.next[-3])
        if t.name == 'boolen':
            # -5-7
            nasm.add('if_not_go', e, 'k+l1+1', None)
            n, width, l = state(node.next[-5], offset)
            nasm[nasm.index - l - 1].arg2 = nasm.index

            return 0, 0, l + l0 + 1
        else:
            raise Exception("type error in line {}".format(node.next[0].val.pos))

    # 虽然有 变量数量和宽度， 但是在作用于结束的时候可以释放所以返回宽度不算


# CHECK
def for_sentence(node, offset):
    # 'for_sentence-> for@(@loop_control_sentence@loop_control_sentence@loop_control_sentence@)@complex_sentence
    #                 for@(@loop_control_sentence@)@sentence',
    # 此处由于 for 语句中可能有 变量声明， 所以一个 for 语句实际是两个 嵌套作用域
    smb_t.insert(Record('Enter for loop'))
    smb_t.location()

    n1, w1, l1 = E1(node.next[-3])
    offset += w1
    loop_start = nasm.index

    t, e, l2 = E2(node.next[-4])

    nasm.add('if_not_go', e, 'index', None)
    
    
    if node.production == Production.bystr("for_sentence-> for@(@E1@;@E2@;@E1@)@complex_sentence"):
        # -3-4-5-7
        
        n4, w4, l4 = complex_sentence(node.next[-7], offset)

    elif node.production == Production.bystr("for_sentence-> for@(@E1@;@E2@;@E1@)@sentence"):

        n4, w4, l4 = sentence(node.next[0], offset)
    
    n3, w3, l3 = E1(node.next[-5])
    nasm.add('go', loop_start, None, None)
    

    nasm[nasm.index - l3 - l4 - 1 - l2].arg2 = nasm.index




    n, w = n1+n3+n4, w1+w3+w4
    smb_t.relocation()
    return 0, 0, l1+l2+l3+l4+2




# CHECK
def while_sentence(node, offset):
    # while_sentence->while@(@E2@)@state
    start = nasm.index
    t, e, l1 = E2(node.next[-3])
    if t.name == 'boolen':
        nasm.add('if_not_go', e, 'index', None)
        n, w, l2 = state(node.next[-5], offset)
        nasm.add('go', start, None, None)
        print(l1,l2)
        nasm[nasm.index - l2 - 2].arg2 = nasm.index

    else:
        raise Exception("type error in line {}".format(node.next[0].val.pos))
    return 0, 0, l1+l2+2


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
