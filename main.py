import os
from SentenceParser.lr_analyze_driver_model import s_parser
# from SentenceParser.gramma_model import G_CC
from WordParser.word_parser import w_parser
from SentenceParser.token_stack_model import *
from SemanticParser.semantic_function import *
# s_parser(G_Expression,"( a + b ) * c + d", 'slr')



# 我们可以发现含有 e_ 的文法转化为不含 e_ 的文法就好哦了

# string = 'if ( ( id * id > id + id ) ) { if ( id > id ) id * id ; id = id ; id *= ( id + id ) ; }'
# s_parser(G_IF_ELSE_TEST,string, 'slr')

# e_ test
# s_parser(G_e__test, 'a a a a a a a', 'lr')
# s_parser(G_e__test, 'a a a a a', 'slr')
# string = 'if ( id + id ) id * id ;'
# s_parser(G_CC, string, 'slr', debug=True)
def write(filename, data):
    with open(filename, 'w') as f:
        f.write(data.__str__())

w = w_parser('/home/ubuntu/Workplace/Complier/WordParser/source/light.c')
# w = w_parser('/home/ubuntu/Workplace/Complier/WordParser/source/demo.c')

root_node, table = s_parser(G_CC, w.check(), 'slr')

# 输出
if not os.path.exists('out'):os.makedirs('out')
write('out/token.out', w)
write('out/tree.out', root_node)
write('out/table.out', table)


# 测试 简单语义分析
SemanticFunctionSet.S(root_node)