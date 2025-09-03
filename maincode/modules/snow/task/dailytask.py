from maincode.tools.core.logger import logger
from maincode.config.configctrl import scc


def snowDailyTask(self):
    """
    执行游戏的日常任务流程

    包含功能：
    1. 角色故事任务
    2. 商店购物
    3. 武器升级
    4. 模拟战扫荡
    """
    # 角色故事任务处理
    if self.para["StoryEnable"]:
        _process_story_tasks(self)

    # 商店购物处理
    if self.para["ShopEnable"]:
        _process_shop_tasks(self)

    # 武器升级处理
    if self.para["WeaponUp"]:
        _process_weapon_upgrade(self)

    # 模拟战扫荡处理
    if self.para["Simulation"]:
        _process_simulation_battle(self)


def _process_story_tasks(self):
    """处理角色故事任务"""
    # 点击进入故事界面
    self.ctler.clickChange((1690, 470), zone=(1552, 468, 1626, 515))
    self.ctler.wait(0.5)

    # 选择个人故事
    self.ctler.clickChange(target="个人", zone=(733, 812, 947, 891))

    used_packages = 0  # 已使用的补给包数量

    # 遍历所有选中的角色故事
    for character_name in self.para["StoryList"]:
        if character_name == "未选择":
            continue

        # 等待进入行动界面
        self.ctler.waitTo("行动", (357, 1000, 474, 1051))

        # 处理角色名称缩写映射
        char_abbreviation = _get_character_abbreviation(character_name)

        # 查找角色位置
        character_found, character_pos, should_continue = _find_character_position(
            self, char_abbreviation, character_name
        )

        if should_continue:
            continue

        if not character_found:
            break  # 角色未找到，退出循环

        # 检查记忆嵌片数量
        memory_chip_count = _check_memory_chips(self)
        if memory_chip_count is None:
            break  # 识别异常，退出循环

        # 处理记忆嵌片不足的情况
        if not _handle_memory_chips_shortage(self, memory_chip_count, used_packages):
            break

        # 执行角色故事任务
        _execute_story_task(self, character_pos, character_name)

        # 返回主页
        self.ctler.pressTo("esc", "resources/snow/picture/home.png", (1504, 0, 1771, 117))

    # 返回任务界面
    self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    self.ctler.wait(0.5)


def _get_character_abbreviation(full_name):
    """获取角色名称的缩写"""
    abbreviation_map = {
        "缄默": "默",
        "咎冠": "冠",
        "悖谬": "谬",
        "魔术师": "术师",
        "驰掣": "驰",
        "冥河代理人": "代理",
        "绯月": "月"
    }
    return abbreviation_map.get(full_name, full_name)


def _find_character_position(self, abbreviation, character_name):
    """查找角色在界面中的位置"""
    character_pos = None
    ocr_results = []

    # 滚动查找角色，最多尝试8次
    for attempt in range(8):
        # 执行OCR识别
        ocr_result = self.ctler.ocr((0, 731, 1417, 858), mode=1)
        ocr_results.append([attempt, ocr_result])

        # 查找角色名称
        position = self.ctler.StrFind(abbreviation, ocr_result)

        if position:
            character_pos = position
            # 检查任务是否已完成
            x, y = self.ctler.convertR(position)
            status_text = self.ctler.ocr((x + 247, 177, x + 447, 233))[0]

            if len(status_text) >= 3 and status_text[-3] == "0":
                self.send(f"今日已完成：角色 {character_name}")
                return None, None, True  # 已完成的标志
            elif len(status_text) >= 3 and status_text[-3] != "1":
                return character_pos, None, False  # 需要清理的标志
            break
        else:
            # 未找到角色，滚动页面
            if attempt == 7:
                self.ctler.roll((1002, 581), 70000, True)
                self.ctler.wait(0.8)
                self.send(f"未识别到角色: {character_name}")
                logger.debug(f"OCR结果: {ocr_results}")
                scc.info.TaskError = True
                return None, None, True
            else:
                self.ctler.roll((1002, 581), -5620, True)
                self.ctler.wait(0.8)

    return character_pos, None, False


def _check_memory_chips(self):
    """检查记忆嵌片数量"""
    screenshot = self.ctler.screenshot()
    chip_text = self.ctler.ocr((1459, 27, 1540, 77), screenshot)[0]
    chip_parts = chip_text.split("/")

    if chip_parts and chip_parts[0].strip().isdigit():
        return int(chip_parts[0].strip())
    else:
        self.send("记忆嵌片数量识别异常")
        screenshot_path = self.ctler.SaveShot(screenshot, "")
        logger.error(f"识别文本: {chip_text}")
        logger.error(f"截图保存路径: {screenshot_path}")
        return None


def _handle_memory_chips_shortage(self, chip_count, used_packages):
    """处理记忆嵌片不足的情况"""
    if chip_count == 0 and self.para["StoryUsePackage"] and used_packages < 2:
        # 使用补给包
        try:
            self.ctler.clickChange((1566, 51), zone=(1547, 38, 1584, 69),
                                   wait=(0.8, 5), errsc=False)
            used_packages += 1
            return True
        except TimeoutError:
            self.send("补给包不足")
            return False
    elif chip_count <= 2:
        self.send(f"记忆嵌片不足: {chip_count}")
        return False

    return True


