---
title: SSH的二三事
tags:
  - 教程
  - 网络
categories: 项目经历
abbrlink: 844ad6f8
date: 2022-03-20 00:18:05
---

## 前言

来学校上了两周网课，两周线下，现在又要上网课了G！上网课就算了，我还要给学弟上网课哈哈。整一波虚拟教师V出道

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220320002327.jpg" alt="63476067_p0_master1200" style="zoom: 67%;" />

<!--more-->

## 什么是SSH

>SSH（Secure Shell 的缩写）是一种网络协议，用于加密两台计算机之间的通信，并且支持各种身份验证机制。
>
>实际使用中，它主要用于保证远程登录和远程通信的安全，任何网络服务都可以用这个协议来加密。

比如我们都知道的 Github 下载源代码有两种方式，HTTPS 和 一种形如`git@github.com:username/repositoryname.git`的连接，这其实就是一种 SSH 协议。

再比如我们要操作机房里的服务器，不可能给每一台服务器都配上键盘鼠标显示器，一般都是通过网络的方式远程访问一台服务器。就类似于 TeamViewer 的远程桌面。

### 安装SSH服务

现在几乎所有的 Linux 发行版、Windows 以及 MacOS 基本都自带了`ssh`服务，其中绝大部分都是 OpenSSH ，这是一个关于实现 SSH-2 协议的开源项目，其中还包含了一些常用的辅助工具比如：`ssh-keygen`、`ssh-agent`、`scp`以及`sftp`。

所以绝大部分的电脑都是有`ssh`的，可以用`ssh -V`简单地查看一下。

```bash
#安装
sudo apt install openssh-client
sudo dnf install openssh-clients
```

然后你就可以用`service`或者`systemctl`之类的开启`sshd`服务。

## SSH基础用法

```bash
ssh {user}@{remote_host} -p {22} command
```

+ `remote_host`可以是一个 IP 地址，也可以是一个可被 DNS 解析的域名（Domain）。
+ `ssh`除了可以登录之外，还可以在后面直接添加一条命令`command`，会返回命令的`STDOUT`。利用这个可以写一些脚本儿。
+ `-p`制定了`ssh`服务的端口，默认都是22。
+ 看看`config`以及`known_hosts`

### 常用配置文件

SSH 客户端的全局配置文件是`/etc/ssh/ssh_config`，用户配置文件在`~/.ssh/config`，用户配置文件优先级更高

SSH 服务端的配置文件是`/etc/ssh/sshd_config`

#### config

```
Host {remoteserver}
     HostName {remote_host}
     User {username}
     Port 2222
     IdentityFile ~/.ssh/id_rsa
     ProxyCommand {...}
Host *
     Port 233
     User root
```

+ `Host *`匹配了所有的`remote_host`，也就是当所有匹配不成功的最后选项。后面的`Port`表示所有主机的默认连接端口都是233，`User`表示默认登录用户为 root 。 
+ `remoteserver`是`remote_host`的别名
+ `IdentityFile`是指定用来登录验证的私钥文件，与`ssh -i {path/to/id_rsa}`的作用相同
+ 还有一个`ProxyCommand`它大概有两个使用场景（原理都一样），一个是用代理进行`ssh`，另一个是使用跳板机（中转机）。这个我们后面的端口转发篇再说。 与`ssh -o "{ProxyCommand}"`作用相同，这里假设我要用本地的`Clash`7890端口做一个`socks5`协议的代理。 

```bash
#Windows 使用 git 自带的 connect 工具
ProxyCommand connect -S 127.0.0.1:7890 %h %p
#Linux 使用 netcat 也就是 nc 工具
ProxyCommand nc -X 5 -x 127.0.0.1:7890 %h %p
```

+ `%p`和`%h`分别是`ssh`的端口号以及`remote_host`
+ `connect`
  + `-S`和`-H`分别是`socks`和`HTTPS`代理
