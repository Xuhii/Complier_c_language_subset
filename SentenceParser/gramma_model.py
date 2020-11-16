# 文法 G 4—6
# 使用 一个符号代替 S'
# 或者应该用什么来代替 文法符号， 每一个符号应该被区别对待 而不是简单德当作字符， 所以我们需要一个类来解析每一个符号 ？
# 所以应该为所有的符号定义， 区别 终结符 和 非终结符号
# 文法符号之间使用@区分， 空格也算符号
# · 符号两边分割为两个expression， 而 其中每个expression都以@分割语法符号


# 由于对于终结符而言， 一个符号可能代表了一类输入我们如何判断他们呢
# 判断两个 token 是否相等
# 1. 优化输入， 终结符可以写成以$符号分割的序列， 定义终结符列表
# 2. 在读入序列的时候判断这个序列是什么类型， 为 Symbol 类增加一个 val 字段， 存入当前符号 
# 
G_4_6 = [
    'S -> a@A',
    'S -> b@B',
    'A -> c@A',
    'A -> d',
    'B -> c@B',
    'B -> d',
]
# Nonfinal = set(['S','A','B'])

G_closure_test = [
    'S_ -> ·S',
]

G_4_4 = [
    'S -> T@E_',
    'E_ -> +@T@E_',
    'E_ -> e_',
    'T -> F@T_',
    'T_ -> *@F@T_',
    'T_ -> e_',
    'F -> (@S@)',
    'F->id'
]
# Nonfinal = set(['S','E_','T', 'T_', 'F'])

G_4_4_R = [
    'S -> S@+@T',
    'S -> T',
    'E -> e_',
    'T -> T@*@F',
    'T -> F',
    'F -> (@S@)',
    'F->id'
]
# Nonfinal = set(['S','T' ,'E', 'F'])

G_SLR_test = [
    'S -> B@A',
    'S -> A@B',
    'A -> a@B',
    'A -> c',
    'B -> a@D@A',
    'B -> d',
    'D->f'
]

G_LR_test = [
    'S -> C@C',
    'C -> c@C',
    'C -> d',
]
# 默认在非终结符号中算上
# Nonfinal = set(['E', 'E_', 'T', 'T_', 'F'])
# Nonfinal = set(['S', 'A', 'B','S_'])


# Nonfinal = set(['S', 'A', 'B','S_', 'D','C', ])

G_CC = [
    'S -> K@V@N@;',

    'N -> =@E',
    'N -> e_',

    'E -> E@F@E',
    'E -> V',

    'F -> +',
    'F -> -',
    'F -> *',
    'F -> /',

    'K -> int',
    'K -> float',


    'V -> v',
    'V -> a',
    'V -> b',
    'V -> c',
    'V -> d',
]

G_e__test = [
   'S->a@S|e_',
]
# Nonfinal = ['S']
# 所有非终结符 都是用字母表示
G_Expression = [
    'S -> E',
    'E -> E@FH@T',
    'E -> T',
    
    'T -> T@FH@F',
    'T -> F',

    'F -> (@E@)',
    'F -> id',
    'FH->+',
    'FH->-',
    'FH->*',
    'FH->/',
    'FH->*',
    'FH->/',
    'FH-> >',
    'FH-> =',

]

# Nonfinal = set(['S', 'E','F', 'T', 'FH'])

# 4_4
# Nonfinal = set(['S','E_','T', 'T_', 'F'])

G_IF_ELSE_TEST={
    'S->B@S',
    'S->B',
    'B->if@(@E@)@E@;',
    'B->if@(@E@)@{@S@}',
    'B->if@(@E@)@{@S@}@else@{@S@}',
    'B->if@(@E@)@{@S@}@else@E@;',

    'B->if@(@E@)@E@;@else@{@S@}',
    'B->if@(@E@)@E@;@else@E@;',
    'B->E@;',
    
    'E -> E@FH@T',
    'E -> T',
    'T -> T@FH@F',
    'T -> F',
    'F -> (@E@)',
    'F -> id',

    'FH->+',
    'FH->-',
    'FH->*',
    'FH->/',

    'FH-> >',
    'FH-><',
    'FH->=',
    'FH->*=',
}
# Nonfinal = ['S','E', 'T', 'F', 'FH', 'B']




G_CC = [
    # sentence
    'S->sentence_list',
    'sentence_list->sentence@sentence_list|sentence|e_',
    'sentence-> func_declare|func_define|if_sentence|for_sentence|while_sentence|go_sentence|expression_sentence|type_declare_sentence|complex_sentence',
    'go_sentence->CONTINUE@;|BREAK@;|RETURN@;|RETURN@expression@;',
    'complex_sentence->{@sentence_list@}',

    # if else while for
    'state->complex_sentence|sentence',
    'if_sentence -> if@(@E1@)@state@else@state|if@(@E1@)@state',
    'for_sentence-> for@(@loop_control_sentence@loop_control_sentence@loop_control_sentence@)@complex_sentence|for@(@loop_control_sentence@)@sentence',
    'loop_control_sentence->expression_sentence|type_declare_sentence',

    'while_sentence->while@(@expression@)@state',

    # 定义expressionsentence
    # 数字越大优先级越大
    # 暂时不实现位运算
    'expression_sentence->E1@;',
    'F1->+=|-=|*=|/=|%=|<<=|>>=|=',
    'F2->or',
    'F3->and',
    'F4->!=|==',
    'F5-><=|<|>=|>',
    'F6-><<|>>',
    'F7->+|-',
    'F8->*|/|%',
    'F9_1->++|--',
    'F9_2->-|*|&',

    

    'E1->E1@F1@E2|E2',
    'E2->E2@F2@E3|E3',
    'E3->E3@F3@E4|E4',
    'E4->E4@F4@E5|E5',
    'E5->E5@F5@E6|E6',
    'E6->E6@F6@E7|E7',
    'E7->E7@F7@E8|E8',
    'E8->E8@F8@E9|E9',
    # 这里的优先级是选 E9还是E10
    'E9->E10@F9_1|F9_2@E10|F9_1@E10|E10',
    'E10 -> E10@[@E10@]|E11',
    'E11->E11@,@E|E',
    'E->(@E1@)|id|NUM|STR|id@(@E1@)',


    # 函数
    'func_declare->type_statement@id@parameter_list@;',
    'func_define->type_statement@id@parameter_list@complex_sentence',
    'type_statement->int|float|void|char',

    'parameter_list->(@list@)',
    'list->list@,@parameter|parameter',
    'parameter->type_statement@id|type_statement',

    # 声明 + 初始化语句 type_declare_sentence
    'type_declare_sentence->type_statement@id_list@initialize@;',
    'initialize->=@E1|e_',
    'id_list->id@,@id_list|id',
]

Nonfinal = []