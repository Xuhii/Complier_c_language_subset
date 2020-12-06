# C 语言子集的编译器

### 项目介绍

*参考书籍：《编译原理与技术 第二版》*

该项目是在 《编译原理》课程学习的实践项目。

因此，会存在很多早前代码没考虑到后续复用， 或者未提供友好接口的情况， 显得过于杂乱。 但是总体还是依据  `词法分析`  -> `语法分析` -> `类型检查`  -> `目标代码生成 `  的多遍遍历方式

由于时间关系， 并未做代码优化相关功能。

### 功能实现

* 词法分析
  
  - [x] 为词法 构造状态机
  - [ ] 实现由文法自动构建状态机的方法
  - [ ] 优化一些莫名其妙的的操作和bug（毕设做完后会修改
  
* 语法分析

  输入：token 序列

  输出：分析树(多叉树)， 其中非终结符处于非叶节点

  - [x] 实现分析树的Ascii打印
  - [x] 构建LR/SLR分析表
  - [x] 设计文法
  - [x] 实现LR语法分析程序
  - [ ] 图形化界面的输出
  - [ ] 优化文法集合的设计（目前有些冗余）
  - [ ] 优化各个类的实现（目前有些杂乱）

* 类型检查

  *声明类型， 表达式类型， 语句类型*

  * [x] 通用语法制导翻译
  * [x] 为每个非终结符编写语义（类型检查语义）
  * [x] 实现符号表（栈式哈希表）
  * [ ] 设计类型表达式 及 相关接口
  * [ ] 优化语义的组织方式
  * [ ] 实现类型重载相关语义
  * [ ] 实现强制类型转换相关语义

* 目标代码生成
  - [ ] 暂无

### 使用方式

**运行程序**

```bash
# 将代编译文件放入 Complier/WordParser/source
python Complier/main.py [filename]
```



**查看结果**

```bash
# 输出文件在 ls Complier/out/
# 查看输入 token （词法分析结果）
cat Complier/out/token.out
# 查看分析树 （语法分析结果）
cat Complier/out/tree.out
# 查看分析表 （语法分析结果）
cat Complier/out/table.out
```

