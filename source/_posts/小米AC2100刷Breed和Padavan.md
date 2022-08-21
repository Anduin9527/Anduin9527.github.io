---
title: 小米/红米 AC2100 急速刷 Breed
tags:
  - 教程
  - 网络
  - 硬件
categories: 折腾系列
abbrlink: e5ccadb4
date: 2021-12-03 17:58:06
---

## 前言

开热点联机文明 6 太折磨了，于是入了一台小米 AC2100，原本想整个软路由的，日后再嗦。

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211203180825.jpeg" alt="小米路由器AC2100立即购买-小米商城" style="zoom: 50%;" />

<!--more-->

## 准备工作

1. 插上电源

2. 准备两根网线，一根连接网口和 `WAN` 口（确保路由器有网络），一根连接 `LAN` 口（三选一）和电脑

## 回退版本

### 下载固件

小米 AC2100 的 **2.0.722** 版本和红米 AC2100 的 **2.0.7** 版本，都留下的 SSH 漏洞，能让我们进系统刷机。目前全球的 AC2100 刷机方案，似乎都是由这个漏洞来的，感觉是小米官方有意为之。<del> 那你倒是给个开发者模式啊！</del>

所以我们需要先回退到之前的版本，拿到权限后再刷机。

> **官方下载链接：**
> 红米 RM2100： http://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/rm2100/miwifi_rm2100_firmware_d6234_2.0.7.bin
> 小米 R2100：http://cdn.cnbj1.fds.api.mi-img.com/xiaoqiang/rom/r2100/miwifi_r2100_firmware_4b519_2.0.722.bin

### 更换固件

进入小米路由器的网关(192.168.31.1)

在常用设置-> 系统状态-> 升级检测-> 手动升级，上传上一步下载好的固件。等待路由器降级重启完成。检查版本无误即可

## 刷 Breed

Breed 是一个不死 uboot，可以方便的刷固件并且保证不会变砖

### 漏洞注入

进入网关，可以看到地址栏的链接为

```
http://192.168.31.1/cgi-bin/luci/;stok=<STOK>/web/home#router
```

`<STOK>` 是每次登陆都会动态变化的，把他记录下来

接着在浏览器地址栏中输入以下代码，**注意替换掉 `<STOK>` 部分**：

```
http://192.168.31.1/cgi-bin/luci/;stok=<STOK>/api/misystem/set_config_iotdev?bssid=Xiaomi&user_id=longdike&ssid=-h%3B%20nvram%20set%20ssh_en%3D1%3B%20nvram%20commit%3B%20sed%20-i%20's%2Fchannel%3D.*%2Fchannel%3D%5C%22debug%5C%22%2Fg'%20%2Fetc%2Finit.d%2Fdropbear%3B%20%2Fetc%2Finit.d%2Fdropbear%20start%3B
```

+ 返回 `{"code":0}` 代表成功
+ 返回 `401` 或者 `404` 请检查固件版本或者链接

### 重启路由

在上步刷入成功之后，路由器系统灯（下面那个）会从蓝熄灭，然后变黄，再变蓝进入系统

此时 **拔掉电源，按住 reset 键（红米用针顶住 reset 孔）同时接上电源**，此时电源灯会经历双闪，然后网络灯（上面那个）蓝色闪烁不停，说明 Breed 刷机成功。

### 访问 Breed 后台

地址栏输入 192.168.1.1 或者 192.168.2.1 可以进入 Breed 的网关。如果进入失败，请检查以太网的 IP 设置。

在网络适配器中更改 IPv4 协议属性，设置手动获取 IP。

```
IP地址
192.168.1.1
子网掩码
255.255.255.0
默认网关
192.168.1.1
```

## 刷自定义固件

固件更新-> 选中固件-> 然后上传即可

关于固件我这里推荐老毛子也就是 Padavan

[老毛子](https://opt.cn2qq.com/padavan/)（红米选择 RM2100 小米选择 R2100）

然后等待重启，访问 192.168.123.1 即可

> 默认配置
>
> 固件网关：192.168.123.1
>
> 管理页面：http://my.router/
>
> 管理帐号：admin
>
> 管理密码：admin
>
> WIFI 密码：1234567890
>
>（刷机不会恢复默认配置）

一键更新固件脚本：

```bash
wget --no-check-certificate -O- https://opt.cn2qq.com/opt-script/up.sh > /tmp/up.sh && bash < /tmp/up.sh &
```



## 参考

https://www.right.com.cn/forum/forum.php?mod = viewthread&tid = 4066963&extra = page%3D2%26filter%3Dtypeid%26typeid%3D43

http://openwrt.ink: 88/archives/s-breed

[Breed 固件](https://opt.cn2qq.com/)

