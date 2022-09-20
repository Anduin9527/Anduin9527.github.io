---
title: Games101-Transform
tags:
  - 计算机图形学
  - 笔记
category: Games101笔记
abbrlink: 918c829e
katex: true
date: 2022-09-20 19:00:00
---



## 前言

本文是对 [Game101](https://www.bilibili.com/video/BV1X7411F744?p=3) L3~L4 的笔记，阅读前请先保证对线性代数几何意义有着较为直观的理解，推荐配合食用 [3Blue1Brown-线性代数的本质](https://www.bilibili.com/video/BV1ys411472E)

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220920190945.jpeg" alt="img" style="zoom:80%;" />

<!--more-->

## 向量变换

空间的变换可以用 **基向量** 的变换来加以描述，这些基向量可以构成单位矩阵。换言之，通过一个矩阵我们就可以描述空间的变化

### 线性变换

利用指向 $x$ 轴正方向的的基向量 $\hat x$ 和指向 $y$ 轴正方向的基向量 $\hat y$，可以很容易的得出所谓的变换矩阵。而将一个向量左乘一个变换矩阵得到一个新向量的过程，因为其按照矩阵乘法展开式为线性运算形式
$$
v' = M v \\ \\
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime}
\end{array}\right]=\left[\begin{array}{ll}
a & b \\
c & d
\end{array}\right]\left[\begin{array}{l}
x \\
y
\end{array}\right]\\ \\
x' = ax+by \\
y' = cx+dy
$$
故称之为 **线性变换**

约定，以下的 $\hat x = \begin{pmatrix} 1 \\ 0  \end{pmatrix}$，$\hat y = \begin{pmatrix} 0 \\ 1  \end{pmatrix}$

#### 缩放 Scale

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919214655.png" alt="image-20220919214647983" style="zoom: 50%;" />

可以使用如下的公式
$$
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime}
\end{array}\right]=\left[\begin{array}{cc}
s_x & 0 \\
0 & s_y
\end{array}\right]\left[\begin{array}{l}
x \\
y
\end{array}\right]
$$
也可以直接观察两个基向量的变化情况，$\hat x' = \begin{pmatrix} s_x \\ 0  \end{pmatrix}$，$\hat y' = \begin{pmatrix} 0 \\ s_y  \end{pmatrix}$

然后将两个新的基向量 **拼合** 即可组成变换矩阵，以上内容后文不再赘述

#### 对称 Reflection

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919220419.png" alt="image-20220919220419759" style="zoom:50%;" />
$$
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime}
\end{array}\right]=\left[\begin{array}{cc}
-1 & 0 \\
0 & 1
\end{array}\right]\left[\begin{array}{l}
x \\
y
\end{array}\right]
$$

#### 剪切 Shear

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919221109.png" alt="image-20220919221109356" style="zoom:50%;" />
$$
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime}
\end{array}\right]=\left[\begin{array}{ll}
1 & a \\
0 & 1
\end{array}\right]\left[\begin{array}{l}
x \\
y
\end{array}\right]
$$

#### 旋转 Rotation

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919221229.png" alt="image-20220919221229457" style="zoom:50%;" />
$$
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime}
\end{array}\right]=\left[\begin{array}{ll}
\cos \theta & -\sin \theta \\
\sin \theta & \cos \theta
\end{array}\right]\left[\begin{array}{l}
x \\
y
\end{array}\right]
$$

### 仿射变换

#### 齐次坐标

> 由 August Ferdinand M ö bius 提出的齐次坐标（又称投影坐标，homogeneous coordinates），使图形和几何学的计算在投影空间中成为可能。齐次坐标是用 $N+1$ 个数来表示 $N$ 维坐标的一种方式

要制作齐次坐标，我们只需在现有坐标中增加一个额外的变量 $w$。具体而言，在齐次坐标中我们把 **点** 和 **向量** 的表示区别开

+ 将原本的向量$(x, y)^T$表示为$(x, y,0)^T$
+ 点则为$(x, y,1)^T$的形式

