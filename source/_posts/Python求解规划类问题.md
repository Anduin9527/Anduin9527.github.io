---
title: Python求解规划类问题
tags:
  - 笔记
  - 数学
  - Python
category: 数学建模
katex: true
abbrlink: d7cb7c5c
date: 2022-06-29 23:08:00
---

## 前言

摸鱼，等崛起的神威太刀。

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/%E6%B3%A1%E5%A3%B6%E9%BE%99%E5%A4%AA%E5%88%80.jpg" alt="89249011_p1_master1200" style="zoom: 67%;" />

<!--MORE-->

## 线性规划

**生产问题，投料问题**

线性规划求解需要确定目标函数（$max，min$）和约束条件（$s.t.$）

求解前应该转为标准形式，即不等式约束，等式约束以及范围约束：
$$
\min \mathrm{c}^{T} x \\
\begin{equation}
\text { s.t. }\left\{\begin{array}{c}
A x \leq b \\
A e q * x=b e q \\
l b \leq x \leq u b
\end{array}\right.
\end{equation}
$$

+ $c^T$为目标函数系数**向量**
+ $A$为不等式组系数**矩阵**，$b$为不等式组常数**向量**
+ $Aeq$为等式组系数**矩阵**，$beq$为等式组系数**向量**
+ $lb,ub$为下界和上界**向量**

```matlab
[x,fval] = linprog(c, A, b, Aeq, beq, lb, ub, X0)
```

+ 标准形式为求解最小值，如果求解最大值等价于求$-\min \mathrm{c}^{T} x$的最小值，最后结果再给个相反数即可

+ 标准形式的不等式为**小等于**

+ `x` 为最小值的系数**向量**，`fval `为最小值
+ `X0`为迭代初值，可省略



```python
from scipy import optimize
import numpy as np

def LinearProgram(c, A, b, Aeq, beq, bounds=None):
  # 求解函数
  res = optimize.linprog(c, A, b, Aeq, beq, bounds)
  # 目标函数最小值
  print(res)
  # 最优解
  print(res.x)
```

+ 标准形式为求解最小值，如果求解最大值等价于求$-\min \mathrm{c}^{T} x$的最小值，最后结果再给个相反数即可
+ 标准形式的不等式为**小等于**
+ 无上下界约束为默认值
+ `bounds`为二元组列表，每个二元组对应一个$x$的下界和上界，无限制则为`None`

![线性规划例子](https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220421172003.png)

## 整数规划

### 线性整数规划

**钢管切割问题**

在线性规划的基础上，加入决策变量为整数的条件

整数规划求解的基本框架是**分支定界法**（Branch and bound，BnB）

首先去除整数约束得到“**松弛模型**”，使用线性规划的方法求解。若有某个变量不是整数，在松弛模型上分别添加约束

但是`python`实现分支定界较为繁琐，所以选择使用`Plup`这个专门用来解线性规划问题的库

```matlab
[x,fval] = intlinprog(c, intcon, A, b, Aeq, beq, lb, ub)
```

+ `intcon`为一个**向量**，指定那些决策变量是整数

### 0-1规划

**背包问题，指派问题** 

特殊的线性整数规划，即决策变量只取0或者1

显然，只需要对线性整数规划的上下界进行约束即可

### Plup

>真好用啊，符合人类直觉的限制方式
>
>Pulp本质上是求解器的接口，具体的求解是依赖优化器实现的

1. 定义一个规划问题类`LpProblem`

```python
myProb = pulp.LpProblem("ProblemName", sense=pulp.LpMaximize)
```

+ `sense`可为：`LpMinimize` `LpMaximize`对最小值问题和最大值问题

2. 定义决策变量`LpVariable`

```python
x1 = pulp.LpVariable('x1', lowBound=0, upBound=7, cat=pulp.LpConstraint) 
x2 = pulp.LpVariable('x2', lowBound=0, cat=pulp.LpInteger)
x3 = pulp.LpVariable('x3', cat=pulp.LpBinary) 
```

+ 上下界缺省为无穷
+ `cat`设定变量类型，用于解决小数、整数以及0-1规划

3. 添加目标函数

```python
myProb += 2*x1 + 3*x2 - 5*x3				# 设置目标函数
```

+ 添加目标函数使用 “之前定义的规划问题类 += 目标函数式” 格式。

4. 添加约束条件

```python
myProb += 2*x1 - 5*x2 + x3 >= 10  # 不等式约束
myProb += x1 + 3*x2 + x3 <= 12  	# 不等式约束
myProb += x1 + x2 + x3 == 7  			# 等式约束
```

+ 约束式只能为`==` `>=` `<=`

5. 求解

```python
myProb.solve()
# myProb.solve(pulp.GUROBI_CMD())
print("求解状态:", pulp.LpStatus[myProb.status])
for v in myProb.variables():
  print(v.name, "=", v.varValue)
print("目标值=", pulp.value(myProb.objective))
```

+ PuLP默认采用 CBC 求解器来求解优化问题
+ 可以调用其它的优化器来求解，如：GLPK，COIN CLP/CBC，CPLEX，和GUROBI，但需要另外安装。

### CvxPY

>支持较多变量需要用到矩阵乘法的规划问题

1. 定义系数矩阵

```python
C = np.array[()]
A = np.array[()]
B = np.array[()]
```

2. 声明决策变量

```python
x = cp.Variable(n,integer = True)
```

+ $n$为变量长度
+ 可以声明决策变量类型
  + `neg pos nonneg nonpos`：负数 正数 非负数 非正数
  + `boolean`：布尔变量

3. 声明问题

```python
objective = cp.Minimize(cp.sum(C*x))
```

+ `Minimize`和`Maximize`

4. 定义约束

```python
# 开始拼接约束方程
# B是右边的常数项
B = np.concatenate((B1, B2, B3, B4, B5))
# print(B)
# A是左边的约束项
A = np.vstack([A1, A2, A3, A4, A5])
# print(A)
# Be是右边的等式约束项
Be = np.concatenate((Be1, Be2,Be3,Be4,Be5))
# print(Be)
# Ae是左边的等式约束项
Ae = np.vstack([Ae1, Ae2,Ae3,Ae4,Ae5])
```

5. 定义求解器

```python
constraints = [Ae @ x == Be, A @ x >= B]
prob = cp.Problem(objects, constraints)
prob.solve(solver=cp.GUROBI)
print("Status:", prob.status)
print("Optimal value", prob.value)
print("Optimal var\n", x.value.reshape())
```



## 非线性规划

如果目标函数或者约束条件存在非线性函数，即为非线性规划情况
$$
\min \mathrm{c}^{T} x \\
\begin{equation}
\text { s.t. }\left\{\begin{array}{c}
A x \leq b \\
A e q * x=b e q \\
C(x) \leq 0 \\
Ceq(x) =0 \\
l b \leq x \leq u b
\end{array}\right.
\end{equation}
$$


不难发现，比起线性规划的标准形式，非线性规划多了**非线性不等式约束**$C(x) \leq 0$以及**非线性等式约束**$Ceq(x)=0$

+ $c^T$为目标函数系数**向量**

+ $C(x)$为非线性函数**向量**

+ $Ceq$为非线性函数向量

![非线性规划例子](https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220422103411.png)

```matlab
[x, fval] = fmincon(@fun, X0, A, b, Aeq, beq, lb, ub, @nonlfun, OPTION)
```

+ 算法本身求取的是局部最优，所以预期的初始值`X0`非常重要
+ 如果要求全局最优：
  + 给定不同的初始值，得到“全局最优解”
  + 先用蒙特卡罗模拟，将该解作为初始值来求取最优解（推荐）
+ `OPTION`可以指定使用的求解算法，**通过改变算法，可以体现你的模型稳定性**
+ `@fun`和`@nonlfun`需要用额外的`.m`文件定义

非线性规划可以依据目标函数类型简单分为两种，凸函数和非凸函数

+ 凸函数可以使用`cvxpy`库
+ 非凸函数没有特定的算法可以尝试寻找极值：
  + 纯数学
  + 神经网络，深度学习
  + `scipy.optimize.minimize`
  + `gekko`

### SciPy optimize 

>与matlab一样，需要定义目标函数以及约束条件

目标函数

```python
def objective(args):
  '''
  args 为决策变量的系数向量
  '''
  a, b, c, d = args
  def v(x): return a*x[0] * d*x[3] * (a*x[0] + b*x[1] + c*x[2]) + c*x[2]
  return v
```

约束条件

```python
def constraints(args):
  '''
  args 为约束条件的常数向量
  '''
  eq1, ineq1 = args
  cons = (
      {'type': 'ineq', 'fun': lambda x: x[0] * x[1] * x[2] * x[3] - ineq1},
      {'type': 'eq', 'fun': lambda x:
       x[0]**2 + x[1]**2 + x[2]**2 + x[3]**2 - eq1}
  )
  return cons
```

+ `type`有`ineq, eq`分别表示不等式约束和等式约束类型
+ 最后记得减去常数以保证形式都为0
+ 注意：在`optimize.minimize`中的**不等式约束标准形式为大等于**，与`optimize.linprog`相反

求解

```PYTHON
res = minimize(objective(objargs), X0, method='SLSQP',
							bounds=bounds, constraints=constraints(conargs))
```

+ 算法本身求取的是局部最优，所以预期的初始值`X0`非常重要
+ `method`可选多种算法

### Gekko

>与Pulp语法比较接近，属于人类直觉型库

1. 初始化

```python
from gekko import GEKKO

m = GEKKO(remote=False) 
# 指定求解器
m.options.SOLVER = 3
```

2. 定义决策变量

```python
x1 = m.Var(lb=1, ub=5)
x2 = m.Var(lb=1, ub=5)
x3 = m.Var(lb=1, ub=5)
x4 = m.Var(lb=1, ub=5)
```

3. 定义约束条件

```python
m.Equation(x1 * x2 * x3 * x4 >= 25)
m.Equation(x1**2 + x2**2 + x3**2 + x4**2 == 40)
```

4. 定义目标函数

```python
m.Obj(x1 * x4 * (x1 + x2 + x3) + x3)
```

5. 求解

```python
# 指定优化器
m.options.IMODE = 3

# 求解
m.solve(disp=False)  # Solve
# 输出结果
print('x1 = ', x1.value)
print('x2 = ', x2.value)
print('x3 = ', x3.value)
print('x4 = ', x4.value)

print('Objective: ' + str(m.options.objfcnval))
```