from os import path, makedirs
import json
from sgacode.tools.main import env, DictListType
from shutil import copyfile


class ScheMa(dict):
    def __init__(self, schema: dict):
        super().__init__(schema)

    def typedict(self):
        return {key: _dict['type'] for key, _dict in self.items()}


class ConfigTool(dict):
    ConfigFolderPath = "personal/config"
    ExampleModuleScheMa = {
        'ConfigKey': {'type': str, 'default': ""},  # 每个配置文件的识别码，每个文件唯一
        'ModuleKey': {'type': int, 'default': 0},  # 每个模块的识别码，每个模块唯一
        'ConfigName': {'type': str, 'default': "默认配置"}}  # 每个配置文件的名字，不唯一

    def __init__(self, schema: ScheMa):
        super().__init__()
        self.schema: ScheMa = schema

    def getdefault(self) -> dict:
        """
        根据schema规范生成默认字典
        :return: 包含默认值的字典
        """
        default_dict = {}
        for field, config in self.schema.items():
            if 'default' in config:
                default_dict[field] = config['default']
            elif config.get('required', True):
                # 为必填字段但没有默认值的字段生成默认值
                field_type = config.get('type')
                if field_type == str:
                    default_dict[field] = ""
                elif field_type == int:
                    default_dict[field] = 0
                elif field_type == float:
                    default_dict[field] = 0.0
                elif field_type == bool:
                    default_dict[field] = False
                elif field_type == list:
                    default_dict[field] = []
                elif field_type == dict:
                    default_dict[field] = {}
        return default_dict

    def init(self):
        super().__init__(self.getdefault())

    def GetSelfDict(self):
        return dict(self)

    def check(self, data: dict):
        """
        验证字典是否符合规范
        :param data: 要验证的字典
        :return: (是否有效, 错误信息)
        """
        errors = []
        # 检查必填字段是否缺失
        for field, config in self.schema.items():
            if config.get('required', False) and field not in data:
                errors.append(f"缺少必填字段: {field}")
        # 检查字段类型
        for field, value in data.items():
            if field in self.schema:
                expected_type = self.schema[field].get('type')
                if expected_type and not isinstance(value, expected_type):
                    errors.append(f"字段 '{field}' 类型错误，应为 {expected_type}，实际为 {type(value)}")
        # 检查是否有未定义的字段
        for field in data:
            if field not in self.schema:
                errors.append(f"存在未定义的字段: {field}")
        return len(errors) == 0, errors

    @classmethod
    def save(cls, config: dict):
        if not path.exists(cls.ConfigFolderPath):
            makedirs(cls.ConfigFolderPath)
        configpath = path.join(cls.ConfigFolderPath, config['ConfigKey'] + config['ConfigName'] + ".json")
        with open(configpath, 'w', encoding='utf-8') as c:
            json.dump(config, c, ensure_ascii=False, indent=1)


class TimerConfig(ConfigTool):
    schema = {
        'ItemNum': {'type': int,         'default': 3},
        'Execute': {'type': [int] * 10,  'default': [0] * 10},
        'Time':    {'type': [str] * 10,  'default': [''] * 10},
        'Name':    {'type': [str] * 10,  'default': [''] * 10},
        'Awake':   {'type': [bool] * 10, 'default': [False] * 10},
    }
    schema = ScheMa(schema)

    def __init__(self):
        super().__init__(self.schema)


