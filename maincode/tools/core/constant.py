import os
import sys


class SGAConstants:
    IS_FROZEN = hasattr(sys, '_MEIPASS') or getattr(sys, 'frozen', False)
    ResourcesDir = "resources"
    PersonalDir = "personal"
    CodeDir = "maincode" if not IS_FROZEN else "_internal/maincode"
    WorkDir = os.getcwd()
    
    # 文件/目录路径
    MainConfigPath = f"{PersonalDir}/mainconfig.json"
    MainConfigBackupPath = f"{PersonalDir}/mainconfigbackup.json"
    SGAScriptDir = f"{ResourcesDir}/main/script"
    ScriptsDir = f"{CodeDir}/script"
    LogsDir = f"{PersonalDir}/logs"
    SnowJson = f"{ResourcesDir}/snow/list.json"
    SnowRollDir = f"{PersonalDir}/snow/roll"
    # URL
    GithubURL = "https://github.com/Kin-L/SucroseGameAssistant"
    GiteeURL = "https://gitee.com/huixinghen/SucroseGameAssistant"
    BilibiliURL = "https://space.bilibili.com/406315493"
    SGAWebURL = "https://kin-l.github.io/sga-instructions/index.html#guide"
    SwitcherURL = "https://www.bilibili.com/video/BV1XU411m7TT"
    
    # SGA图标
    SGATitlePic = f"{ResourcesDir}/main/SGA/title.png"
    LoadingGif = f"{ResourcesDir}/main/SGA/loading.gif"
    LoadBackPic = f"{ResourcesDir}/main/SGA/loadback.png"
    SGAdefaultPic = f"{ResourcesDir}/main/SGA/default.png"
    SGASupportPic = f"{ResourcesDir}/main/SGA/hxh.png"
    SGAICO = f"{ResourcesDir}/main/SGA/title.ico"
    KleinIcon = f"{ResourcesDir}/klein/kleinicon.png"

    # 按钮图片
    HistoryPic = f"{ResourcesDir}/main/button/history.png"
    SavePic = f"{ResourcesDir}/main/button/save.png"
    FoldPic = f"{ResourcesDir}/main/button/fold.png"
    ReducePic = f"{ResourcesDir}/main/button/reduce.png"
    RefreshPic = f"{ResourcesDir}/main/button/refresh.png"
    SupportPic = f"{ResourcesDir}/main/button/support.png"
    GithubPic = f"{ResourcesDir}/main/button/github.png"
    GiteePic = f"{ResourcesDir}/main/button/gitee.png"
    BilibiliPic = f"{ResourcesDir}/main/button/bilibili.png"
    HelpPic = f"{ResourcesDir}/main/button/help.png"
    RestartPic = f"{ResourcesDir}/main/button/refresh.png"
    ArrowDownPic = f"{ResourcesDir}/main/button/arrowdown.png"
    ArrowLeftPic = f"{ResourcesDir}/main/button/arrowleft.png"
    DeletePic = f"{ResourcesDir}/main/button/delete.png"
    UnlockPic = f"{ResourcesDir}/main/button/unlock.png"
    LockPic = f"{ResourcesDir}/main/button/lock.png"
    AddPic = f"{ResourcesDir}/main/button/add.png"
    RenamePic = f"{ResourcesDir}/main/button/rename.png"
    FinishPic = f"{ResourcesDir}/main/button/finish.png"
    HomePic = f"{ResourcesDir}/main/button/home.png"
    RightPic = f"{ResourcesDir}/main/state/right.png"
    StopPic = f"{ResourcesDir}/main/state/stop.png"
    ErrorPic = f"{ResourcesDir}/main/state/error.png"
    SetPic = f'{ResourcesDir}/main/button/set.png'
    Command = f"{ResourcesDir}/main/button/command.png"

    CACHE_DIR = "cache"
    SCRIPT_DIR = f"{PersonalDir}/script"
    SCHTASKS_SRC = f"{ResourcesDir}/main/schtasks.json"
    SCHTASKS_DST = f"{PersonalDir}/schtasks.json"
    BAT_SRC = f"{ResourcesDir}/main/script/start-SGA.bat"
    BAT_DST = f"{PersonalDir}/script/start-SGA.bat"
    MAA_BAT_SRC = f"{ResourcesDir}/main/script/maacreate.bat"
    MAA_BAT_DST = f"{PersonalDir}/script/maacreate.bat"
    VBS_SRC = f"{ResourcesDir}/main/script/start-SGA.vbs"
    VBS_DST = f"{PersonalDir}/script/start-SGA.vbs"


spr = SGAConstants()


class SnowConstants:
    SnowDir = f"{spr.ResourcesDir}/snow"
    HomePic = f"{SnowDir}/picture/home.png"


spr.snow = SnowConstants()
