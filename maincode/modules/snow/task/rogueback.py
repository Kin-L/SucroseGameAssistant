import time
import keyboard
from PyQt5.QtCore import QThread


def snowRogue(self):
    """
    执行验证战场（Rogue-like模式）的自动化流程

    功能：
    1. 检查是否在正确界面
    2. 选择难度并开始战斗
    3. 自动触发技能（E键）
    4. 处理战斗奖励选择
    5. 处理战斗结束流程
    """
    # 检查是否在验证战场界面
    if not _is_in_rogue_interface(self):
        self.send("请先进入验证战场界面")
        return

    self.send("开始验证战场")

    # 创建并启动技能触发线程
    skill_trigger = SkillTriggerThread()

    try:
        # 主循环处理多次战斗
        _process_rogue_battles(self, skill_trigger)

    except Exception as error:
        # 异常处理
        _handle_rogue_exception(self, skill_trigger, error)
        raise

    finally:
        # 确保线程被正确清理
        if skill_trigger.isRunning():
            skill_trigger.stop()
            skill_trigger.quit()
            skill_trigger.wait()
            skill_trigger.deleteLater()


def _is_in_rogue_interface(self):
    """检查是否在验证战场难度选择界面"""
    ocr_result = self.ctler.ocr(mode=1)
    return self.ctler.StrFind("难度选择", ocr_result) is not None


def _process_rogue_battles(self, skill_trigger):
    """处理验证战场的多次战斗流程"""
    # 难度对应的坐标位置
    DIFFICULTY_COORDINATES = [
        (383, 400),  # 难度0
        (767, 404),  # 难度1
        (1161, 427),  # 难度2
        (1541, 443)  # 难度3
    ]

    while True:
        # 选择难度并开始战斗
        if not _select_difficulty_and_start(self, DIFFICULTY_COORDINATES):
            break

        # 处理战斗确认对话框
        _handle_confirmation_dialog(self)

        # 进入战斗主循环
        _battle_main_loop(self, skill_trigger)


def _select_difficulty_and_start(self, difficulty_coords):
    """选择难度并开始战斗"""
    try:
        # 获取选择的难度坐标
        selected_difficulty = self.para["roguediff"]
        if selected_difficulty >= len(difficulty_coords):
            self.send(f"无效的难度选择: {selected_difficulty}")
            return False

        # 点击难度选择
        difficulty_pos = difficulty_coords[selected_difficulty]
        self.ctler.clickChange(difficulty_pos, zone=(102, 22, 301, 84))

        # 点击开始按钮
        self.ctler.clickChange(target="开始", zone=(1694, 944, 1885, 1051))
        self.ctler.wait(1)

        return True

    except TimeoutError:
        # 检查是否次数已用完
        ocr_result = self.ctler.ocr(mode=1)
        if self.ctler.StrFind("难度选择", ocr_result):
            self.send("今日悖论迷宫次数已消耗殆尽")
            self.send("验证战场结束")
            return False
        else:
            raise TimeoutError("选择难度超时")


def _handle_confirmation_dialog(self):
    """处理开始战斗前的确认对话框"""
    ocr_result = self.ctler.ocr(mode=1)
    if self.ctler.StrFind("确定", ocr_result):
        self.ctler.clickChange(target="确定", zone=(1365, 719, 1580, 816))
    self.ctler.wait(3)