说了这么多，所以为什么要引入 **齐次坐标** 呢？

> 因为懒是一个一个一个美德。	by 闫令琪

你可以发现，上述线性变化矩阵中并没有熟悉的平移 Translation 的身影

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919223311.png" alt="image-20220919223311205" style="zoom:50%;" />

事实上，他也确实不能写作所谓线性变换的形式（因为原点的位置已经被改变了，而线性变化在几何上直观的特点就是：**原点不变** 以及 **直线在变换后依然为直线**），所以我们不得不写成以下形式
$$
\left[\begin{array}{l}
x^{\prime} \\
y^{\prime}
\end{array}\right]=\left[\begin{array}{ll}
a & b \\
c & d
\end{array}\right]\left[\begin{array}{l}
x \\
y
\end{array}\right]+\left[\begin{array}{l}
t_x \\
t_y
\end{array}\right]
$$
这种不统一的形式，显然令人不喜，于是乎引入了 **齐次坐标** 来解决平移的问题。又因为向量具有 **平移不变性**，所以我们将其的 $w$ 设置为 $0$。事实上，这种设置也确实有更多的实际意义，比如
$$
vector + vector = vector\\
point - point = vector\\
point + vector = point\\
point + point = point
$$
注意这里的点之间的加法运算，实际表示的是两点的 **中点**。因为点的完整齐次坐标定义为 $(\frac{x}{w},\frac{y}{w},1)^T,\ w\neq 0$

#### 仿射变换

通过引入了齐次坐标，我们可以将之前比较丑陋的形式改写为 **旋转缩放平移** 三位一体的仿射变换（Affine transformation）形式
$$
\left(\begin{array}{l}
x^{\prime} \\
y^{\prime} \\
1
\end{array}\right)=\left(\begin{array}{llc}
a & b & t_x \\
c & d & t_y \\
0 & 0 & 1
\end{array}\right) \cdot\left(\begin{array}{l}
x \\
y \\
1
\end{array}\right)
$$
我们仍然可以用基向量的方式进行理解，$\hat x', \hat y'$ 是向量所以其为 $(a,c,0)^T,\ (b,d,0)^T$，最后一个理解为 **变换后的原点坐标** $(t_x,t_y,1)^T$，那么我们就可以用仿射变换轻松地表示之前的旋转缩放平移

$$
\mathbf{S}\left(s_x, s_y\right)=\left(\begin{array}{ccc}
s_x & 0 & 0 \\
0 & s_y & 0 \\
0 & 0 & 1
\end{array}\right)\\ \\
$$

$$
\mathbf{R}(\alpha)=\left(\begin{array}{ccc}
\cos \alpha & -\sin \alpha & 0 \\
\sin \alpha & \cos \alpha & 0 \\
0 & 0 & 1
\end{array}\right)\\ \\
$$

$$
\mathbf{T}\left(t_x, t_y\right)=\left(\begin{array}{ccc}
1 & 0 & t_x \\
0 & 1 & t_y \\
0 & 0 & 1
\end{array}\right)
$$



### 3D 变换

三维的情况基本与二维没有出入，除了旋转有个要注意的点。同样的，定义三维的齐次坐标

+ 点：$(x/w, y/w, z/w,1)^T ,\ w \neq 0$
+ 向量：$(x, y, z,0)^T$

其仿射变换如下：
$$
\left(\begin{array}{c}
x^{\prime} \\
y^{\prime} \\
z^{\prime} \\
1
\end{array}\right)=\left(\begin{array}{lllc}
a & b & c & t_x \\
d & e & f & t_y \\
g & h & i & t_z \\
0 & 0 & 0 & 1
\end{array}\right) \cdot\left(\begin{array}{l}
x \\
y \\
z \\
1
\end{array}\right)
$$

#### 缩放

$$
\mathbf{S}\left(s_x, s_y, s_z\right)=\left(\begin{array}{cccc}
s_x & 0 & 0 & 0 \\
0 & s_y & 0 & 0 \\
0 & 0 & s_z & 0 \\
0 & 0 & 0 & 1
\end{array}\right)
$$