+ `nc`
  + `-X 5`指定代理协议为`socks 5`，如果是`HTTPS`代理则为`-X connect`
  + `-x`指定代理的主机地址和端口

登录之后可以用`who -a`查看一下登录的 IP 是否是你的代理服务器 IP。

当你用`ssh`成功登录一次后，会自动在`config`文件中生成对应的配置文件，`IdentityFile`默认缺省。这样，以后我们`ssh`一个已经在`config`中的主机的时候，可以直接`ssh remoteserver`登录，而不需要写一串命令。

#### sshd_config

+ **Port**：建议改为非22的LuckyNumber，防止被扫端口弱口令爆破。
+ **PermitRootLogin**：是否允许 root 账号直接登录。设置为 no 可以有效防止自己`rm -rf /`的欲望
+ **PermitEmptyPasswords**：是否允许空密码登录。如果设置为 yes 并且登录的用户密码为空，则可以使用这个用户免密码登录。
+ **PasswordAuthentication**：是否允许密码登录。如果设置为 no 可以增加安全性。
+ **PrintMotd**： 打印登录提示信息，提示信息存储在/etc/moed文件中
+ 更改配置项后，记得重启`sshd`服务

```bash
sudo systemctl restart sshd.service
```

### 公私钥的概念

上面我们使用`ssh`的时候每一次登录都需要输入密码，这并不安全，其次非常麻烦。`ssh`鼓励用户使用非对称加密的**公私钥验证**来进行登录，而不是使用密码。所谓的**公私钥验证**，本质上是一套加密算法生成出的一对RSA**公钥**和**私钥**。其中**私钥**自行保存，而**公钥**可以用来放在远程的服务器上。这样当远程的服务器接收到来自由你私钥发出的命令后，会使用之前存放的公钥进行认证。免去了在网络明文使用密码传输的风险。在`ssh`中，我们可以使用`ssh-keygen`来生成一对公私钥。

+ 小试一下（使用`ssh-keygen`生成并查看）
+ `ssh-keygen`除了用来生成密钥，还可以用来删除失效变更的公钥指纹（known_hosts），这通常发生在远程服务器出于某些原因被重置了。

```bash
 ssh-keygen -R {remote_host}
```

### 上传SSH公钥的三种姿势

上传公钥的最终目的是在你要登录用户的`~/.ssh/authorized_keys`文件中追加你的**公钥文本**。如果目标用户没有这个文件，需要先自行创建，并修改对应的**权限**，否则`ssh`不会信任你的公钥。

```bash
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

#### ManualSimulation

```bash
mkdir ~/.ssh
touch ~/.ssh/authorized_keys
vim ~/.ssh/authorized_keys
#把公钥复制粘贴进去
```

当然，如果你熟悉管道运算符，你还可以一句话搞定

```shell
cat ~/.ssh/id_rsa.pub | ssh {user}@{remote_host} "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

#### scp

`scp`是 SSH 提供的一个客户端程序，用来在两台主机之间加密传送文件（即复制文件）。其用法和`cp`类似。

```shell
scp ~/.ssh/id_rsa.pub {user}@{remote_host}:~/
ssh {user}@{remote_host} "cat ~/id_rsa.pub >> ~/.ssh/authorized_keys"
rm ~/id_rsa.pub
# 或者
scp ~/.ssh/id_rsa.pub {user}@{remote_host}:~/.ssh/authorized_keys
```

#### ssh-copy-id

OpenSSH 自带一个`ssh-copy-id`命令，可以自动将公钥拷贝到远程服务器的`~/.ssh/authorized_keys`文件。如果`~/.ssh/authorized_keys`文件不存在，`ssh-copy-id`命令会自动创建该文件。

```shell
ssh-copy-id -i key_file user@host
```

