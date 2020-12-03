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

G_CC = [
    # sentence
    'S->sentence_list',
    'sentence_list->sentence@sentence_list|sentence|e_',
    'sentence-> func_define|if_sentence|for_sentence|while_sentence|go_sentence|expression_sentence|type_declare_sentence|complex_sentence',
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
    'F_dot_exp->,',
    'F2->or',
    'F3->and',
    'F4->!=|==',
    'F5-><=|<|>=|>',
    'F6-><<|>>',
    'F7->+|-',
    'F8->*|/|%',
    'F9_1->++|--',
    'F9_2->-|*|&',

    

    'E1->E1@F1@E_dot_exp|E_dot_exp',
    'E_dot_exp->E_dot_exp@F_dot_exp@E2|E2',

    'E2->E2@F2@E3|E3',
    'E3->E3@F3@E4|E4',
    'E4->E4@F4@E5|E5',
    'E5->E5@F5@E6|E6',
    'E6->E6@F6@E7|E7',
    'E7->E7@F7@E8|E8',
    'E8->E8@F8@E9|E9',
    # 这里的优先级是选 E9还是E10
    'E9->E10@F9_1|F9_2@E10|F9_1@E10|E10',
    'E10->E10@[@E10@]|E',
    # 'E11->E11@,@E|E',
    'E->(@E2@)|id|NUM|STR|id@(@E_dot_exp@)|e_',


    # 函数
    # 'func_declare->type_statement@id@(@list@)@;',
    'func_define->type_statement@id@(@list@)@complex_sentence',
    'type_statement->int|float|void|char|boolen',

    'list->list@,@parameter|parameter',
    
    'parameter->type_statement@id|type_statement',

    # 声明 + 初始化语句 type_declare_sentence
    'type_declare_sentence->type_statement@id_list@initialize@;',
    'initialize->=@E1|e_',
    'id_list->id@,@id_list|id',
]
# 非终结符 列表/字典 在载入时生成
Nonfinal = []