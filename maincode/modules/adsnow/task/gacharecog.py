import json
import time
import shutil
from os import path, makedirs, startfile, getcwd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from maincode.tools.core.constant import spr

HomePic = spr.snow.HomePic


def snowGachaRecog(self):
    """
    获取尘白禁区游戏的抽卡记录并导出到Excel

    功能：
    1. 进入抽卡记录界面
    2. 遍历所有选中的卡池类型
    3. 识别并记录抽卡结果
    4. 导出到Excel文件并进行数据统计
    """
    self.send("开始获取抽卡记录")

    # 进入抽卡记录界面
    self.ctler.clickChange((1655, 606), zone=(1525, 573, 1611, 624))
    self.ctler.waitTo(HomePic, (1504, 0, 1771, 117))

    # 初始化抽卡记录数据结构
    gacha_records = {
        "特选角色共鸣": [],
        "特选武器共鸣": [],
        "限定角色共鸣": [],
        "限定武器共鸣": [],
        "常守之誓": [],
        "中庭炉心": [],
        "新手池": []
    }

    # 检查是否至少选择了一个卡池
    if not any(self.para["GachaList"]):
        self.send("共鸣记录：请至少勾选一个卡池选项")
        return True

    # 获取选中的卡池列表
    selected_pools = _get_selected_pools(self.para["GachaList"])

    # 遍历所有选中的卡池并获取记录
    for pool_name in selected_pools:
        _process_gacha_pool(self, pool_name, gacha_records)

    # 返回主页并整理记录
    self.ctler.clickChange(target=HomePic, zone=(1504, 0, 1771, 117))
    self.ctler.wait(0.5)
    self.send("获取抽卡记录完成")

    # 导出记录到Excel
    export_gacha_records(self, gacha_records)


def _get_selected_pools(gacha_list):
    """根据配置获取选中的卡池列表"""
    pool_names = [
        "特选角色共鸣", "特选武器共鸣", "限定角色共鸣",
        "限定武器共鸣", "常守之誓", "中庭炉心", "新手池"
    ]

    selected_pools = []
    for i, is_selected in enumerate(gacha_list):
        if is_selected and i < len(pool_names):
            selected_pools.append(pool_names[i])

    return selected_pools


def _process_gacha_pool(self, pool_name, gacha_records):
    """处理单个卡池的记录获取"""
    # 进入对应的卡池界面
    _enter_gacha_pool(self, pool_name)

    # 打开记录页面
    self.ctler.clickChange((1877, 141), zone=(1858, 117, 1903, 163))
    self.ctler.wait(0.5)
    self.ctler.clickChange((1081, 84), zone=(379, 177, 579, 215))

    # 等待记录加载完成
    if not _wait_for_records_loaded(self):
        self.send(f"{pool_name}: 获取共鸣记录等待超时")
        raise RuntimeError("尘白禁区: 获取共鸣记录等待超时")

    # 读取当前页面的记录
    pool_records = _read_current_pool_records(self)
    gacha_records[pool_name].extend(pool_records)

    # 返回卡池选择界面
    self.ctler.clickChange((1851, 81), zone=(1834, 64, 1872, 103))
    self.ctler.wait(1)


def _enter_gacha_pool(self, pool_name):
    """进入指定的卡池界面"""
    # 查找常守入口（基础入口）
    changshou_pos = self.ctler.findtext("常守", (3, 67, 280, 1066))

    if pool_name == "特选角色共鸣":
        self.ctler.clickTo(changshou_pos, "出", (377, 227, 490, 292))
        x, y = self.ctler.findtext("100", (3, 67, 280, 1066))
        self.ctler.clickChange((x - 90, y + 35), zone=(349, 854, 389, 897))
        self.ctler.clickTo((x - 90, y + 120), "角色", (465, 959, 702, 1002))

    elif pool_name == "特选武器共鸣":
        self.ctler.clickTo(changshou_pos, "出", (377, 227, 490, 292))
        x, y = self.ctler.findtext("100", (3, 67, 280, 1066))
        self.ctler.clickChange((x - 90, y + 35), zone=(349, 854, 389, 897))
        self.ctler.clickTo((x - 90, y + 210), "武器", (465, 959, 702, 1002))

    elif pool_name == "限定角色共鸣":
        self.ctler.clickTo(changshou_pos, "出", (377, 227, 490, 292))
        x, y = self.ctler.findtext("50", (3, 67, 280, 1066))
        self.ctler.clickChange((x - 90, y + 35), zone=(349, 854, 389, 897))
        self.ctler.clickTo((x - 90, y + 120), "角色", (494, 994, 645, 1035))

    elif pool_name == "限定武器共鸣":
        self.ctler.clickTo(changshou_pos, "出", (377, 227, 490, 292))
        x, y = self.ctler.findtext("50", (3, 67, 280, 1066))
        self.ctler.clickChange((x - 90, y + 35), zone=(349, 854, 389, 897))
        self.ctler.clickTo((x - 90, y + 210), "武器", (494, 994, 645, 1035))

    elif pool_name == "常守之誓":
        self.ctler.clickTo(changshou_pos, "出", (377, 227, 490, 292))

    elif pool_name == "中庭炉心":
        zhongting_pos = self.ctler.findtext("中庭炉心", (3, 67, 280, 1066))
        self.ctler.clickTo(zhongting_pos, "出", (377, 227, 490, 292))

    elif pool_name == "新手池":
        qicheng_pos = self.ctler.findtext("启程", (3, 67, 280, 1066))
        if qicheng_pos:
            self.ctler.clickTo(qicheng_pos, "到", (324, 71, 500, 129))

    self.ctler.wait(0.5)