#### 平移

$$
\mathbf{T}\left(t_x, t_y, t_z\right)=\left(\begin{array}{cccc}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1
\end{array}\right)
$$

#### 旋转（绕着某个轴）

$$
\begin{aligned}
&\mathbf{R}_x(\alpha)=\left(\begin{array}{cccc}
1 & 0 & 0 & 0 \\
0 & \cos \alpha & -\sin \alpha & 0 \\
0 & \sin \alpha & \cos \alpha & 0 \\
0 & 0 & 0 & 1
\end{array}\right) \\
&\mathbf{R}_y(\alpha)=\left(\begin{array}{cccc}
\cos \alpha & 0 & \sin \alpha & 0 \\
0 & 1 & 0 & 0 \\
-\sin \alpha & 0 & \cos \alpha & 0 \\
0 & 0 & 0 & 1
\end{array}\right) \\
&\mathbf{R}_z(\alpha)=\left(\begin{array}{cccc}
\cos \alpha & -\sin \alpha & 0 & 0 \\
\sin \alpha & \cos \alpha & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{array}\right)
\end{aligned}
$$

+ 不难发现，绕着$Y$轴旋转的结果有些奇怪，这是因为$X$轴基向量和$Z$轴基向量的叉乘为$Y$轴负向的向量，那么所有的旋转角度都会相当于变为原来的 **负值**，从而才会产生这样的差异

#### 旋转（Rodrigues'Rotation Formula）

