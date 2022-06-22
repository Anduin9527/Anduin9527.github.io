---
title: 微软三件套安装以及配置
tags:
  - 工具
  - 分享
abbrlink: f77b55e6
date: 2021-10-26 17:27:59
---

### <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211026174036.jpg" alt="cxdxhh2f9r071" style="zoom:50%;" />

<!--more-->

## Windows Terminal

>Windows 终端是一个面向命令行工具和 shell（如命令提示符（cmd）、PowerShell 和适用于 Linux 的 Windows 子系统 (WSL)）用户的新式终端应用程序。 它的主要功能包括多个选项卡、窗格、Unicode 和 UTF-8 字符支持、GPU 加速文本呈现引擎，你还可用它来创建你自己的主题并自定义文本、颜色、背景和快捷方式。

<del>好看才是第一生产力，所以别在用cmd的黑框还有powershell的蓝框了</del>

### 安装

方法一 [微软商店](https://aka.ms/terminal)（推荐方式）

方法二 Windows Terminal 的 [Github Releases](https://github.com/microsoft/terminal/releases) <img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211026175219.png" alt="image-20211026175219873" style="zoom:67%;" />

+ 选择完版本（preview是预览版），选择后缀为`.msixbundle`的文件下载安装即可

方法三 winget

首先你得微软商店（搜索应用安装程序）通过[Github Releases](https://github.com/microsoft/winget-cli/releases) 安装winget，然后打开你的powershell 输入

```powershell
winget install --id=Microsoft.WindowsTerminal -e
#安装成功后查看版本
winget -v
```

+ 如果提示没有这个命令，考虑重启终端或者重启电脑

+ 推荐安装一下，因为后续的 powershell7 配置（美化）还会用到这个东西

安装成功之后

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211026180656.png" alt="image-20211026180655833" style="zoom: 50%;" />

<img src="https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211026180900.png" alt="image-20211026180900388" style="zoom: 50%;" />

你会发现你的界面和我的不大一样，问题不大，下面开始配置

### 配置

选择**设置**可以进行一些基础功能的设置，比较明了，不作介绍。所有的配置项都在`setting.json`（点击设置后，选择打开JSON文件）中保存。

![image-20211026184621095](https://imgbed-1304793179.cos.ap-nanjing.myqcloud.com/typora/20211026184621.png)

+ 最外层都是一些全局设置，具体的配置选项可以去[微软文档](https://docs.microsoft.com/zh-cn/windows/terminal/json-fragment-extensions)中看
+ `defaultProfile`：值是一个UUID，也就是`profiles`的`guid`
+ `keybindings`：自定义一些快捷键
+ `profiles`的默认选项是对所有配置文件生效的
  + `acrylicOpacity`：亚克力面板效果
  + `fontFace`：选择安装含有PL（powerline）且等宽（Mono）的字体（推荐https://www.nerdfonts.com/font-downloads）
  + `list`：含有众多配置的单独设置，如果你自己新建的话，注意`guid`别自己写。然后如果配置要连接你的服务器`commandline`就可以写成ssh之类的
+ `schemes`：配色方案

## PowerShell 7

>Windows PowerShell 5.1 是在 .NET Framework v4.5 基础上构建的。 随着 PowerShell 6.0 的发布，PowerShell 成为基于 .NET Core 2.0 构建的开源项目。 PowerShell 7.0 是在 .NET Core 3.1 基础上构建的。 随着 PowerShell 7.2 的发布，将在 .NET 6.0 基础上构建 PowerShell。 从 .NET Framework 转换到 .Net Core 使 PowerShell 成为可跨平台的解决方案。 PowerShell 在 Windows、macOS 和 Linux 上运行。

### 安装

方法一 微软商店<del>连Powershell都上了VSCode呢？</del>

方法二 PowerShell的[Github Releases](https://github.com/PowerShell/PowerShell/releases/) windows选择`.msi`后缀即可

方法三 winget

```powershell
winget install --name PowerShell --exact --source winget
```

### 配置

首先是要让之前安装的 windows terminal 默认开启 powershell 7 而不是原装的 windows powershell

打开之前的`Profile`在如下位置添加`commandline`

```json
"profiles": {
    "defaults": {
      "commandline": "pwsh.exe"
    },
}
```

#### 安装gsudo

在命令行中提供管理员权限，而无需另起管理员powershell

```powershell
 winget install --name gsudo --source winget
 #安装成功后查看版本
 sudo -v
 #使用
 sudo yourcommand
```

+ 后续的命令中有一些需要管理员权限

#### 安装Oh-My-Posh 3

有的人应该知道oh-my-zsh，都是懒癌福音，一键解锁终端主题。

```powershell
Install-Module oh-my-posh -Scope AllUsers
```

安装中基本一直y即可

安装完成之后，可以查看现有的主题，然后选择一个更换。

```powershell
#查看主题
Get-PoshThemes						
#设置主题
Set-PoshPrompt -Theme ThemeName
```

+ 如果你发现主题中有大量方框乱码，请回到上文考虑修改默认字体

当然如果你想要自定义主题的话可以导出主题配置文件，然后修改其json文件再重新设置

```powershell
#导出主题
Export-PoshTheme -FilePath ~/.mytheme.omp.json
#设置主题
Set-PoshPrompt -Theme ~/.mytheme.omp.json
```

但是你会发现重启终端之后就失效了，这是为什么嘞？，其实是要修改 PowerShell 自身的配置文件（类似于.zshrc或者.bashrc）。

#### 安装PSReadLine

PSReadLine会根据你的历史记录来进行预测和补全命令

```powershell
Install-Module PSReadLine -Scope AllUsers
```

```powershell
# 显示所有可以配置的选项
Get-PSReadLineOption  
# 显示所有可以配置的快捷键
Get-PSReadLineKeyHandler  
```

#### 配置Profile

```powershell
if (!(Test-Path -Path $PROFILE.AllUsersCurrentHost)) {
  New-Item -ItemType File -Path $PROFILE.AllUsersCurrentHost -Force
}
```

+ 一个简单的脚本判断你是否已经创建了配置文件

```powershell
#使用vscode编辑
code $Profile 
#使用记事本编辑 （呜呜呜别再用记事本了）
notepad $Profile
```

在`$Profile`中添加：

```powershell
# 设置 oh-my-posh
Import-Module oh-my-posh
# 设置 ps-read-line
Import-Module PSReadLine
# 设置主题
Set-PoshPrompt paradox
# 设置预测文本来源为历史记录
Set-PSReadLineOption -PredictionSource History
# 每次回溯输入历史，光标定位于输入内容末尾
Set-PSReadLineOption -HistorySearchCursorMovesToEnd
# 设置 Tab 为菜单补全和 Intellisense
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete
# 设置向上键为后向搜索历史记录
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
# 设置向下键为前向搜索历史纪录
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
```

最后重启终端即可！

## WSL

>适用于 Linux 的 Windows 子系统可让开发人员按原样运行 GNU/Linux 环境 - 包括大多数命令行工具、实用工具和应用程序 - 且不会产生传统虚拟机或双启动设置开销。
>
>您可以：
>
>- [在 Microsoft Store](https://aka.ms/wslstore) 中选择你偏好的 GNU/Linux 分发版。
>- 运行常用的命令行软件工具（例如 `grep`、`sed`、`awk`）或其他 ELF-64 二进制文件。
>- 运行 Bash shell 脚本和 GNU/Linux 命令行应用程序，包括：
> - 工具：vim、emacs、tmux
> - 语言：[NodeJS](https://docs.microsoft.com/zh-cn/windows/nodejs/setup-on-wsl2)、Javascript、[Python](https://docs.microsoft.com/zh-cn/windows/python/web-frameworks)、Ruby、C/ C++、C# 与 F#、Rust、Go 等。
> - 服务：SSHD、[MySQL](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-database)、Apache、lighttpd、[MongoDB](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-database)、[PostgreSQL](https://docs.microsoft.com/zh-cn/windows/wsl/tutorials/wsl-database)。
>- 使用自己的 GNU/Linux 分发包管理器安装其他软件。
>- 使用类似于 Unix 的命令行 shell 调用 Windows 应用程序。
>- 在 Windows 上调用 GNU/Linux 应用程序。
>- 现已支持CUDA！一起来炼丹吧！

### 安装

```powershell
wsl --install
```

+ 此命令将启用所需的可选组件，下载最新的 Linux 内核，将 WSL 2 设置为默认值，并默认安装 Ubuntu
+ 而后会新建用户并设置密码

然后重启电脑。在终端就看见一个新的选项卡

而后的Linux配置可以参考组内另一名讲师（莫非）的[虚拟机安装Ubuntu教程](https://closed-linen-ea9.notion.site/Ubuntu-cb4d33bdbcc2400b9b04cc56ba21d080)



## 参考

[微软官方文档](https://docs.microsoft.com/en-us/)

[Windows Terminal 完美配置 PowerShell 7.1](https://zhuanlan.zhihu.com/p/137595941)

[Window Terminal 安装以及使用](https://zhuanlan.zhihu.com/p/351281543)

