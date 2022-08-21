---
title: 信息茧房脱出-自建 RSS
tags:
  - 教程
  - 分享
categorise: 折腾
abbrlink: 3db8db5b
date: 2021-12-15 11:37:57
---

## 前言

RSS，也就是 Rich Summary Site 。这玩意儿有点时代的眼泪的感觉了。在推荐算法大行其道的当下，RSS 本身是一种逆潮流的选择。加之国区对于 RSS 应用的监管力度之大致使很多优秀的 RSS 服务在国内被和谐。

我之前一直使用的是 feeder.co 无奈他的 IPAD 应用不仅要 Dollar，还锁了国区。所以选择折腾一手，自建 RSS。

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216172339.jpeg" alt="img" style="zoom:67%;" />

<!--more-->

## Miniflux

[Miniflux](https://miniflux.app/) 是一个免费开源的 RSS 聚合源，与另一个开源的 [TTRSS](https://tt-rss.org/) 相比，它的极简设计风格，深的我心（虽然默认 UI 都差不多丑）。

然后 Miniflux 是基于 `GO` 的，没有其他奇奇怪怪的依赖项。

### 部署

如果你没有 Docker 以及 Docker-compose，请立即安装并学习。

[Docker 从入门到实践](https://vuepress.mirror.docker-practice.com/)

1. 新建一个 miniflux 目录

```bash
mkdir ~/miniflux && cd ~/miniflux
```

2. 创建并修改 `docker-compose.yml`

```yaml
version: '3.4'
services:
  miniflux:
    image: miniflux/miniflux:latest
    ports:
      - "<181>:8080"  # 端口181
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://miniflux:<passWord>,.@db/miniflux?sslmode=disable # 数据库密码
      - RUN_MIGRATIONS=1
      - CREATE_ADMIN=1
      - ADMIN_USERNAME=<admin>  # 登录Miniflux的用户名，可自定义
      - ADMIN_PASSWORD=<password>  # 登录Miniflux的密码，可自定义，至少6位
    healthcheck:
      test: ["CMD", "/usr/bin/miniflux", "-healthcheck", "auto"]
  db:
    image: postgres:latest
    environment:
      - POSTGRES_USER=miniflux
      - POSTGRES_PASSWORD=secret
    volumes:
      - miniflux-db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "miniflux"]
      interval: 10s
      start_period: 30s
volumes:
  miniflux-db:

```

+ 自行修改上述带有 `<>` 的选项

3. 启动 Miniflux

```bash
docker-compose up -d
```

访问 `localhost:<端口>` 进入 Miniflux 的管理页面说明大成功，然后就可以开启相应的防火墙，让外网也可以访问。

## RssHub

Miniflux 充当的角色是个 **聚合的订阅源**，那么源本身从哪里来呢？别人整合的固然方便，但是自定义程度肯定不如自己来得爽。但是有些网站或者博客根本没有做 RSS 订阅（<del> 比如我 </del>）

> RSSHub 是一个开源、简单易用、易于扩展的 RSS 生成器，可以给任何奇奇怪怪的内容生成 RSS 订阅源。RSSHub 借助于开源社区的力量快速发展中，目前已适配数百家网站的上千项内容
>
> 可以配合浏览器扩展 [RSSHub Radar (opens new window)](https://github.com/DIYgod/RSSHub-Radar) 和 移动端辅助 App [RSSBud (opens new window)](https://github.com/Cay-Zhang/RSSBud)(iOS) 与 [RSSAid (opens new window)](https://github.com/LeetaoGoooo/RSSAid)(Android) 食用

### 使用

最常用的场景就是下载一个浏览器插件，他会自动嗅探当前网页，如果有符合的路由规则（来自于开源社区的支持），他会自动帮你生成一个 RSS 源，同时支持一键导入到你的聚合源（在设置界面中添加 Miniflux 的地址）。

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216165507.png" alt="image-20211216165506944" style="zoom:67%;" />

### 部署

RSSHub 默认可以使用官方提供的服务器服务，但出于反爬以及稳定性的考量，还是建议我们选择自建服务。

<del> 如果你没有 Docker 以及 Docker-compose，请立即安装并学习。</del>

运行下面的命令下载 RSSHub 镜像

```bash
$ docker pull diygod/rsshub
```

然后运行

```bash
$ docker run -d --name rsshub -p 1200:1200 diygod/rsshub
```

### 添加配置

配置运行在 docker 中的 RSSHub，最便利的方法是使用 docker 环境变量

以设置缓存时间为 1 小时举例，只需要在运行时增加参数：`-e CACHE_EXPIRE=3600`

```bash
$ docker run -d --name rsshub -p 1200:1200 -e CACHE_EXPIRE=3600 
```

更多配置项请看 [官方文档](https://docs.rsshub.app/install/#pei-zhi)

### 使用

同样的，在部署成功之后访问对应的地址。（记得打开防火墙）

然后就可以在 RSSHub Rader 等的设置页面，使用自定义 RSSHub 域名

## 阅读器推荐

说了这么多，总得来点读的，考虑到我的使用场景，所以没有找 IOS 或者 Android 的阅读器。

### win10&win11

推荐国人大佬 云之幻 制作的 [RSS 追踪](https://www.microsoft.com/zh-cn/p/rss-%E8%BF%BD%E8%B8%AA/9n85pv1rjd6v)，界面充分体现了 UWP 应用一贯的极简且平滑的设计理念👍。

> 集成多种主流 RSS 服务的原生 UWP 阅读器，通过在线服务，你可以实现多端同步。经过全新设计的 UI 与强化后的功能，是 Windows 端一个不错的 RSS 阅读选择

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216170732.jpeg" alt="img" style="zoom:67%;" />

这里选择 Fever 模式

进入 Miniflux 的后台，在设置中打开 Fever 插件，设置用户名密码后。即可用 `http://IP:minifluxport/fever/` 的方式导入

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216171232.png" alt="image-20211216171231808" style="zoom:67%;" />

总之就是清爽😎

### ipadOS

APPStore 个人觉得最好用的 Feeder 5 已经从国区下架了，国人团队做的 Ego Reader 体验也不错。可惜横屏适配问题一直没有解决。

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216172758.jpg" alt="img" style="zoom:67%;" />

## 踩坑

### V2rayA 代理问题

可能因为 `/etc/resolv.conf` 被 V2rayA 自动修改成本地的 53 端口来进行 `redirect` 透明代理，导致 docker 内容器出现 ping 不通，curl 不了的问题。经过以下三个步骤，我把 docker 容器都设置为走 V2rayA 的代理模式了。

1. 重新用 docker 部署了一遍 V2rayA

```bash
# run v2raya
docker run -d \
  --restart=always \
  --privileged \
  --network=host \
  --name v2raya \
  -e V2RAYA_ADDRESS=0.0.0.0:2017 \
      -v /lib/modules:/lib/modules \
  -v /etc/resolv.conf:/etc/resolv.conf \
  -v /etc/v2raya:/etc/v2raya \
  mzz2017/v2raya
```

2. 设置 `~/.docker/config.json`

```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://192.168.1.5:20172"	
    }
  }
}
```

+ `192.168.1.5` 是我自定义的 docker0 inet，请使用 `ifconfig` 或者 `ip a`，自行查看 `docker0` 的 inet
+ 20172 是我的 V2RayA 的 HTTP 分流端口

3. 我的 V2rayA 的设置

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216160732.png" alt="image-20211216160732519" style="zoom:50%;" />

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211216160830.png" alt="image-20211216160829968" style="zoom: 67%;" />

## 参考

[Miniflux](https://miniflux.app/)

[RSSHub](https://docs.rsshub.app/)

[利用 Miniflux 自建 RSS](https://hydrotho.github.io/Miniflux-Build-Guide/)







​	