绕着转轴 $n$ 旋转 $\alpha$ 角度，[推导过程](https://www.cnblogs.com/wtyuan/p/12324495.html):cry:
$$
R(n, \alpha)=\cos (\alpha) E+(1-\cos (\alpha)) n n^T+\sin (\alpha)\left(\begin{array}{ccc}
0 & -n_z & n_y \\
n_z & 0 & -n_x \\
-n_y & n_x & 0
\end{array}\right)
$$

## 视图/相机变换

想象我们拍照的过程，首先放置几个人物（模型变换 M），然后给定相机位置（相机变换 V），最后按下快门保存为一张二维的照片（投影变换 P），这就是所谓的 **MVP Transformation**

### 定义相机属性

1. 位置（postion）： $\vec{e}$
2. 视线方向（Look-at / gaze direction）：$\hat g$
3. 垂直方向（Up direction）：$\hat t$

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919232151.png" alt="image-20220919232151055" style="zoom:67%;" />

+ 事实上将你的头视作摄像机，改变位置很好理解，走两步就行；改变视线方向也很好理解，即让你的视线瞄准一个坐标为$(x, y, z)^T$的物体即可；最后一个垂直方向，是类似法线（呆毛）的概念，你可以通过 **歪头** 这一行为更改

+ 约定初始状态，也为了后续表示的方便，相机 **永远** 位于原点，永远视线朝向$-Z$，永远上方向为$Y$

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220919234134.png" alt="image-20220919234134279" style="zoom: 67%;" />

那么现在的问题就变为，如何将一个由 $(\vec{e},\hat g, \hat t)$ 表示的相机，**标准化** 为上述的初始状态呢？不难想到应该由以下几步：

1. 将其位置 $\vec{e}$ 移动到原点（平移变换）
2. 将 $\hat g $ 朝向 $-Z$（旋转变换）
3. 将 $\hat t $ 朝向 $Y$（旋转变换）
4. 令 $\hat g \times \hat t $ 朝向 $X$（旋转变化）

总体来说，先平移后旋转（先右后左）：$M_v = R_vT_v$

这样一步步写，无疑是很痛苦的。所以我们考虑其逆矩阵（因为旋转矩阵是正交矩阵，所以其逆矩阵就是它的转置矩阵）

首先是平移（这步没有必要逆矩阵）
$$
T_v =\left[\begin{array}{cccc}
1 & 0 & 0 & -x_e \\
0 & 1 & 0 & -y_e \\
0 & 0 & 1 & -z_e \\
0 & 0 & 0 & 1
\end{array}\right]
$$
然后是旋转，这里我们逆向考虑把要求的各个方向的 **基向量** 转到 $\hat g,\ \hat t,\ \hat g \times \hat t$ 即可得到逆旋转矩阵，然后转置即可得到旋转矩阵
$$
\begin{aligned}
R_{\text {v }}^{-1} &=\left[\begin{array}{llll}
x_{\hat{g} \times \hat{t}} & x_t & x_{-g} & 0 \\
y_{\hat{g} \times \hat{t}} & y_t & y_{-g} & 0 \\
z_{\hat{g} \times \hat{t}} & z_t & z_{-g} & 0 \\
0 & 0 & 0 & 1
\end{array}\right] \\
R_{\text {v }} &=\left[\begin{array}{cccc}
x_{\hat{g} \times \hat{t}} & y_{\hat{g} \times \hat{t}} & z_{\hat{g} \times \hat{t}} & 0 \\
x_t & y_t & z_t & 0 \\
x_{-g} & y_{-g} & z_{-g} & 0 \\
0 & 0 & 0 & 1
\end{array}\right]
\end{aligned}
$$


## 投影变换

### 正交投影

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220920124755.jpeg" alt="img" style="zoom: 80%;" />

上图显示一个简单的正交投影的三个不同视图，正交投影可以简单理解成

1. 摄像机看向 $-Z$ 方向，上方向为 $Y$
2. 将 $Z$ 设置为 0
3. 平移并缩放物体至区域 $[-1,1]^2$

但在实际操作中，我们一般用一个立方体以描述正交投影的变换矩阵（Orthographic Projection），以六元组 $(l,r,b,t,n,f)$ 表示其左，右，底，顶，近，远平面

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220920174659.jpeg" alt="img" style="zoom:80%;" />

+ 注意$Z$值，这里$z_{far} < z_{near}$

那我们的目的就是将其缩放到变为一个标准立方体，不难想到也是先平移再缩放
$$
\begin{aligned}
\mathbf{P}_o =\mathbf{S}(\mathbf{s}) \mathbf{T}(\mathbf{t}) &=\left(\begin{array}{cccc}
\frac{2}{r-l} & 0 & 0 & 0 \\
0 & \frac{2}{t-b} & 0 & 0 \\
0 & 0 & \frac{2}{f-n} & 0 \\
0 & 0 & 0 & 1
\end{array}\right)\left(\begin{array}{cccc}
1 & 0 & 0 & -\frac{l+r}{2} \\
0 & 1 & 0 & -\frac{t+b}{2} \\
0 & 0 & 1 & -\frac{f+n}{2} \\
0 & 0 & 0 & 1
\end{array}\right) \\
&=\left(\begin{array}{cccc}
\frac{2}{r-l} & 0 & 0 & -\frac{r+l}{r-l} \\
0 & \frac{2}{t-b} & 0 & -\frac{t+b}{t-b} \\
0 & 0 & \frac{2}{f-n} & -\frac{f+n}{f-n} \\
0 & 0 & 0 & 1
\end{array}\right) .
\end{aligned}
$$

### 透视投影

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220920180456.png" alt="image-20220920180456183" style="zoom: 67%;" />

想象把左边的平截头体（Frustum）**挤压** 成右边的立方体，然后再做一次 **正交投影** 即可。显然在 **挤压** 的过程中满足以下条件

1. 近平面所有点不变
2. 远平面所有点坐标 z 值不变
3. 远平面的中心点坐标值不变

那么问题就变为了如何 **挤压**，这里用矩阵 $M_{persp \to orho}$ 表示

首先来看一个纵切面

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220920181358.png" alt="image-20220920181358915" style="zoom: 80%;" />

通过小学二年级的相似知识，不难得出 $\dfrac{x'}{x} =\dfrac{y'}{y} = \dfrac{n}{z}$

即 $y' = \frac{n}{z} y,\ x' = \frac{n}{z}x$，写成矩阵变换的形式

$$
M_{p \rightarrow o}^{(4 \times 4)}\left(\begin{array}{c}
x \\
y \\
z \\
1
\end{array}\right)==\left(\begin{array}{c}
n x / z \\
n y / z \\
\text { unknown } \\
1
\end{array}\right)==\left(\begin{array}{c}
n x \\
n y \\
\text { still unknown } \\
z
\end{array}\right)
$$

如果将矩阵乘法展开第一行，第二行以及最后一行：

$$
Ax+By+Cz+D = nx \\
Ex+Fy+Gz+H = ny \\
Mx+Ny+Oz+P = z
$$

不难发现应得到：$A=F=n,\ O = 1$ 其余项为 0，那么至此 $M_{p\to o}$ 已经可以写出一大半了，只有第三行未知

这时想到之前的 3 个约束条件：

1. 近平面所有点不变

   $(x,y,n,1)^T$ 经过 $M_{p\to o}$ 变换后应该还是为本身才行
   $$
   \left(\begin{array}{cccc}
   n & 0 & 0 & 0 \\
   0 &n & 0 & 0 \\
   I & J & K & L \\
   0 & 0 & 1 & 0
   \end{array}\right) .
   \left(\begin{array}{c}
   x  \\y \\n  \\1 
   \end{array}\right)
   = 
   \left(\begin{array}{c}
   x  \\y \\n  \\1 
   \end{array}\right)
   $$
   很明显，这里只有当 $n =1 $ 时才成立，这显然有问题。所以我们这里选择把结果 $(x,y,n,1)^T*n$，这样
   $$
   \left(\begin{array}{cccc}
   n & 0 & 0 & 0 \\
   0 &n & 0 & 0 \\
   I & J & K & L \\
   0 & 0 & 1 & 0
   \end{array}\right) .
   \left(\begin{array}{c}
   x  \\y \\n  \\1 
   \end{array}\right)
   = 
   \left(\begin{array}{c}
   nx  \\ny \\n^2  \\n 
   \end{array}\right)
   $$
   那么就可以开始求取第三行了
   $$
   Ix+Jy+Kn+L = n^2
   $$
   很明显，$I = J=0,\ Kn+ L = n^2$

2. 远平面中心点坐标值不变

   $(0,0,f,1)$ 经过 $M_{p\to o}$ 变换后应该还是为本身才行，同样的，为了满足第四行选择 $(0,0,f,1)^T*f$
   $$
   \left(\begin{array}{cccc}
   n & 0 & 0 & 0 \\
   0 &n & 0 & 0 \\
   0 & 0 & K & L \\
   0 & 0 & 1 & 0
   \end{array}\right) .
   \left(\begin{array}{c}
   0  \\0 \\f  \\1 
   \end{array}\right)
   = 
   \left(\begin{array}{c}
   0  \\0 \\f  \\1 
   \end{array}\right)
   = =
   \left(\begin{array}{c}
   0  \\0 \\f^2  \\f 
   \end{array}\right)
   $$
   那么就可以得到 $Kf+L = f^2$

联立上面两个式子
$$
\begin{cases}
   Kn+ L &= n^2\\
   Kf+ L &= f^2
\end{cases}
$$
解得 $K = n+f,\ D = -nf$

所以就可以得到投影向正交变换的矩阵
$$
\left(\begin{array}{cccc}
n & 0 & 0 & 0 \\
0 &n & 0 & 0 \\
0 & 0 & n+f & -nf \\
0 & 0 & 1 & 0
\end{array}\right) 
$$
那么，最终的投影矩阵即为
$$
M_{persp} = M_{ortho}M_{p\to o}
$$

## 参考

https://blog.csdn.net/weixin_43803133/article/details/107449570

[推导投影矩阵 - 知乎](https://zhuanlan.zhihu.com/p/122411512?utm_source=qq&utm_medium=social&utm_oi=605668290971045888)

[什么是齐次坐标? - 知乎](https://zhuanlan.zhihu.com/p/258437902)

[实时渲染第四版 4.6 投影变换 - 知乎](https://zhuanlan.zhihu.com/p/392216888)