def _wait_for_records_loaded(self):
    """等待抽卡记录加载完成"""
    check_count = 0
    timeout_counter = 0

    while timeout_counter < 200:  # 20秒超时
        self.ctler.wait(0.1)

        # 检查记录加载完成的图片标识
        if self.ctler.findpic("resources/snow/picture/rollcheck.png")[1]:
            check_count = 0  # 重置计数
        else:
            check_count += 1

        # 连续4次检查不到标识则认为加载完成
        if check_count >= 4:
            return True

        timeout_counter += 1

    return False


def _read_current_pool_records(self):
    """读取当前卡池的所有记录"""
    all_records = []
    page_count = 0

    while True:
        try:
            # 尝试点击下一页
            self.ctler.clickChange((1666, 602), zone=(1635, 488, 1716, 555), wait=(0.6, 3))
        except TimeoutError:
            break  # 没有更多页面

        # 截图并识别记录
        screenshot = self.ctler.screenshot()
        item_names = self.ctler.ocr((357, 185, 685, 866), screenshot, 1)
        item_dates = self.ctler.ocr((1357, 185, 1561, 866), screenshot, 1)

        page_count += 1
        duplicate_count = 0
        current_page_records = []

        # 处理当前页的记录
        for idx, (name_row, date_row) in enumerate(zip(item_names, item_dates)):
            name = name_row[0].strip()
            if not name:
                break  # 空行，结束当前页

            date = date_row[0]
            # 处理日期格式（添加空格分隔）
            if len(date) > 10 and date[10] != " ":
                date = date[:10] + " " + date[10:]

            # 识别稀有度颜色
            rarity = _detect_item_rarity(self, idx, screenshot)

            record = [name, date, rarity]
            current_page_records.append(record)

            # 检查是否与上一页重复（去重）
            if page_count > 1 and idx < len(all_records) and record[:2] == all_records[idx][:2]:
                duplicate_count += 1

        # 添加当前页记录到总记录
        all_records = current_page_records + all_records

        # 如果整页都是重复记录，停止翻页
        if duplicate_count >= 10:
            break

        # 继续翻页
        self.ctler.click((1666, 602))
        self.ctler.wait(0.6)

    return all_records


def _detect_item_rarity(self, item_index, screenshot):
    """检测物品的稀有度"""
    # 定义检测区域（根据物品索引）
    detect_zone = (342, 216 + 68 * item_index, 362, 216 + 68 * item_index + 5)

    # 检测颜色对应的稀有度
    if self.ctler.findcolor("3662F2", detect_zone, screenshot):  # 蓝色
        return "blue"
    elif self.ctler.findcolor("C069D6", detect_zone, screenshot):  # 紫色
        return "purple"
    elif self.ctler.findcolor("EA9B36", detect_zone, screenshot):  # 橙色
        return "orange"
    else:
        return "unknown"


def _normalize_item_name(item_name):
    """标准化物品名称"""
    name_mappings = {
        "日王牌": "晴-旧日王牌",
        "芬妮": "芬妮-咎冠",
        "琴诺": "琴诺-悖谬",
        "不予显示": "安卡希雅-[不予显示]",
        "热年代": "灸热年代",
        "姐姐大人": "恩雅-姐姐大人",
        "王权连": "王权连枷",
        "瑞斯": "瑟瑞斯-瞬刻",
        "九夜之": "九夜之冕",
        "龙舌兰": "薇蒂雅-龙舌兰"
    }

    for keyword, normalized_name in name_mappings.items():
        if keyword in item_name:
            return normalized_name

    return item_name


def export_gacha_records(self, gacha_records):
    """导出抽卡记录到Excel文件"""
    # 创建时间戳
    timestamp = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

    # 保存原始JSON记录
    cache_dir = "personal/snow/roll/cache"
    if not path.exists(cache_dir):
        makedirs(cache_dir)

    json_path = f"{cache_dir}/history - {timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(gacha_records, f, ensure_ascii=False, indent=2)

    self.send("抽卡记录已暂存")

    # 准备Excel模板
    _prepare_excel_template()

    # 创建Excel文件
    excel_path = path.join(getcwd(), f"personal/snow/roll/尘白禁区共鸣记录 - {timestamp}.xlsx")
    _create_gacha_excel(gacha_records, excel_path, timestamp)

    self.send("共鸣记录已导出", 3)

    # 可选：自动打开Excel文件
    if self.para["GachaOpenSheet"]:
        startfile(excel_path)