def _execute_story_task(self, position, character_name):
    """执行角色故事任务"""
    x, y = self.ctler.convertR(position)

    # 点击角色开始任务
    self.ctler.clickChange((x, 900), zone=(858, 801, 1072, 875))

    # 如果需要清理，点击清理按钮
    # 这里需要根据实际情况判断是否需要清理
    # self.ctler.clickChange((1168, 718), zone=(875, 685, 945, 749))

    # 点击开始按钮
    self.ctler.clickChange(target="开始", zone=(858, 801, 1072, 875))

    self.send(f"完成:个人故事 {character_name}")


def _process_shop_tasks(self):
    """处理商店购物任务"""
    # 进入商店
    self.ctler.clickChange(target="商店", zone=(1756, 997, 1852, 1061))
    self.ctler.roll((1241, 380), -2000)
    self.ctler.wait(0.5)

    # 遍历购物列表
    for item in self.para["ShopList"]:
        use_multiple = False
        item_name = item

        # 处理批量购买标识
        if "×" in item:
            item_name = item.split("×")[0]
            use_multiple = True

        # 查找商品位置
        position = self.ctler.findtext(item_name, (323, 213, 1860, 1003))
        if position:
            # 点击商品
            self.ctler.clickChange(position, zone=(1723, 981, 1840, 1044))

            # 处理批量购买
            if use_multiple:
                self.ctler.clickChange((1832, 853), zone=(1545, 834, 1582, 874))
            break

    # 返回主页
    self.ctler.clickChange((1782, 1014), zone=(1504, 0, 1771, 117))

    # 确认返回主页
    if not self.SnowHome(self):
        raise TimeoutError("返回主页超时")

    self.send("完成:商店购物")


def _process_weapon_upgrade(self):
    """处理武器升级任务"""
    # 进入背包
    self.ctler.clickChange(target="背包", zone=(1599, 994, 1692, 1063))
    self.ctler.wait(0.5)

    # 排序操作
    self.ctler.clickChange((73, 1025), zone=(50, 1011, 111, 1056))
    self.ctler.wait(0.5)
    self.ctler.clickChange((585, 327), zone=(625, 303, 681, 349))
    self.ctler.clickChange((585, 327), zone=(625, 303, 681, 349))
    self.ctler.clickChange((1316, 840), zone=(1302, 798, 1435, 893))

    # 武器升级流程
    self.ctler.clickChange((425, 191), zone=(50, 1011, 111, 1056))
    self.ctler.clickChange((985, 774), zone=(50, 1011, 111, 1056))
    self.ctler.clickChange((181, 300), zone=(123, 263, 248, 332))

    # 等待升级按钮出现并点击
    upgrade_pos = self.ctler.waitTo("升级", (1691, 981, 1818, 1053))
    self.ctler.clickChange((1383, 717), zone=(123, 263, 248, 332))
    self.ctler.clickChange((119, 168), zone=(1341, 675, 1431, 766))
    self.ctler.clickChange(upgrade_pos, zone=(1691, 981, 1818, 1053))

    self.send("完成:武器升级")

    # 返回任务界面
    self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    self.ctler.wait(0.5)


def _process_simulation_battle(self):
    """处理模拟战扫荡任务"""
    # 进入特别界面
    self.ctler.clickChange((1690, 470), zone=(1552, 468, 1626, 515))
    self.ctler.clickChange(target="特别", zone=(157, 464, 425, 560))

    # 等待精神界面出现
    pos = self.ctler.waitTo("精神", (150, 770, 1779, 848))
    x, y = self.ctler.convertR(pos)
    self.ctler.clickChange((x, 462), zone=(61, 998, 245, 1059))

    completed_count = 0

    # 遍历不同的模拟战位置
    for position in [(224, 253), (216, 394)]:
        self.ctler.click(position)
        self.ctler.wait(0.8)

        # 尝试快速扫荡
        for _ in range(4):
            if completed_count >= 4:
                break

            # 检查快速按钮是否存在
            ocr_result = self.ctler.ocr((1351, 977, 1512, 1052))[0]
            if "快速" in ocr_result:
                self.ctler.clickChange((1415, 999), zone=(1358, 964, 1548, 1071))
                self.ctler.wait(0.5)
                self.ctler.clickChange((1375, 773), zone=(1358, 964, 1548, 1071))
                self.ctler.wait(0.5)
                completed_count += 1
                self.send("拟境扫荡一次")
            else:
                break

    self.ctler.wait(0.5)

    # 检查并领取评测奖励
    if self.ctler.findcolor("FFFF8B", (188, 869, 195, 876)):
        self.ctler.clickChange((137, 914), zone=(16, 51, 240, 128))
        self.ctler.clickChange((1742, 1001), zone=(1670, 971, 1830, 1022))
        self.send("领取评测奖励")

    # 返回任务界面
    self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    self.ctler.wait(0.5)