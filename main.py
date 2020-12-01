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


w = w_parser('/home/ubuntu/Workplace/Complier/WordParser/source/compute.c')
# w = w_parser('/home/ubuntu/Workplace/Complier/WordParser/source/demo.c')

print(w)
root_node = s_parser(G_CC, w.check(), 'slr')
# 绘制分析树
print(root_node)


# 测试 简单语义分析
SemanticFunctionSet.S(root_node)

