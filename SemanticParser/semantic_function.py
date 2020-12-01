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
    
    @staticmethod
    def S(node):
        getattr(SemanticFunctionSet,"sentence_list")(node.next[-1])
    
    @staticmethod
    def sentence_list(node):
        getattr(SemanticFunctionSet,"sentence")(node.next[-1])
    
    @staticmethod
    def sentence(node):
        getattr(SemanticFunctionSet,"type_declare_sentence")(node.next[-1])
    
    @staticmethod
    def type_declare_sentence(node):
        TYPE = getattr(SemanticFunctionSet,"type_statement")(node.next[-1])
        getattr(SemanticFunctionSet,"id_list")(node.next[-2], TYPE)
        

    @staticmethod
    def type_statement(node):
        return node.next[0].val.name
    
    @staticmethod
    def id_list(node, TYPE):

        print("ADD TO SYMBOL TABLE: <{}, {}>".format(node.next[-1].val.val, TYPE))
        if len(node.next) == 3:
            getattr(SemanticFunctionSet,"id_list")(node.next[0], TYPE)
    


if __name__ == "__main__":
    getattr(SemanticFunctionSet,"test_demo")(1,2,3)