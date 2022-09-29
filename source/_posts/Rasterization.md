---
title: Games101-Rasterization
tags:
  - 计算机图形学
  - 笔记
category: Games101笔记
katex: true
abbrlink: 154ddc25
---

## 前言

在 [上文-Transform](https://lapras.xyz/2022/09/20/918c829e.html) 中，我们已经将常见经过 MVP（Model-View-Projection）变换，使其转换到了二维平面。但终究还是要令其在“屏幕”上成像的，这也是 Rasterization 光栅化要做的事

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925223836.png" alt="image-20220925223836691" style="zoom: 67%;" />

<!--more-->

### 如何成像？

首先让我们定义一下 **屏幕**：一个大小为其 **分辨率** 的 **二维数组**，数组中的每个元素称之为 **像素**（Pixel，Picture element）。那么所谓光栅化（Rasterize）就是指把东西画在屏幕上的过程（Drawing onto the screen）

> 具体像素定义（针对本节课，比较简略）：
>
> 1. 是一个独立的小正方形
> 2. 颜色由 `RGB` 定义
> 3. 是成像的最小单位

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925222219.png" alt="image-20220925222212092" style="zoom:80%;" />

定义 **屏幕空间**：

+ 以左下角为原点$(0,0)$，每个单位长度是一个像素的边长，规定坐标只能为整数

+ 显然像素$(x, y)$的中心位于$(x+0.5, y+0.5)$
+ 像素坐标的范围从$(0,0)\sim (width-1, height-1)$

那么就要把我们之前做好的 **标准正方体** 变换到这个屏幕空间中

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925222803.png" alt="image-20220925222803251" style="zoom:80%;" />

首先，请忽视 $Z$ 的存在（另有他用），只考虑 $X-Y$，很容易写出变换矩阵
$$
M_{ {viewport }}=\left[\begin{array}{cccc}
\frac{ { width }}{2} & 0 & 0 & \frac{ { width }}{2} \\
0 & \frac{{ height }}{2} & 0 & \frac{ { height }}{2} \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{array}\right]
$$
然后再把屏幕空间中的多边形分解为 **三角形**，成像到屏幕上，光栅化的流程基本就走完了

### 三角形？三角形！

1. 三角形是最基本的图元，任何多边形都可以分解成三角形

2. 三角形上所有的点一定是共面的

3. 可以通过向量叉积判断内外

   <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925224523.png" alt="image-20220925224523534" style="zoom:80%;" />

   观察这个三角形 $P_0P_1P_2$，要判断 $Q$ 点与三角形的位置关系，只需要计算 $\overrightarrow{P_0P_1} \times \overrightarrow{P_0Q} $，这样就可以根据叉乘结果的正负判断 $Q$ 在 $\overrightarrow{P_0P_1}$ 的左边还是右边，接着在计算 $\overrightarrow{P_1P_2} \times \overrightarrow{P_1Q}$ 以及 $\overrightarrow{P_2P_3} \times \overrightarrow{P_2Q}$ 就可以很容易得到结果啦！

4. 具有成熟的顶点插值方法

那么如何把三角形进行光栅化呢？先来个最简单的办法：**采样**，跟信号与系统的概念类似，本质是将连续的信息离散化，这里我们用三角形的 **三个顶点坐标** 提供信息，依次判断每个 **像素点中心** 是否在三角形 **内部**，是的话就点亮这个像素点

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925223836.png" alt="image-20220925223836691" style="zoom:80%;" />

用一段简单的程序描述，其中 `isinside` 就是三角形叉积判断内外：

```c++
bool isinside(Triangle tri, float x, float y)
{...}
for(int i = 0; i < imax; i++){
    for(int j = 0; j < jmax; j++){
        image[i][j] = isinside(tri, i+0.5, j+0.5);
    }
}
```

每次遍历全部像素显然比较浪费时间，所以可以用 **Axis-Aligned Bounding Box（AABB）** 来进行优化，即先根据三个顶点的坐标确定一个范围的正方形后再遍历。以及适合细长三角形的 **Incremental Triangle Traversal**

### 我超，锯齿！

OK，万事俱备，点亮屏幕！

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925225750.png" alt="image-20220925225750876" style="zoom:80%;" />

显然，这种结果并非我们所愿，为什么会这样的？是我们的采样方法过于简单了吗？

#### 采样理论

 在图形学中，采样无处不在。如光栅化相当于对屏幕中的二维点进行采样、录像相当于对时间进行采样。在采样过程中，当出现一些不正确的现象时，我们会把这些现象称为走样（Aliasing），比如：

| 现象                             | 示例                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| 锯齿（Jaggies ）                 | <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925230315.png" alt="image-20220925230315513" style="zoom: 25%;" /> |
| 摩尔纹（Moir é Patterns）         | <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925230359.png" alt="image-20220925230359098" style="zoom: 25%;" /> |
| 车轮现象（Wagon Wheel Illusion） | <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925230454.png" alt="image-20220925230454399" style="zoom: 25%;" /> |

背后的原理其实是 **傅里叶变换** 和 **奈奎斯特采样定律**

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925231351.png" alt="image-20220925231351667" style="zoom: 67%;" />

如图，有 5 个连续的函数 $f_1 \sim f_5$，其频率渐渐变高。竖直的虚线表示 **采样频率**。在相同采样频率下，我们对这些函数进行采样，然后把采样后的点连线，不难发现

- 频率越低的函数，采样后的连线与原函数差异越小
- 频率越高的函数，采样后的连线与原函数差异越大

这就是 **走样** 的产生原因，因为信息在采样的过程中丢失了，不足以令我们 **还原** 出“完整”的信息。那么根据原因不难想到两种方法以抗锯齿：

+ **提高采样率**：换一块分辨率更高的屏幕
+ **反走样**

#### 反走样

回过头来思考，为什么会产生“锯齿感”，换言之就是不够“平滑”。这里的平滑其实指的就是边缘的渐变效果，颜色和颜色之间不是非黑即白而是逐渐过渡的感觉。这也引出了我们反走样（Antialiased Sampling）的第一个思路：**边界模糊**

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925231024.png" alt="image-20220925231024236" style="zoom: 67%;" />

简言之，就是先 **模糊**，再 **采样**。对于图片而言，也可以进行二维的傅立叶分解。在频率上，这种操作相当于先用 **低通滤波** 把 **高频信息** 过滤掉，再进行采样。

等等你说你不知道啥是低通滤波，啥是高频信息？来看些栗子

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925232459.png" alt="image-20220925232459184" style="zoom:80%;" />

右边的图像就是其傅里叶图像，你不需要直到其具体含义。象征性地记住越靠近中心的部分表示其频率越低即可。这里我使用 `Python` 的 `Numpy` 和 `opencv` 库进行了操作，首先将原图的傅里叶信息表示出来，然后对其傅里叶信息进行操作，也就是各种 **滤波**。那么不难发现，高通滤波（HighPassFiltering ）也就是屏蔽低频率的图像，留下高频率的图像，会让图片的 **边界** 保留下来。反之低通滤波（LowPassFiltering ）会让 **边界模糊**。中通滤波则是兼而有之。那么我们可以得到：对于图片而言，其高频信号反映了其 **边界特征**（剧烈变化）。当然，上述的做法都非常的 **暴力**，具体的滤波器有非常多（比如 **卷积**，数字图片处理懂得伐），这里只是举个例子。

除了模糊化之外，还有很多方案可以用来抗锯齿

+ MSAA（muti-sample anti-aliasing）：每个像素多次采样，求平均，像素的颜色值为负责的区域内取样多次颜色值的平均

- FXAA (Fast Approximate AA)：用边界寻找算法找到边界，直接换成没有锯齿的边界
- TAA (Tem'poral AA) ：时序信息，借助前面帧的信息来进行采样
- DLSS (Deep Learning Super Sampling) ：深度学习的方式还原高分辨率图片

### 场景光栅化

光栅化完三角形，接着就要把之前的场景全部光栅化（还记得大明湖畔的 $Z$ 吗），为了解决近处物体遮蔽远处物体的问题，最简单的思路就是先 **画** 远得，再画近的。但这显然有些问题，因为你将每个三角形看成一个整体，但有些时候他们的远近并不好 **分辨**（考虑三个三角形头尾互相叠）。所以换个角度，从像素出发，反之最后都要光栅化，直接决定每个像素应该画什么不是更简单吗？这也就是 **深度缓冲**（Z-Buffer）的思想：

工作原理：每次渲染的时候除了生成最终的图像之外，还生成一张 **深度图**，该深度图记录了每个像素当前的最小深度

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220925234817.png" alt="image-20220925234817411" style="zoom:80%;" />

用代码更好解释：

```c++
for (each triangle T)							//遍历所有三角形
  for (each sample(x,y,z) in T)		//遍历该三角形涉及到的所有像素
      if (z < zbuffer[x,y]) {			//该像素的当前深度比之前的深度小（距离摄像机更近）
          framebuffer[x,y] = rgb;	//更新该像素的颜色
          zbuffer[x,y] = z;				//更新该像素的深度
      }
```

+ 显然，这是个线性的复杂度$O(n)$，$n$为三角形的个数
+ 但是其无法处理透明物体

## 作业 2

> 在上次作业中，虽然我们在屏幕上画出一个线框三角形，但这看起来并不是那么的有趣。所以这一次我们继续推进一步——在屏幕上画出一个实心三角形，换言之，栅格化一个三角形。上一次作业中，在视口变化之后，我们调用了函数 rasterize_wireframe(const Triangle& t)。但这一次，你需要自己填写并调用函数 rasterize_triangle(const Triangle& t)。该函数的内部工作流程如下：
> 1. 创建三角形的 2 维 bounding box。
> 2. 遍历此 bounding box 内的所有像素（使用其整数索引）。然后，使用像素中心的屏幕空间坐标来检查中心点是否在三角形内。
> 3. 如果在内部，则将其位置处的插值深度值(interpolated depth value) 与深度缓冲区(depth buffer) 中的相应值进行比较。
>
> 4. 如果当前点更靠近相机，请设置像素颜色并更新深度缓冲区(depth buffer)。你需要修改的函数如下：
>
>• `rasterize_triangle()`： 执行三角形栅格化算法
>
>• `static bool insideTriangle()` ：测试点是否在三角形内
>
> 因为我们只知道三角形三个顶点处的深度值，所以对于三角形内部的像素，我们需要用插值的方法得到其深度值。我们已经为你处理好了这一部分，因为有关这方面的内容尚未在课程中涉及。插值的深度值被储存在变量 z_interpolated 中。

代码如下：

`main.cpp`：

```cpp
constexpr double MY_PI = 3.1415926;
inline double deg2red(double deg) { return deg * MY_PI / 180; }
inline double cot(double X) { return 1.0 / tan(X); }
Eigen::Matrix4f get_projection_matrix(float eye_fov, float aspect_ratio, float zNear, float zFar)
{
	// TODO: Copy-paste your implementation from the previous assignment.
	Eigen::Matrix4f projection;
	eye_fov = deg2red(eye_fov / 2);//注意这里弧度转角度的时候为其一半
	projection <<
		cot(eye_fov) / (2 * aspect_ratio ), 0, 0, 0,
		0, cot(eye_fov)/2 , 0, 0,
		0, 0, zNear + zFar / (zNear - zFar), -2.0 * zNear * zFar / (zNear - zFar),
		0, 0, 1, 0;
	return projection;
}
```

`rasterize.cpp`：

```cpp
static bool insideTriangle(int x, int y, const Vector3f* _v)
{
	// TODO : Implement this function to check if the point (x, y) is inside the triangle represented by _v[0], _v[1], _v[2]

	Vector3f P(x + 0.5f, y + 0.5f, 1.0f);

	const Vector3f& A = _v[0];
	const Vector3f& B = _v[1];
	const Vector3f& C = _v[2];

	Vector3f AB = B - A;
	Vector3f BC = C - B;
	Vector3f CA = A - C;

	Vector3f AP = P - A;
	Vector3f BP = P - B;
	Vector3f CP = P - C;

	float z1 = AB.cross(AP).z();
	float z2 = BC.cross(BP).z();
	float z3 = CA.cross(CP).z();

	return (z1 > 0 && z2 > 0 && z3 > 0) || (z1 < 0 && z2 < 0 && z3 < 0);
}
void rst::rasterizer::rasterize_triangle(const Triangle& t) {
	auto v = t.toVector4();//将3D坐标转化为4D齐次坐标

	//TODO : Find out the bounding box of current triangle.
	puts("坐标为");
	std::cout << "v[0]:" << std::endl << v[0] << std::endl
		<< "v[1]:" << std::endl << v[1] << std::endl
		<< "v[2]:" << std::endl << v[2] << std::endl;
	float x_min = std::min(v[0][0], std::min(v[1][0], v[2][0]));
	float x_max = std::max(v[0][0], std::max(v[1][0], v[2][0]));
	float y_min = std::min(v[0][1], std::min(v[1][1], v[2][1]));
	float y_max = std::max(v[0][1], std::max(v[1][1], v[2][1]));
	//将坐标向上取整和向下取整保证三角形位于box内
	x_min = static_cast<int>(std::floor(x_min));
	y_min = static_cast<int>(std::floor(y_min));
	x_max = static_cast<int>(std::ceil(x_max));
	y_max = static_cast<int>(std::ceil(y_max));
	puts("Bounding Box为");
	//按照[min_x, max_x],[min_y, max_y]输出
	printf("x:[%0f, %0f], y:[%0f, %0f]\n", x_min, x_max, y_min, y_max);
	//float  x_min, x_max, y_min, y_max;
	// iterate through the pixel and find if the current pixel is inside the triangle
	for (int i = x_min; i <= x_max; i++)
		for (int j = y_min; j <= y_max; j++)
		{
			if (insideTriangle(i, j, t.v))
			{
				float min_depth = FLT_MAX;//设置默认深度为无穷大（远）
				// If so, use the following code to get the interpolated z value.
				//C++17标准，使用std::tuple返回多个值
				//重心坐标计算
				auto [alpha, beta, gamma] = computeBarycentric2D(static_cast<float>(i + 0.5), static_cast<float>(j + 0.5), t.v);
				float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
				float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
				z_interpolated *= w_reciprocal;
				//获取像素在缓冲区中的索引
				int buf_index = get_index(i, j);
				//如果当前深度小则更新，否则跳过
				if (z_interpolated >= depth_buf[buf_index]) continue;
				//更新深度
				depth_buf[buf_index] = z_interpolated;
				//绘制像素
				set_pixel(Vector3f(i, j, 1), t.getColor());
			}
		}
}
```

效果：

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220926150834.png" alt="image-20220926150834772" style="zoom: 67%;" />

## 参考

[Games101 笔记 —— 光栅化 - scarletsky](https://scarletsky.github.io/2020/06/10/games101-notes-rasterization/)

[GAMES101(5-9): 光栅化-学习笔记 – PP's Blog](https://pangruitao.com/post/2339#51_%E4%BB%8B%E7%BB%8D%E6%88%90%E5%83%8F)

[计算机视觉系列教程 2-2：详解图像滤波算法 | AI 技术聚合](https://aitechtogether.com/article/8460.html)

[Quanwei1992/GAMES101: GAMES101: 现代计算机图形学入门 作业](https://github.com/Quanwei1992/GAMES101)
