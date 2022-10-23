---
title: Games101-Shading
tags:
  - 计算机图形学
  - 笔记
category: Games101笔记
katex: true
abbrlink: ecdaa9d1
---

## 前言

Shading is the process of applying a material to an object

<!--more-->

在光栅化之后，我们已经能将物体正确的显示在屏幕上，但其颜色却并不“真实”。因而我们现需要对其进行着色（Shading）。课程里面只介绍了一种着色模型：Blinn-Phong 反射模型

## Blinn-Phong 光照模型

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929220613.png" alt="image-20220929220613081" style="zoom: 67%;" />

光照模型，简而言之就是描述光线在物体表面反射效果的模型。比如观察这张图的光影，可以将其分为高光（Specular highlights），漫反射（Diffuse reflection）以及环境光（Ambient lighting）三个部分

取物体表面的一个点进行分析

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929220944.png" alt="image-20220929220944052" style="zoom:80%;" />

+ $\vec v$表示观测方向，即光传播入观测者的方向
+ $\vec n$表示该表面的法线
+ $\vec l$表示光的入射方向（这里为了计算表示方便，使其从反射点指向光源）
+ 显然以上三个向量都是表示方向的方向向量

除此之外，物体表面的亮度取决于从光源到物体表面发射的能量光的大小，显然同一个点上的能量 $I$ 随着光不断向外传播而逐渐减少， 根据能量守恒定律，每一个球面上的总能量都是相同的，很容易推出
$$
r^24\pi I = r'^2 4\pi I'
$$
再假设初始 $r =1$，那么 $I' = I/r^2$，这便是光源入射到某单位面积处的总能量

根据朗伯余弦定律（Lambert's Cosine Law），如果入射光束与接受面存在夹角的情况，那么其接受到的总能量需要打一个折扣，即实际接受光的面积 $A = A'\cos \theta$。换言之，垂直于物体表面的光束分量被全部吸收，平行于物体表面的光束分量被全部无视，那么假定到达表面的光的能量为 $I'$，那么被表面吸收的为入射光的垂直分量，即 $I'\lvert \vec l \rvert\ \cos \theta$ ，同时 $\vec n \cdot \vec l =  \lvert \vec n \rvert\lvert \vec l \rvert \cos \theta$，而两者同为单位向量，所以 $I'' = I'\cdot \vec n \cdot \vec l$，那不妨假设单位面积接受到的能量为 1，最终的公式就是简单的 $\vec n \cdot \vec l$

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929222525.png" alt="image-20220929222525445" style="zoom:80%;" />

 除了反射到 **点** 的能量，物体表面的材质也会对该点对 **光的吸收率** 产生影响，取一反射系数 $K$，当 $K = 1$ 时表示完全不吸收能量（光全部反射，最终呈现为白色），反之则全部吸收呈现为黑色。

### 漫反射

