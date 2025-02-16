# SGA-SucroseGameAssistant

#### 介绍
1.  砂糖代理（SGA），用于游戏等软件，SGA主体的功能是设置定时唤醒电脑，并定时执行各模块的相关功能，完成后睡眠，从而完成任务循环。  

    目前SGA最佳推荐环境为win10，游戏窗口分辨率1920*1080。其他系统win11，win7可能出现我无法解决的bug。其他分辨率的识别能力下降，可能遇到功能异常。

####  目前作者只更新尘白禁区模块和SGA主体已经新功能的开发，其余模块若无合作者接手将无限期停更。
####  原神模块暂交由@yuhui437，并感谢其对于崩铁助手与绝区零助手的贡献
####  欢迎新的合作者参与对其他模块进行更新适配。
2.  目前已有功能模块：  
环行旅舍(功能停止更新)  
原神(交由合作者@yuhui437不定期更新中)  
MAA（明日方舟）(适配停止更新)  
三月七助手（崩坏：星穹铁道）(适配停止更新)  
尘白禁区(不定期更新中)  
通用执行(测试阶段，功能不稳定)
连点器(不定期更新中)  
绝区零助手(由合作者@yuhui437完成)  
3.  SGA视频演示/介绍，SGA使用说明，项目说明文档完善中。

4.  SGA2.0项目开源免费，源代码将同时更新于:  
github(https://github.com/Kin-L/SucroseGameAssistant)  
gitee(https://gitee.com/huixinghen/SucroseGameAssistant)  

5.  完整版下载链接，手动更新包链接：  
完整版： 
蓝奏云： https://wwrv.lanzn.com/b033h9z0d 密码:bm32  
gitee： https://gitee.com/huixinghen/SucroseGameAssistant/releases  
123云盘（推荐）：https://www.123pan.com/s/PjLbVv-9kEuA.html提取码:stdl  
更新包：https://gitee.com/huixinghen/SucroseGameAssistant/releases  
手动更新方法：下载替换更新包，解压后将SGA文件夹与原SGA文件夹中同名文件夹进行合并并替换。  

OCR组件手动下载链接：  
gitee： https://gitee.com/huixinghen/SucroseGameAssistant/releases/tag/ocr  
蓝奏云（推荐）： https://wwp.lanzn.com/b033h9ybi 密码:1siv  

    邮箱: 2805137028@qq.com  
    bilibili站账号: 绘星痕（406315493）  
    抖音：绘星痕（54796280232）  
    https://space.bilibili.com/406315493  
    QQ群聊仅作bug反馈和交流使用，不完全公开。可以B站私信我或邮件联系我索要群聊号。  

#### 安装教程

从网盘链接获取压缩包，解压可用，需要管理员权限，第一次使用时会自动下载OCR组件  
视频教程：https://www.bilibili.com/video/BV18kKAeYE2t  
详细使用说明见压缩包中“Instructions.docx”文件，该文件可能不是最新版本，部分内容仅供参考。  

#### 使用说明

1.  建议给予SGA管理员权限启动
2.  首次执行任务需要自动下载OCR组件，部分机型会下载rapidOCR，可能出现识别错误的情况，暂时无力优化
3.  使用SGA请善用安装包内的使用说明，和我的bilibili账号上的SGA使用演示
4.  遇到bug可尝试更新，或反馈在我的 github/gitee/bilibili账号/邮箱。
5.  SGA功能中使用了三月七助手/BGI/MAA的功能，需要自行安装对应项目并设置，之后对SGA进行设置，才能正常使用。
6.  反馈bug建议附上自己的环境（win10/win11/win7, 官服/B服）,触发bug的流程/停留的界面/bug触发的录屏、截图，附加SGA的“personal”文件夹压缩发给我。以上条件越完善，越能帮助我定位问题所在，修复bug，请根据自己的情况尽量提供给我比较完善的信息。
7.  SGA卸载删除前请 清除定时 ，否则您的电脑可能遇到仍在您原来设定过的时间 睡眠中自行唤醒 的情况。如果您已经卸载删除且遇到该情况，可在按照百度教程找到 任务计划程序 ,找到 SGA-awake 的条目，禁用/删除即可解决该问题。
8.  SGA为绿色免安装版，无联网功能，运行需要管理员权限，用于软件启动、设置定时等。若出现报毒和添加信任事件，信则用，本人没有心情也没有能力写病毒和盗号功能。添加信任可参考：https://zhuanlan.zhihu.com/p/645089615
9.  SGA快速上手【金山文档】 https://kdocs.cn/l/ctEJIsik2lSQ
#### 特别感谢

1.  SGA用户界面使用了PyQt-Fluent-Widgets  
https://github.com/zhiyiYo/PyQt-Fluent-Widgets
2.  SGA部分代码和学习过程中参考了三月七助手，并组合使用了三月七助手  
https://moesnow.github.io/March7thAssistant
3.  SGA原神模块的自动秘境功能组合使用了BGI的自动秘境功能  
https://github.com/babalae/better-genshin-impact
4.  SGA组合使用了MAA的功能  
https://github.com/MaaAssistantArknights/MaaAssistantArknights
