from typing import List, Tuple, Union, Optional, Any
from os import path, makedirs, listdir
import json
from maincode.tools.main import logger


class SubConfigs:
    CONFIG_DIR = "personal/config"
    
    def __init__(self):
        self._ensure_config_dir_exists()
        self.filelist: List[Tuple[str, str, int]] = []  # 文件识别码， 文件名， 模组识别码
        self._load_configs()

    def _ensure_config_dir_exists(self):
        """确保配置目录存在"""
        if not path.exists(self.CONFIG_DIR):
            makedirs(self.CONFIG_DIR)

    def _load_configs(self):
        """加载所有配置文件信息"""
        _subconfigs = []
        config_keys_seen = set()

        try:
            files = listdir(self.CONFIG_DIR)
        except OSError as e:
            logger.warning(f"无法读取目录 {self.CONFIG_DIR}: {e}")
            return

        for file in files:
            name, suffix = path.splitext(file)
            if suffix != ".json":
                continue

            if len(name) < 4:
                continue

            configkey, filename = name[:4], name[4:]
            if configkey in config_keys_seen:
                continue

            full_path = path.join(self.CONFIG_DIR, file)

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    _config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"无法解析配置文件 {full_path}: {e}")
                continue

            modulekey: Optional[int] = _config.get("ModuleKey")
            if not isinstance(modulekey, int):
                continue

            _subconfigs.append((configkey, filename, modulekey))
            config_keys_seen.add(configkey)

        self.filelist = _subconfigs

    def GetFiles(self):
        return self.filelist

    def GetFilesT(self):
        return tuple(zip(*self.filelist))

    def FindItem(self, _input: Union[str, int]) -> Optional[List[Any]]:
        for n, item in enumerate(self.filelist):
            if _input in item:
                return list(item) + [n]
        return None

    def Read(self, num: int) -> Optional[dict]:
        if not (0 <= num < len(self.filelist)):
            return None
        ck, cn, mk = self.filelist[num]
        full_path = path.join(self.CONFIG_DIR, f"{ck}{cn}.json")
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"无法读取配置文件 {full_path}: {e}")
            return None

    @staticmethod
    def Save(_config: dict) -> bool:
        required_keys = ["ConfigKey", "ConfigName"]
        for key in required_keys:
            if key not in _config or not isinstance(_config[key], str):
                logger.warning(f"缺少或无效字段: {key}")
                return False

        _dir = SubConfigs.CONFIG_DIR
        if not path.exists(_dir):
            makedirs(_dir)

        _name = _config["ConfigKey"] + _config["ConfigName"]
        full_path = path.join(_dir, f"{_name}.json")

        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(_config, f, ensure_ascii=False, indent=1)
            return True
        except IOError as e:
            logger.warning(f"保存配置文件失败 {full_path}: {e}")
            return False


sc = SubConfigs()
