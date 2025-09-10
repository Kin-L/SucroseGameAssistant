from maincode.config.configctrl import scc
from maincode.config.mainconfig import TimerConfigClass
from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.logger import logger
from maincode.mainwindows.timer.function import ApplyTimer


def currentsave(self):
    """
    保存当前模块配置到主配置中

    功能：
    1. 获取当前选中的模块索引
    2. 提取模块配置信息
    3. 更新主配置的当前配置和额外配置
    """
    # 获取当前选中的模块索引
    current_index = self.module.widget.boxmodule.currentIndex()

    # 获取模块的关键信息
    module_infos = scc.modules.GetInfos()
    module_key = module_infos[current_index][2]  # 获取模块标识键

    # 构建基础配置字典
    base_config = {
        'ModuleKey': module_key,
        'ConfigKey': "",  # 配置键为空（主配置）
        'ConfigName': "默认配置"  # 默认配置名称
    }

    # 收集当前模块的配置
    module_widgets = scc.modules.GetWidgets()
    module_config = module_widgets[current_index].CollectConfig()

    # 合并配置，优先使用模块配置
    merged_config = module_config.copy()
    merged_config.update(base_config)

    # 处理额外配置（如果有）
    other_config = merged_config.pop("OtherConfig", {})
    if other_config:
        scc.mc.OtherConfig.update(other_config)

    # 更新主配置的当前配置
    scc.mc.CurrentConfig = merged_config


def subconfigsave(self):
    """
    保存子配置到配置文件

    功能：
    1. 构建子配置信息
    2. 合并当前配置和子配置信息
    3. 保存到子配置列表并更新相关信息
    """
    # 构建子配置标识信息
    subconfig_info = {
        'ConfigKey': scc.mc.ConfigKey,  # 使用主配置的ConfigKey
        'ConfigName': self.module.widget.ecbconfig.text().strip()  # 清理空白字符
    }

    # 复制当前配置并更新子配置信息
    current_config_copy = scc.mc.CurrentConfig.copy()
    current_config_copy.update(subconfig_info)

    # 保存子配置
    scc.sc.Save(current_config_copy)

    # 更新子配置列表中的模块键信息
    config_key = current_config_copy['ConfigKey']
    item_index = scc.sc.FindItem(config_key)[-1]  # 获取配置项索引

    if 0 <= item_index < len(scc.sc.filelist):
        list(scc.sc.filelist[item_index])[2] = current_config_copy['ModuleKey']


def SaveConfig(self):
    """
    自动保存配置（在UI加载完成时调用）

    功能：
    1. 检查UI是否加载完成
    2. 保存当前配置和定时器配置
    3. 如果配置有变化，保存主配置和备份
    """
    if not self.LoadUI:
        return  # UI未加载完成，直接返回

    # 保存当前模块配置
    self.currentsave()

    # 收集并保存定时器配置
    timer_config_data = self.overall.widget.timer.CollectConfig()
    scc.mc.TimerConfig = TimerConfigClass(**timer_config_data)

    # 检查配置是否有变化
    current_config_dump = scc.mc.model_dump()
    if current_config_dump != scc.currentmainconfig:
        scc.SaveMain()  # 保存主配置
        scc.SaveBackUp()  # 创建备份
        scc.currentmainconfig = current_config_dump  # 更新当前配置缓存


def ManualSaveConfig(self):
    """
    手动保存配置（用户触发）

    功能：
    1. 检查保存条件
    2. 根据设置选项执行不同的保存逻辑
    3. 处理保存过程中的异常
    4. 提供操作反馈信息
    """
    # 检查保存条件：UI已加载且定时器允许操作
    if not (self.LoadUI and self.timerallow):
        return

    try:
        # 开始信息记录
        self.infoHead()

        # 根据设置选项执行不同的保存逻辑
        if self.mainwidget.sksetting.currentIndex() != 0:  # 非第一个选项卡
            # 保存当前配置和子配置
            self.currentsave()
            self.subconfigsave()
            self.infoAdd("保存成功", False)
        else:
            # 第一个选项卡：处理定时器配置
            try:
                # 收集并验证定时器配置
                timer_config_data = self.overall.widget.timer.CollectConfig()
                scc.mc.TimerConfig = TimerConfigClass(**timer_config_data)

                # 应用定时器设置
                if ApplyTimer():
                    self.infoAdd("应用SGA定时自启/唤醒", False)
                else:
                    self.infoAdd("取消SGA自启/唤醒行为", False)

            except Exception as timer_error:
                # 定时器操作异常处理
                error_details = GetTracebackInfo(timer_error)
                error_message = f"{error_details}操作异常：更改SGA定时自启/唤醒"
                logger.error(error_message)
                self.infoAdd("操作异常：更改SGA定时自启/唤醒", False)

        # 结束信息记录
        self.infoEnd()

    except Exception as general_error:
        # 全局异常处理
        error_details = GetTracebackInfo(general_error)
        error_message = f"{error_details}手动保存流程异常"
        logger.error(error_message)
        self.infoAdd("手动保存流程异常", False)  # 添加错误信息参数