class SGAMainConfig(ConfigTool):
    tc = TimerConfig()
    schema = {
        'Version': {'type': str, 'default': ''},
        'WorkDir': {'type': str, 'default': ''},
        'OcrPath': {'type': str, 'default': ''},
        'StopKeys': {'type': str, 'default': 'ctrl+/'},
        'AutoUpdate': {'type': bool, 'default': True},
        'TimerConfig': {'type': TimerConfig, 'default': tc.getdefault()},
        'ConfigKey': {'type': int, 'default': ''},
        'ConfigLock': {'type': bool, 'default': True},
        'CurrentConfig': {'type': dict, 'default': {}},
        'SubConfig': {'type': dict, 'default': {}},
    }
    schema = ScheMa(schema)
    MainConfigPath = "personal/mainconfig.json"
    MainConfigBackupPath = "personal/mainconfigbackup.json"
    PersonalPath = "personal"

    def __init__(self):
        super().__init__(self.schema)
        # 加载主配置，若损坏则从备份恢复，若备份损坏或没有则进行初始化修复或者初始化
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        env.value["MainConfigBackup"] = False  # 是否从备份文件读取
        env.value["MainConfigTypeChange"] = False  # 主配置文件类型变动
        env.value["MainConfigInit"] = False  # 是否主配置初始化
        configread = False
        if path.exists(self.MainConfigPath):
            with open(self.MainConfigPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            if self.check(_mainconfig):
                self.update(self.schema)
                configread = True
        if not configread and path.exists(self.MainConfigBackupPath):
            with open(self.MainConfigBackupPath, 'r', encoding='utf-8') as c:
                _mainconfig = json.load(c)
            self.update(self.schema)
            configread = False
            env.value["MainConfigBackup"] = True
            if self.check(_mainconfig):
                env.value["MainConfigTypeChange"] = True
        if not configread:
            self.init()
            env.value["MainConfigInit"] = True
        self.savemain()
        self.savebackup()
        # 运行路径变化时，基础文件初始化
        if env.workdir != self["WorkDir"]:
            self["WorkDir"] = env.workdir
            self.BasisFileInit()

    @staticmethod
    def BasisFileInit():
        cachedir = "cache"
        scdir = "personal/script"
        rstpath = "resources/main/schtasks.json"
        pstpath = "personal/schtasks.json"
        rrspath = "resources/main/script/restart.bat"
        prspath = "personal/script/restart.bat"
        if not path.exists(cachedir):
            makedirs(cachedir)
        if not path.exists(scdir):
            makedirs(scdir)
        with open(rstpath, 'r', encoding='utf-8') as m:
            xml_dir = json.load(m)
        xml_list = xml_dir["part2"]
        xml_list[32] = f"      <Command>{env.workdir}\\SGA.exe</Command>\n"
        xml_list[34] = "      <WorkingDirectory>" + env.workdir + "</WorkingDirectory>\n"
        xml_dir["part2"] = xml_list
        with open(pstpath, 'w', encoding='utf-8') as x:
            json.dump(xml_dir, x, ensure_ascii=False, indent=1)

        f = open(rrspath, 'r', encoding='utf-8')
        start_list = f.readlines()
        f.close()
        start_list[2] = "start /d \"%s\" SGA.exe\n" % env.workdir
        f = open(prspath, 'w', encoding='utf-8')
        f.writelines(start_list)
        f.close()

        f = open("resources/main/script/maacreate.bat", 'r', encoding='ansi')
        bat_list = f.readlines()
        f.close()
        bat_list[1] = f" cd. > \"{env.workdir}/cache/maacomplete.txt\""
        f = open("personal/script/maacreate.bat", 'w', encoding='ansi')
        f.writelines(bat_list)
        f.close()

        rstvpath = "resources/main/script/restart.vbs"
        prsv = "personal/script/restart.vbs"
        pss = "personal/script/start-SGA.vbs"
        if not path.exists(prsv):
            copyfile(rstvpath, prsv)
        if not path.exists(pss):
            copyfile(rstvpath, pss)

    def check(self, configdict):
        if self.schema.typedict() != DictListType(configdict):
            return False
        if DictListType(configdict['TimerConfig']) != TimerConfig.schema.typedict():
            return False
        return True

    def keylist(self):
        return list(self.keys())

    def savemain(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        with open(self.MainConfigPath, 'w', encoding='utf-8') as c:
            json.dump(dict(self), c, ensure_ascii=False, indent=1)

    def savebackup(self):
        if not path.exists(self.PersonalPath):
            makedirs(self.PersonalPath)
        with open(self.MainConfigBackupPath, 'w', encoding='utf-8') as c:
            json.dump(dict(self), c, ensure_ascii=False, indent=1)
