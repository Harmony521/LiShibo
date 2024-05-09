<p align="center"><img src="./images/logo.png" alt=""></p>
<h1 align="center">基于Grover量子搜索算法的布尔方程组求解🌌</h1>
<p align="center">使用Grover算法解决布尔方程组.</p>


# 目录
- [目录](#目录)
- [介绍](#介绍)
	- [文件结构](#文件结构)
	- [算法简介](#算法简介)
		- [方程组生成算法](#方程组生成算法)
		- [grover算法](#grover算法)
- [用法](#用法)
- [使用非本程序格式的方程组](#使用非本程序格式的方程组)

# 介绍

语言：Python
量子计算框架：Qiskit
运行环境：曙光计算云
功能：求解n变元布尔方程组（受限）

**布尔方程组表示形式：**
使用 二维列表 存储布尔方程组中的方程
使用 元组 表示两个元素相乘
使用 一维列表 存储布尔方程组中方程的值
如：
[ [1, 2], [(1,2)] ]
[0, 1]
表示布尔方程组:
x1 + x2 = 0
x1 * x2 = 1

**整体思路：**
1. 生成随机布尔方程组
2. 暴力穷举布尔方程组判断是否有解，选择有唯一解的布尔方程组
3. 用量子算法求解有唯一解的布尔方程组
4. 判断解的情况以及画出电路图


## 文件结构

- BoolEquations.py
随机生成与优化布尔方程组算法实现
- Grover.py
Grover算法电路实现
- SolveEquations.py
求解布尔方程组完整代码

## 算法简介

### 方程组生成算法

- 随机生成方程组
- 优化
- 经典破解
- 无解情况
- 多解情况

### grover算法

- oracle生成

# 用法

进入曙光计算云，将本项目文件夹复制过来
```sh
module load apps/anaconda3/5.2.0
source activate qiskit-py3 
cd SolveEquations/
python solvequations.py
```
- 程序提醒输入变元数量
- 生成方程组，代码内部进行优化与经典破解，最终打印具有唯一解的方程组及其解
- 根据方程组运行grover算法，对方程组进行量子求解
> 如需画图可取消solvequations.py中最后一行注释

# 使用非本程序格式的方程组

需将方程组的**格式**转换成符合本程序的格式，并将其赋值给BoolEquations类中的 eq_set 和 eq_value ，使用run_other()函数进行优化与经典破解。

例如，以下是部分代码
```python
	equations = BoolEquations(num_variable)
	equations.eq_set = [[x]]
	equations.eq_value = [x]
	eq_set, eq_value = equations.run_other()
```