def _prepare_excel_template():
    """准备Excel模板文件"""
    zip_path = path.join(getcwd(), "resources/snow/default.zip")
    template_path = path.join(getcwd(), "resources/snow/default.xlsx")

    if not path.exists(template_path):
        from shutil import unpack_archive
        unpack_archive(zip_path, path.join(getcwd(), "resources/snow"))


def _create_gacha_excel(gacha_records, excel_path, timestamp):
    """创建包含抽卡记录的Excel文件"""
    # 复制模板文件
    template_path = path.join(getcwd(), "resources/snow/default.xlsx")
    shutil.copyfile(template_path, excel_path)

    # 加载工作簿并设置样式
    wb = load_workbook(excel_path)
    _setup_excel_styles(wb, gacha_records)

    # 保存文件
    wb.save(excel_path)


def _setup_excel_styles(wb, gacha_records):
    """设置Excel样式并填充数据"""
    # 定义字体样式
    font_normal = Font(name='宋体', size=12)
    font_blue = Font(name='宋体', size=12, color="3374F8")
    font_purple = Font(name='宋体', size=12, color="7E30FF", bold=True)
    font_orange = Font(name='宋体', size=12, color="FFC332", bold=True)

    alignment_center = Alignment(horizontal='center', vertical='center')

    # 各卡池的统计信息
    pool_stats = []
    pool_names = ["特选角色共鸣", "特选武器共鸣", "限定角色共鸣", "限定武器共鸣", "常守之誓", "中庭炉心", "新手池"]

    for pool_name in pool_names:
        records = gacha_records[pool_name]
        sheet = wb[pool_name]

        stats = _process_pool_records(sheet, records, font_normal, font_blue,
                                      font_purple, font_orange, alignment_center)
        pool_stats.append(stats)

    # 更新总览表
    _update_summary_sheet(wb, pool_stats, pool_names)


def _process_pool_records(sheet, records, font_normal, font_blue, font_purple, font_orange, alignment):
    """处理单个卡池的记录并返回统计信息"""
    row_count = 1
    purple_count_since_last_orange = 0
    orange_count_since_last_orange = 0

    stats = {
        'blue_count': 0,
        'purple_count': 0,
        'orange_count': 0,
        'total_count': 0,
        'pity_count': 0,
        'purple_history': [],
        'orange_history': []
    }

    for record in records:
        name, date, rarity = record
        row_count += 1

        # 标准化名称
        normalized_name = _normalize_item_name(name)

        # 更新计数
        if rarity == "blue":
            stats['blue_count'] += 1
            font = font_blue
        elif rarity == "purple":
            stats['purple_count'] += 1
            purple_count_since_last_orange += 1
            stats['purple_history'].append(f"{normalized_name}({purple_count_since_last_orange})")
            purple_count_since_last_orange = 0
            font = font_purple
        elif rarity == "orange":
            stats['orange_count'] += 1
            orange_count_since_last_orange += 1
            stats['orange_history'].append(f"{normalized_name}({orange_count_since_last_orange})")
            orange_count_since_last_orange = 0
            purple_count_since_last_orange = 0  # 重置紫计数
            font = font_orange
        else:
            font = font_normal

        # 填充单元格
        sheet[f"A{row_count}"] = date
        sheet[f"B{row_count}"] = normalized_name
        sheet[f"C{row_count}"] = row_count - 1  # 总序号
        sheet[f"D{row_count}"] = orange_count_since_last_orange  # 当前保底计数

        # 设置样式
        for col in ['A', 'B', 'C', 'D']:
            cell = sheet[f"{col}{row_count}"]
            cell.alignment = alignment
            cell.font = font if col in ['A', 'B'] else font_normal

        sheet.row_dimensions[row_count].height = 18

    # 最终统计
    stats['total_count'] = row_count - 1
    stats['pity_count'] = orange_count_since_last_orange

    return stats


def _update_summary_sheet(wb, pool_stats, pool_names):
    """更新总览表的数据"""
    sheet = wb["总览"]

    # 定义各卡池在总览表中的起始行
    pool_start_rows = [3, 6, 9, 12, 15, 18, 21]

    for i, (stats, start_row) in enumerate(zip(pool_stats, pool_start_rows)):
        if i >= len(pool_names):
            break

        # 更新基础统计
        sheet[f"B{start_row}"] = stats['blue_count']
        sheet[f"C{start_row}"] = stats['purple_count']
        sheet[f"D{start_row}"] = stats['orange_count']
        sheet[f"E{start_row}"] = stats['total_count']
        sheet[f"F{start_row}"] = stats['pity_count']

        # 更新历史记录
        purple_history_row = start_row - 1
        orange_history_row = start_row

        sheet[f"I{purple_history_row}"] = " ".join(stats['purple_history'])
        sheet[f"I{orange_history_row}"] = " ".join(stats['orange_history'])
