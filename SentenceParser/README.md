##### 一 语法分析方法

1. 自顶向下分析  eg.预测分析
2. 自底向上分析  eg.LR分析

/* 都是从左往右每次读入一个记号 */

##### 二 错误处理

**目标**

1. 词法错误

   在词法分析阶段将错误词法标记， 规定发生词法错误将不会进入语法分析阶段

2. 语法错误

   表达式括号不匹配， 缺少运算对象。。

3. 语义错误
4. 逻辑错误

**错误**

1. 错误位置
2. 错误性质（这个不知道怎么判断
3. 跳过错误--->顺利检查后边的错误（在词法分析已经实现了
4. 错误处理不会带来太多的系统开销

**错误恢复**

1. 紧急恢复
2. 短语级恢复
3. 出错产生式（先验错误
4. 全局纠正

# 自顶向下分析方法

面向目标分析

如果是文法的一个句子， 那么通过产生式推导就可以得到分析树

如果不是就抛出错误

* 确定
* 不确定

自顶向下分析的本质是穷举法， 消除回溯是算法的关键。 

##### 递归下降法


/* 由于 python 开发效率高 之后可以用 c/c++进行重构  */


<!-- 代码 安排 如下 -->
* 由于set集合无法通过 访问产生式左端访问 产生式可以使用dict()代替， 但是不清楚后续会遇到的问题， 所以之后遇到问题再重构
* 11.8 实现SLR 表的构造 ， 记录实现中的缺陷
   * 计算机内部的 repr 应该使用以 @ 分割的形式， 而 str 应该使用 以空格区分的形式？这其实不好解决， 内部既然使用了 list 作为存储就不应该改变了， 而应该添加构建左部和右部的新的构造函数
   * 实现了多叉树作为输出方式， 着手构建多叉树的 ascii 展示方法


ToDo: 11.9
* 完成最基本的分析器类和 Run 方法：按优先级实现
   1. 分析表类(由 正规项目集簇构造 构建)， 而分析表需要可以：
            1. 不同实现(LR(1), LR(1)) ：继承分析表类
            2. 但是需要 统一接口 ： 抽象必须的接口
            3. 使用一个 正规项目集蹙初始化该表： 多初始化函数
            4. 确定存储类型 字典 二维数组？？等等
   2. 输入序列类， 它可以由文件或者py文件 读入输入序列： 需要实现：
            1. get 方法
            2. top 方法
            3. 序列的每一个元素是一个 symbol 对象， 栈底是 $
            4. 需要重载不同的构造函数（init 函数需要是最基本的， 与存储格式最适合的）
   3. 分析器 run 方法的输出是产生式序列， 需要使用 TreeNode 类构建语法树并且展示
            1. run 方法照着写， 但是是否是每一个表的run方法都一样还不知道， 到时候看
            2. 产生式序列作为输出的结果
            3. 做一个 toTree 函数， 将输出结果转化为 TreeNode


TODO:
1. 为 Production 类添加 first 集合和 follow 集合的构造方法

```c
文法: 
{[S -> B A], [B -> d], [S_ -> S], [A -> c], [B -> b A], [A -> a B], [S -> A B]}

输入: b c a b a d

归约方式:
      S              
      |              
  :--------:         
  B        A         
  |        |         
:---:   :------:     
b   A   a      B     
    |          |     
    :       :-----:  
    c       b     A  
                  |  
                :---:
                a   B
                    |
                    :
                    d
```