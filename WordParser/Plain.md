### To  realization the Complier

1. 借鉴 python 的词法分析器

   <img src="C:\Users\herrn\AppData\Roaming\Typora\typora-user-images\image-20200930112038844.png" alt="image-20200930112038844" style="zoom:50%;" />

   观察 python 的 tokenize 模块对程序的处理， 类似的我们也采用真样的5元组表示一个 token：

   `   (start_pos, end_pos, type, content)​   `

   

2. 思路 
   * 利用正则表达式描述
   * 正则表达式转换为正则文法
   * 构建有限自动机
3. 问题化简和分解
   * 对于给定的语言子集可以手动构造自动机
   * 可以根据正规式，先构造NFA， DFA， 再构造自动机
   * 那我们首先实现手动构造自动机， 再实现自动构造自动机， 其中必须实现的是自动机类





4. 步骤
   * 定义自动机类
   * 手动构造状态转换矩阵
   * 实现自动构造状态转换矩阵的方法（ 未实现 ）

 