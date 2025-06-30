# SGA-SucroseGameAssistant

砂糖代理（SGA）需要运行在win10系统，用于定时循环执行各模块的相关功能。可设置完成后睡眠和从睡眠中唤醒，从而避免电脑在非必要时长期运行。  
目前SGA已适配尘白禁区，原神，MAA，三月七助手等游戏，并支持使用通用执行模块启用其他第三方自动化软件。

####  SGA开源免费，源代码将同时更新于:  
    github(https://github.com/Kin-L/SucroseGameAssistant)  
    gitee(https://gitee.com/huixinghen/SucroseGameAssistant)  

####  目前作者只更新尘白禁区模块和SGA主体，欢迎新的合作者参与对其他模块进行更新适配  

    邮箱: 2805137028@qq.com  
    bilibili站账号: 绘星痕（406315493）  
    抖音：绘星痕（54796280232）  
    https://space.bilibili.com/406315493  
    QQ群聊仅作bug反馈和交流使用，不完全公开。可以B站私信我或邮件联系我索要群聊号。  

## 功能特性

- SGA推荐环境为win10，游戏窗口分辨率1920×1080(最低1600×900)
- 目前已有功能模块：(v2已支持所有模块，v3版本将陆续增加相关适配)  
环行旅舍(功能停止更新)  
原神  
MAA（明日方舟）  
三月七助手  
尘白禁区  
通用执行  
连点器  
绝区零助手  
鸣潮助手  
琴音小助手  

## 安装指南
视频教程：https://www.bilibili.com/video/BV18kKAeYE2t  
1、从网盘下载带"full"后缀的最新安装包  
完整版： 
蓝奏云： https://wwrv.lanzn.com/b033h9z0d 密码:bm32  
gitee： https://gitee.com/huixinghen/SucroseGameAssistant/releases  
123云盘（推荐）：https://www.123pan.com/s/PjLbVv-9kEuA.html提取码:stdl  
更新包：https://gitee.com/huixinghen/SucroseGameAssistant/releases  
手动更新方法：下载替换更新包，解压后将SGA文件夹与原SGA文件夹中同名文件夹进行合并并替换。  
2、解压后，用管理员权限打开SGA.exe文件  

## 快速上手
1、点击左侧“连续任务”下拉选框，选择要执行的模块  
2、点击右侧齿轮样图标进入模块设置页面，选择服务器并输入启动器绝对路径  
3、勾选左侧要执行的任务  
4、点击对应齿轮样图标进入子设置页面，选择要执行的任务  
5、点击上方开始按钮，开始执行任务  
6、使用快捷键（默认为“ctrl+/”）快捷中止运行中的任务

## 部分情况说明
1.  SGA卸载删除前请 清除定时 ，否则您的电脑可能遇到仍在您原来设定过的时间 睡眠中自行唤醒 的情况。如果您已经卸载删除且遇到该情况，可在按照百度教程找到 任务计划程序 ,找到 SGA-awake 的条目，禁用/删除即可解决该问题。
2.  SGA为绿色免安装版，无联网功能，运行需要管理员权限，用于软件启动、设置定时等。若出现报毒和添加信任事件，信则用，本人没有心情也没有能力写病毒和盗号功能。添加信任可参考：https://zhuanlan.zhihu.com/p/645089615
## 特别感谢

1.  SGA用户界面使用了PyQt-Fluent-Widgets  
https://github.com/zhiyiYo/PyQt-Fluent-Widgets
2.  SGA部分代码和学习过程中参考了三月七助手，并组合使用了三月七助手  
https://moesnow.github.io/March7thAssistant
3.  SGA原神模块的自动秘境功能组合使用了BGI的自动秘境功能  
https://github.com/babalae/better-genshin-impact
4.  SGA组合使用了MAA的功能  
https://github.com/MaaAssistantArknights/MaaAssistantArknights