> **漫反射**（简称 **漫射**，英语：diffuse reflection ）是指当一束平行的入射光线射到粗糙的表面时，粗糙的表面会把光线向著各个方向反射的现象。虽然入射线互相平行，由于粗糙的表面上的各点的 [法线](https://zh.m.wikipedia.org/wiki/法线) 方向不一致，造成反射光线向不同的方向无规则地反射。这种反射的光称为漫射光
>
> <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929221524.png" alt="image-20220929221524483" style="zoom:80%;" />

直接给出漫反射的 Blinn-Phong 公式：
$$
L_d = k_d (I/r^2) max(0,\vec n \cdot \vec l)
$$

+ 漫反射由于是光向四周均匀反射产生的，所以与观察方向无关
+ $k_d$即漫反射系数
+ 这里的 `max` 函数是为了当向量点乘为负数的时，即光从背面穿过了物体达到了 shading point，显然这是没有物理意义的，应该视为在光源背面的点（为 0）

### 高光

高光（Specular highlights），我们都知道光线在照射到理想镜面上时，反射光与法线的夹角和入射光与法线的夹角相同，记反射光的方向为 $\vec R$。但由于现实世界并不存在理想镜面，所以当 $\vec R$ 和 $\vec v$ 足够接近时我们就能看到所谓高光

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929225709.png" alt="image-20220929225709233" style="zoom:80%;" />

那么我们就可以用 $\vec R \cdot \vec v$ 的方式来判断它们的接近程度（都是单位向量，点乘越接近 1 为越靠近），但计算 $\vec R$ 的过程相对繁琐，所以我们选择用法线方向 $\vec n$ 和半程向量 $\vec h$ 来刻画。所谓半程向量，也就是两个共起点向量的角平分线所在的方向，这里的 $\vec h$ 就是入射光 $\vec l$ 与观察视角 $\vec v$ 的半程向量。之所以可以这么等价，是因为 $\vec n$ 在理想状态下就是 $\vec l$ 和 $\vec v$ 的半程向量

给出高光的 Blinn-Phong 模型公式
$$
L_s = k_s(I/r^2)max(0,\vec n\cdot \vec h)^p
$$

+ 此公式中没有和漫反射项一样去计算表面接收光能的比例的原因是简化计算（经验性公式）
+ $k_s$即为镜面反射系数
+ `max` 的理由同漫反射，不过这里注意这里描述的是法线和半程向量方向的接近程度
+ 指数$p$的存在是为了加速高光对观测角度变化的敏感程度（在 Blinn-Phong 模型中一般使用 100~200）

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929231136.png" alt="image-20220929231136051" style="zoom:80%;" />

+ 随着镜面反射系数$k_s$的增大，物体高光范围越大
+ 随着指数$p$的增长，物体高光范围会越来越小

### 环境光照

在 Blinn-Phong 这个经验性的模型中，环境光（Ambient Term）项就比较简单。指的是物体表面一点接收到的来自周围物体反射过来四面八方的反射光，是一种 **间接光照**。**它与光的入射方向和观测方向均无关**，在 Blinn-Phong 模型中是一个 **常数**，起增加整体亮度的作用。假设任何一个点所接收到的来自环境的光永远都是相同的，我们记作 $I_a$，再给定一个系数就 $k_a$ 可以直接近似地来得到环境光
$$
L_a = k_a I_a
$$

### 叠加效果

终于，把这三者叠加在一起就得到了完整的 Blinn-Phong 光照模型，其效果如下

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220929231730.png" alt="image-20220929231730319" style="zoom:80%;" />
$$
\begin{aligned}
L &= L_a+L_d+L_s \\
&= k_a I_a+k_d\left(I / r^2\right) \max (0, {n} \cdot {l})+k_s\left(I / r^2\right) \max (0, {n} \cdot {h})^p
\end{aligned}
$$

## 着色频率

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002100503.png" alt="image-20221002100456257" style="zoom:80%;" />

观察上面这幅图，发现其拥有相同的几何细节，但是呈现出的观感却不尽相同。这是因为其着色频率（Shading Frequencies）或者说着色的对象并不一致。从左到右，依次是：逐平面（Flat Shading），逐顶点（Gouraud Shading）以及逐像素（Phong Shading）。本质上来说是对着色的最小单位选取的不同导致其差异

> 这三种着色具体的区别其实也取决于具体的模型，并不是说 Flat  Shading 就一定会很差，下图中，每一行的模型都是完全一样的，每一列是不同网格顶点数的区别，也就是说当我们的几何模型相对复杂的话，其实也可以用一些相对简单的着色模型，而且得到的结果还可以。着色频率取决于面、点数量。当然，Phong Shading 的着色效果好，其计算量当然也比 Flat Shading 大很多（但也不绝对，如果面数超过了像素数那么 Phong  Shading 可能更小），所以具体用哪种着色方法要取决于具体的物体。当面数不是特别多的情况下，Phong Shading 能得到一个较好的结果
>
> <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002103000.png" alt="image-20221002103000530" style="zoom: 67%;" />

### 平面着色

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002101004.png" alt="image-20221002101004726" style="zoom:80%;" />

平面着色/逐平面着色（Flat Shading）是指每一个三角形组成一个平面，求每个三角形的法线只需要将三角形的两个边做 **叉积** 即可，但自然在三角形内部不会有着色的变化，也就是说每个三角形面内各点的颜色是完全一样的。这就造成了观感上会看见许多的三角形

### 高洛德着色

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002101259.png" alt="image-20221002101258949" style="zoom:80%;" />

高洛德着色/逐顶点着色（Gouraud Shading）是指对每个顶点求取其法向量，然后通过 **重心坐标插值**（后续介绍）的方法求出三角形内部的颜色以实现点与点之间颜色的平滑过渡

#### 平均周边面法线

那么如何求取每个顶点的法向量呢，我们知道模型最基本的单位是三角形，建模其实就是用一个个三角形去“拟合”出我们想要的模型，那么那么如果直到每个三角形拟合的对象，比如

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002104528.png" alt="image-20221002104528472" style="zoom:80%;" />

那每个三角形的顶点法向量自然就是与球心的反向延长线，但实际上我们不可能直到每个三角形背后想要表示的具体图形是什么。所以就必须 **从三角形中推断出顶点法线**，所以介绍一个方法：平均周边面法线（average surrounding face normals）

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002110712.png" alt="image-20221002110712818" style="zoom:80%;" />

也就是使用顶点周围的三角形的法线，做一个加权平均，权重可以为三角形的面积（也许并不科学，但是效果好。正所谓“如果它看上去是对的，那么它就是对的”）
$$
N_v =\frac{\sum_i w_iN_i}{\left\|\sum_i w_iN_i\right\|}
$$


### 冯氏着色

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002102753.png" alt="image-20221002102753113" style="zoom:80%;" />

冯氏着色/逐像素着色（Phong Shading）是指对每个像素计算一次光照，像素的法向量是通过 **顶点法向量插值** 得到的，冯氏着色最接近现实，可以在减少三角面数的情况下达到相同的效果（插值后法向量会光滑变化）

+ 注意 Blinn-Phong 是一种着色模型，这里的 Phong Shading 指的是着色频率

## 图形管线

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002113315.png" alt="image-20221002113315867" style="zoom:80%;" />

图形管线（Pipeline）的整个过程其实就是从三维场景到最后看到的二维像素的过程。而这个过程是已经在硬件里写好了，显卡所做的整个的操作就是这样的操作。

1. Vertex Processing：对空间中每一个顶点做 MVP 变换
2. Triangle Processing：形成三角形
3. Rasterization：对每个像素采样判断是否在三角形内，即光栅化
4. Fragment Processing：判定像素是否可见（也可以归为光栅化）
5. Shading：Shading 可以发生在 **顶点处理**（逐顶点着色）上也可以发生在 Fragment 处理（逐像素着色）上

## 纹理

那么现在，模型的光照已经确定下来了，也就是模型拥有了明暗细节的变化。但是更多的信息（属性）该如何体现？比如漫反射系数，颜色等等

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002114725.png" alt="image-20221002114725183" style="zoom:80%;" />

可以看到，这个丑不拉几的独眼巨人在套上了纹理（贴图）之后就丑的更有细节了，套用纹理的过程如下：

1. 美术大大使用 $uv$ 展开，将绘制好的三维图像映射到二维的 texture space（具体映射方法不作介绍）
2. 于是图像上每个点的信息都被存储到二维的 texture 中
3. 每次利用光照模型进行计算的时候根据映射关系，去 **查询** 该点所在 texture 中的信息，对于三角形内部的点同样的也是使用中心坐标插值的方式计算出其在 texture 中的 $u,v$ 坐标
4. 于是最后就得到了“贴图”模型

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002115339.png" alt="image-20221002115339132" style="zoom:80%;" />

### 重心坐标

上述讲了很多地方都需要 **插值** 以达到平滑过渡的效果，而插值就需要表示这些坐标

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002112300.png" alt="image-20221002112300920" style="zoom:50%;" />

对于三角形所在平面上的任意一点的坐标，都可以用三角形的三个顶点坐标的线性表达式表示
$$
(x, y) = \alpha A + \beta B + \gamma C
$$
则 $(\alpha ,\beta,\gamma)$ 为该点的 **重心坐标**

+ 满足$\alpha +\beta+\gamma = 1$

+ 对于三角形内部的点$\alpha ,\beta,\gamma \gt 0$
+ 三角形重心的重心坐标为$(\frac13,\frac13,\frac13)$
+ 几何意义：与三角形的三个顶点构成三个三角形，顶点所对的三角形的面积与三角形总面积的比值，即为对应的重心坐标值

给出其公式：
$$
\begin{gathered}
\alpha =\frac{-\left(x-x_B\right)\left(y_C-y_B\right)+\left(y-y_B\right)\left(x_C-x_B\right)}{-\left(x_A-x_B\right)\left(y_C-y_B\right)+\left(y_A-y_B\right)\left(x_C-x_B\right)} \\
\beta =\frac{-\left(x-x_C\right)\left(y_A-y_C\right)+\left(y-y_C\right)\left(x_A-x_C\right)}{-\left(x_B-x_C\right)\left(y_A-y_C\right)+\left(y_B-y_C\right)\left(x_A-x_C\right)} \\
\gamma = 1-\alpha-\beta
\end{gathered}
$$
重心坐标的意义在于，我们可以将 $A,B,C$ 换成任何顶点的属性，比如法线，漫反射系数，颜色等等以快速方便的进行插值

## 纹理走样问题

### 纹理太小

将低分辨率的纹理应用到高分辨率的画面中，需要将纹理放大（即一个纹理像素 texel 会被映射到多个像素点上），这就导致图片的 **颗粒感** 很严重

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002120831.png" alt="image-20221002120831161" style="zoom:80%;" />

具体过程：如图，该片面为纹理平面，红点表示一个像素点映射到纹理平面的位置。因为屏幕的分辨率高于纹理分辨率，那么会存在多个像素映射到一个 **texel** 附近的情况。对于像素来说，他们默认通过 **Nearest** 方法取最近的 **texel**。这显然不是很对，于是乎我们再次选择插值，看看能否令其平滑过渡

#### 双线性插值

双线性插值（ bilinear interpolation）是根据距离权重综合周围 **四个点** 的属性进行插值

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002121218.png" alt="image-20221002121218677" style="zoom:80%;" />

还是上述的栗子，取 **pixel** 周围四个 **texel**：$ u_{01},u_{11},u_{00},u_{10}$，认为两两 **texel** 之间的距离为单位 1

然后给出线性插值的公式：$lerp(x,v_0,v_1) = v_0 + x(v_1 -v_0)$

所谓双线性插值，就像是线性插值做了两轮，一轮水平以及一轮竖直，这里我们以先水平后竖直为例
$$
\begin{aligned}
u_0&=\operatorname{lerp}(s, u_{00}, u_{10}) \\
u_1&=\operatorname{lerp}(s, u_{01}, u_{11}) \\\\
f(x, y) &= \operatorname{lerp}(t, u_{0}, u_{1})
\end{aligned}
$$
至于双三次插值（bicubic）则是取 16 个像素进行高阶插值，这里不作介绍

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002120535.png" alt="image-20221002120535284" style="zoom:80%;" />

### 纹理太大

同样的，当屏幕分辨率小于纹理分辨率时也会出现走样的问题

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002123248.png" alt="image-20221002123248279" style="zoom:80%;" />

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002123425.png" alt="image-20221002123425170" style="zoom:80%;" />

从左至右，一个像素覆盖的纹理范围越来越大，如果此时还是选择用像素中心点查询对应的纹理信息那么就会出现因为采样频率不足导致的走样问题。当然我们可以选择使用超采样（Supersampling）的方法，对多个采样点进行采样。但是对于远处的点这样做的消耗非常之高。

#### mipmap

“采样会引起走样，那如果我们不采样呢？”

本质上是将点查询问题转换为了范围查询问题，将原本采样一个点，变为直接得到范围内的平均值（最大值/最小值）<del> 我敲，线段树！</del>

具体而言，**多级渐远纹理**（mipmap）能快速地，近似地，范围查询正方形。通过生成一系列的图片达到快速查询的目的。其理念很简单：距观察者的距离超过一定的阈值，OpenGL 会使用不同的多级渐远纹理，即最适合物体的距离的那个。由于距离远，解析度不高也不会被用户注意到。同时，它的性能非常好

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002125149.png" alt="image-20221002125148982" style="zoom:80%;" />

+ 逐层分辨率减半，即将 4 个相邻像素点求均值合为 1 个像素点
+ 一共有$log_2n$层
+ 其需要占用原本$\frac43$的存储空间（等比数列求和）

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002130326.png" alt="image-20221002130326744" style="zoom:80%;" />

那么现在查询一个像素的具体过程：

1. 同时查询这个像素点和其上方右方的两点

2. 取 $L$ 为该点到另外两点距离的最大值（在 $uv$ 平面上）
   $$
   L =\max \left(\sqrt{\left(\frac{d u}{d x}\right)^2+\left(\frac{d v}{d x}\right)^2}, \sqrt{\left(\frac{d u}{d y}\right)^2+\left(\frac{d v}{d y}\right)^2}\right)
   $$

3. 根据 $L$ 的值在 `mipmap` 生成的纹理图片中直接查询 $D = log_2L$。比如 $L = 4$ 那么对应 $D = log_24 = 2$ 层的纹理，因为原本 $4\times 4$ 的纹理范围在 $D=2$ 中变为 $1\times 1$ 的纹理

显然，这样得到的 $D$ 是只有整数，离散的。因此我们考虑插值。比如我们计算出的 $D = 1.8$，那么我们先对其在 $D = 1$ 和 $D =2$ 层进行 **双线性插值**，最后层与层之间再进行一次线性插值。也就是 **三线性插值**

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002131626.png" alt="image-20221002131626565" style="zoom:80%;" />

至此，我们就可以查询任何非整数坐标的纹理

**MipMap 算法的局限**：只能在 u-v 坐标系下做 **方块查询**，有时候会造成 **过度模糊** 的情况，这是因为不同像素点对应到纹理空间的形状并不规整，这一现象在远处更是明显

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002132011.png" alt="image-20221002132011875" style="zoom:67%;" />

为了避免这种情况，引入 **各向异性过滤**，在准备不同级别的纹理贴图时，不再是简简单单横纵纹素各减小一半进行分级，而是 **长减半宽不变 or 宽减半长不变 or 长和宽各减半** 三种情况各进行一次分级，显存消耗为原来的三倍，但性能方面并没有多少影响，这种方法就可以实现在 u-v 坐标系下进行矩形查询

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20221002132026.png" alt="image-20221002132026704" style="zoom:80%;" />

## 参考

[GAMES101 学习笔记-Shading 概述 - 知乎](https://zhuanlan.zhihu.com/p/337887394)

[GAMES101 笔记(3)——Shading - 简书](https://www.jianshu.com/p/39a5b50a70b3)

[计算机图形学七：纹理映射(Texture Mapping)及 Mipmap 技术 - 知乎](https://zhuanlan.zhihu.com/p/144332091?utm_source=qq&utm_medium=social&utm_oi=605668290971045888)