+ 注意，`ssh-copy-id`是直接将公钥添加到`authorized_keys`文件的末尾。如果`authorized_keys`文件的末尾不是一个换行符，会导致新的公钥添加到前一个公钥的末尾，两个公钥连在一起，使得它们都无法生效。所以，如果`authorized_keys`文件已经存在，使用`ssh-copy-id`命令之前，务必保证`authorized_keys`文件的末尾是换行符（假设该文件已经存在）。

## SSH端口转发

>SSH 除了登录服务器，还有一大用途，就是作为加密通信的中介，充当两台服务器之间的通信加密跳板，使得原本不加密的通信变成加密通信。这个功能称为端口转发（port forwarding），又称 SSH 隧道（tunnel）。
>
>端口转发有两个主要作用：
>
>（1）将不加密的数据放在 SSH 安全连接里面传输，使得原本不安全的网络服务增加了安全性，比如通过端口转发访问 Telnet、FTP 等明文服务，数据传输就都会加密。
>
>（2）作为数据通信的加密跳板，绕过网络防火墙。



### 本地转发（正向转发）

把远程服务器的端口映射到本地，绕过防火墙和安全组的限制。比如我在远程服务器的8888端口运行了一个不知名的 Web 应用，如果我要在公网临时查看他的部署结果，毕竟远程服务器一般情况下是没有`GUI`的，那么我必须开防火墙和安全组让这个端口暴露在公网，完事后还得再关上，比较麻烦。那么就可以使用`ssh`本地转发。

```shell
 ssh -L [local-remote:]{local-port}:{target-host}:{target-port} {tunnel-host}
```

+ `local-remote`缺省为本机
+ `tunnel-host`就是一句能正常登陆你的远程服务器的`ssh`连接语句
+ `local-port`是映射到本地的某个端口
+ `target-host`为最终的`remote_host`，如果是访问`tunnel-host`的服务，则为`localhost`，要不就是某个内网机器的 host 地址
+ `target-port`为最终的`remote_host`的端口号，也就是服务真正所在的端口

当然，你也可以使用万能的 **VSCode** 直接一键转发。

![image-20220319224707914](https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20220319224716.png)

### 远程转发（反向转发）

**WARNING！反向转发有一定风险**

把本地的某个端口映射到远程服务器，这个应用场景也很常见，比如我在宿舍的机子上跑了一个不知名的 WEB Docker 容器，但是校园网是经过 **NAT** 没有所谓的公网IP，这样在校外就无法访问到我的应用。那么就可以使用`ssh`远程转发，这样我就可以通过访问具有公网IP的远程服务器的某个端口访问到我的应用。

```shell
 ssh -R [remote-host:]{remote-port}:{target-host}:{target-port} {tunnel-host}
```

+ `remote-host`缺省为`tunnel-host`的`localhost`。如果你想让应用被公网任意地址访问，需要更改为`0.0.0.0`，否则只能被远程机器用`localhost`访问，就完全相当于正向转发的逆向了。
+ `remote-port`是映射到远程服务器的某个端口，记得打开对应防火墙和安全组
+ `target-host`是应用所在的 host ，本地就是`localhost`
+ `target-port`是服务真正所在的端口

但是`ssh`默认配置的情况下，哪怕你改了`remote-host`为`0.0.0.0`也不会让你进行一个公网的访问，这是出于安全考量的。

如果你使用`-v`查看的话，就会发现一个警告`Remote: Forwarding listen address "192.168.1.1" overridden by server GatewayPorts`

so，若果想要开启，需要更改`~/.ssh/config`的`GatewayPorts`为yes

### Tips

1. 反向转发注意安全
2. 可以使用`-f`后台执行
3. 可以使用`-N`不进入ssh交互命令行模式
4. 通过`ssh`进行端口转发其实并不稳定，想要构建稳定的端口转发可以了解`autossh`或者`frp`



## 参考

https://wangdoc.com/ssh/basic.html

https://kanda.me/2019/07/01/ssh-over-http-or-socks/

https://abcdabcd987.com/ssh/

https://www.cnblogs.com/bonelee/p/12511024.html