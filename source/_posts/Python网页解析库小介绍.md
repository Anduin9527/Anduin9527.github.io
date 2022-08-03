---
title: Python网页解析库小介绍
tags:
  - 爬虫
  - Python
categories: 爬虫学习
abbrlink: f8dd4268
date: 2022-07-09 10:57:00
---

## 前言

在用`Python`进行网络爬虫，拿到HTML内容之后势必要对其进行一些内容上的解析。之前用过正则表达式`re`和`BeautifulSoup`。前者速度挺快的，但是代码可读性较差。后者虽然简单，但是速度令人捉急。

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220709111111.jpg" alt="92274729_p0_master1200" style="zoom:80%;" />

<!--more-->

先放个速度对比图，数据来源[知乎-拒绝撕逼，用数据来告诉你选择器到底哪家强](https://zhuanlan.zhihu.com/p/25887452)

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220726005550.png" alt="img" style="zoom:80%;" />

## XPath

`XPath`是一门在`XML`⽂档中查找信息的语言.` XPath`可用来在`XML`文档中对元素和属性进行遍历。而我们熟知的`HTML`恰巧属于`XML`。 所以完全可以用其进行解析。

### XML基本知识

```xml
<book>
	<title>高等数学</title>
	<price>28.0</price>
	<author>
		<nick>武钟祥</nick>
		<nick>张宇</nick>
	</author>
</book>
```

+ DOM 将 HTML 表示为标签的树形结构。
+ 每一对标签都是一个节点
+ **标签中的属性及文本也可视为该节点的子节点**
+ 节点之间有父子关系，同胞关系。以及先辈和后裔这种一代及以上的关系
+ 利用缩进，可以很好的理解这些概念

### 安装导入

```bash
pip install lxml -i https://pypi.tuna.tsinghua.edu.cn/simple
```

有很多库都提供了 Xpath 解析的方法，这里选择 `lxml`。

```python
from lxml import etree
# 或者
from lxml import html
etree = html.etree
```

### 解析过程

1. 准备源文件
2. 得到解析对象`et = etree.HTML(html)`
3. 使用`xpath`方法进行解析，视情况选择直接解析或者进一步`for`循环解析。

### 具体方法介绍

1. 节点选取

   + node：选取此节点的所有子节点
   + `/`：从根节点选取
   + `//`：从当前节点选择文档中后裔节点
   + `.`：选取当前节点
   + `..`：选取当前节点的父节点
   + `@`：选取属性

2. 节点选取举例

   | 表达式          | 描述                                                         |
   | --------------- | ------------------------------------------------------------ |
   | bookstore       | 选取 bookstore 元素的所有子节点                              |
   | / bookstore     | 选取根元素 bookstore ，相当于绝对路径的写法                  |
   | bookstore/book  | 选取属于 bookstore 的子元素的所有 book 元素                  |
   | //book          | 选取所有 book 子元素，而不管它们在文档中的位置               |
   | bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置 |
   | //@lang         | 选取名为 lang 的所有属性                                     |

3. 值筛选

   上述表达式都会返回一个`Element`类的列表，我们可以在**表达式中**使用`[]`进行进一步筛选节点。

   用法为在任意节点后添加`[]`，里面的表达式可以为：

   + `1`：选取该节点的第一个元素
   + `last()`：选取该节点的最后一个元素
   + `position()`：选取位置符合布尔表达式的元素。比如`position()>4`。
   + `@lang`：选取拥有名为 lang 的属性的该节点元素。比如`//title[@lang]`表示选取所有拥有名为 lang 的属性的 title 元素
   + `@lang='xx'`：选取拥有名为 lang 的属性且值为 xx 的该节点元素
   + `contains(@属性,"值")`：选取属性包含有某个值的节点元素
   + 可以搭配`and or |`使用

4. 通配符

   + `*`：匹配任何元素节点
   + `@*`：匹配任何属性节点
   + `node()`：匹配任何节点

5. 获取数据

   + `/text()`：获取节点文本内容
   + `/@属性`：获取节点某个属性的内容

### 浏览器工具

1. 首先当然是万能的`F12`。可以通过右键元素选择检查，找到元素的相对位置

   ![F12检查](https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220708154611.png)

   同时，在开发者工具的`Element`中搜索时可以使用`XPath`表达式进行检索。也可以右键元素，选择复制`XPath`

2. `selectorshub`这个浏览器插件，可以直接生成 xpath, cssSelector, Playwright selectors , jQuery, JS Path 等路径


### 小栗子

```python
from lxml import etree
import requests

# 爬取B站排行榜
url = 'https://www.bilibili.com/v/popular/rank/all'
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
proxy = {'http': 'http://127.0.0.1:7890',
         'https': 'http://127.0.0.1:7890'}
resp = requests.get(url, headers=headers, proxies=proxy)
resp.encoding = 'utf-8'
# etree把网页内容转换成可以操作的对象
et = etree.HTML(resp.text)
# 获取排行榜的标题
titles = et.xpath("//div[@class='info']/a/text()")
print(titles)
```



## Pyquery

与 JS 中使用的 Jquery 基本相同，都是使用 CSS 选择器达到解析的目的。

### 常用的CSS选择器

1. 标签选择器`Label`：选择器名和指定的HTML元素名的不区分大小写的匹配。这是选择所有指定类型的最简单方式
2. 类选择器`.Label`：类名是在HTML class文档元素属性中没有空格的任何值。类 Class 是可以重复且有多个的
3. ID选择器`#Label`： 任何元素都可以使用 id 属性设置唯一的 ID 名称。 这是选择单个元素的最有效的方式
4. 通配选择器`*`：选择在一个页面中的所有元素,常常搭配使用
5. 组合器分组`Label1, Label2......`：选择所有出现的Label
6. 后代选择器`Label1 Label2`：选择`Label1`中的所有`Label2`后裔
7. 子选择器`Label1 > Label2`：选择`Label1`中的所有`Label2`直接后代
8. 相邻兄弟选择器`Label1+Label2`：选择`Label2`元素，它是`Label1`的下一个直接兄弟元素
9. 通用兄弟选择器`Label1~Label2`：选择`Label2`元素，它是`Label1`的兄弟元素
10. 属性选择器`Label[attr]`表示选择包含 attr 属性的所有元素，`Label[attr]=val`表示仅选择 attr 属性被赋值为 val 的所有元素，`[attr~=val]`：该选择器仅选择 attr 属性的值（以空格间隔出多个值）中有包含 val 值的所有元素
11. 伪类选择器：内容繁多，功能丰富。详见[w3c](https://www.w3school.com.cn/css/css_pseudo_classes.asp)

### 安装导入

```bash
pip install pyquery -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
from pyquery import PyQuery as pq
```

### 解析过程

1. 准备源文件
2. 得到解析对象`doc = pq(resp.text)`
3. 使用`doc(CSS选择器表达式)`的方式获取`HTML`内容
4. 使用`.text()`获取文本，使用`.attr('属性')`获取属性值
5. 使用`.attr('属性', '值')`来修改属性或者添加属性
6. 使用`.children(css)`查找子节点，`.find(css)`查找子孙节点
7. 使用`.parent(css)`查找父节点，`.parents(css)`查找祖先节点
8. 使用`.siblings(css)`查找兄弟节点
9. 如果选择的内容超过一条后想要获取他们的文本属性值，则需使用`.items()`，返回一个迭代器后使用`for`迭代或者使用`list comprehension`

### 小例子

```python
from pyquery import PyQuery as pq
import requests

# 爬取B站排行榜
url = 'https://www.bilibili.com/v/popular/rank/all'
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
proxy = {'http': 'http://127.0.0.1:7890',
         'https': 'http://127.0.0.1:7890'}
resp = requests.get(url, headers=headers, proxies=proxy)
resp.encoding = 'utf-8'
# pyquery把网页内容转换成可以操作的对象
p = pq(resp.text)
# 获取排行榜的标题
items = p('.rank-list .info>a').items()
title = [item.text() for item in items]
print(title)
```

## Parsel

Parsel 这个库可以解析 HTML 和 XML，同时支持 CSS 和 XPath 两种解析方式并融合了正则表达式的提取功能。[scrapy](https://scrapy.org/)选择器部分也是基于此二次封装的产物。

### 安装导入

```bash
pip install parsel -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```python
from parsel import Selector
```

### 解析过程

1. 首先创建一个`Selector`对象，传入 HTML 字符串。

   ```python
   selector = Selector(text = HTML)
   ```

2. 使用`.css()`或者`.xpath()`进行解析，并通过CSS中的`::text`或者`::attr(属性)`，通过`XPath`的`/text()`和`/@属性`获取内容，返回一个`SelectorList`迭代对象

3. `SelectorList`进行遍历用`.get()`获取内容文本，或者`.getall()`返回内容文本列表
4. `SelectorList`使用`.re()`可以使用正则表达式进一步提取内容并返回列表