def _battle_main_loop(self, skill_trigger):
    """战斗主循环处理"""
    # 奖励选择区域的坐标
    REWARD_ZONES = [
        (106, 781, 597, 881),  # 奖励区域1
        (804, 799, 1113, 850),  # 奖励区域2
        (1428, 800, 1745, 852)  # 奖励区域3
    ]

    REWARD_CLICK_POSITIONS = [
        (329, 829),  # 对应区域1的点击位置
        (972, 822),  # 对应区域2的点击位置
        (1561, 826)  # 对应区域3的点击位置
    ]

    while True:
        screenshot = self.ctler.screenshot()

        # 检查波数显示，启动技能触发
        wave_text = self.ctler.ocr((33, 65, 146, 122), screenshot)[0]
        if "波" in wave_text and not skill_trigger.isRunning():
            skill_trigger.stop_flag = False
            skill_trigger.start()

        # 检查确认按钮（奖励选择）
        confirm_text = self.ctler.ocr((901, 963, 1013, 1036), screenshot)[0]
        if "确认" in confirm_text:
            _handle_reward_selection(self, skill_trigger, REWARD_ZONES, REWARD_CLICK_POSITIONS)

        # 检查退出按钮（战斗结束）
        elif "退出" in confirm_text:
            _handle_battle_exit(self, skill_trigger)
            break

        else:
            self.ctler.wait(0.5)


def _handle_reward_selection(self, skill_trigger, reward_zones, click_positions):
    """处理战斗奖励选择"""
    # 停止技能触发
    skill_trigger.stop_flag = True
    skill_trigger.quit()
    skill_trigger.wait()

    self.ctler.wait(0.3)
    screenshot = self.ctler.screenshot()

    # 查找空奖励槽位
    empty_slot_position = None
    for zone, click_pos in zip(reward_zones, click_positions):
        zone_text = self.ctler.ocr(zone, screenshot)[0]
        if not zone_text.strip():  # 空槽位
            empty_slot_position = click_pos
            break

    # 默认选择第一个位置
    if empty_slot_position is None:
        empty_slot_position = click_positions[0]

    # 选择奖励流程
    _select_reward_process(self, empty_slot_position)


def _select_reward_process(self, click_position):
    """执行奖励选择流程"""
    while True:
        # 点击奖励位置
        self.ctler.click(click_position)
        self.ctler.wait(0.3)

        # 点击确认按钮
        self.ctler.click((965, 1008))
        self.ctler.wait(0.5)

        # 检查对话框类型
        dialog_text = self.ctler.ocr((231, 955, 1053, 1050))[0]

        if "确认" in dialog_text:
            continue  # 继续选择

        elif "丢弃" in dialog_text:
            # 处理丢弃确认
            self.ctler.click((1298, 677))
            self.ctler.wait(0.3)

            try:
                # 尝试点击确定按钮
                self.ctler.clickChange((1566, 988), zone=(1503, 955, 1623, 1019))
            except Exception:
                # 备选方案
                self.ctler.click((311, 993))
                self.ctler.wait(0.3)
                self.ctler.clickChange(target="确定", zone=(1356, 733, 1552, 800))
            break

        else:
            break  # 其他情况退出循环


def _handle_battle_exit(self, skill_trigger):
    """处理战斗退出流程"""
    # 停止技能触发
    skill_trigger.stop_flag = True
    skill_trigger.quit()
    skill_trigger.wait()

    # 点击退出按钮
    self.ctler.clickChange(target="退出", zone=(896, 946, 1004, 1018))

    # 等待返回选择界面
    self.ctler.waitTo(target="选", zone=(73, 8, 328, 92), wait=(1, 30))


def _handle_rogue_exception(self, skill_trigger, error):
    """处理验证战场异常"""
    self.send(f"验证战场执行异常: {error}")

    if skill_trigger.isRunning():
        skill_trigger.stop_flag = True
        skill_trigger.quit()
        skill_trigger.wait()
        skill_trigger.deleteLater()


class SkillTriggerThread(QThread):
    """
    技能自动触发线程
    在战斗过程中自动按E键释放技能
    """

    def __init__(self):
        super().__init__()
        self.stop_flag = False

    def run(self):
        """
        线程主循环
        每0.8秒触发一次E键，直到被停止
        """
        while not self.stop_flag:
            try:
                keyboard.send("e")
                time.sleep(0.8)
            except Exception as e:
                # 键盘操作异常，退出循环
                break

    def stop(self):
        """停止线程"""
        self.stop_flag = True
