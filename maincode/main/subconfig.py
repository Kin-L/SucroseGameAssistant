from typing import List, Tuple, Union
from os import path, makedirs, listdir
import json


class SubConfigs:
    def __init__(self):
        # 读取子设置信息
        _subconfigs = []
        _configdirpath = "personal/config"
        if not path.exists(_configdirpath):
            makedirs(_configdirpath)
        _listdir = listdir(_configdirpath)
        if _listdir:
            for file in _listdir:
                name, suffix = path.splitext(file)
                configkey, name = name[:4], name[4:]
                if suffix == ".json":
                    _path = path.join(_configdirpath, file)
                    with open(_path, 'r', encoding='utf-8') as c:
                        _config = json.load(c)
                        modulekey: Union[int, None] = _config.get("ModuleKey", None)
                    if modulekey is not None:
                        allow = True
                        for item in _subconfigs:
                            if configkey in item:
                                allow = False
                        if allow:
                            _subconfigs += [[configkey, name, modulekey]]
        # 储存设置文件信息，文件名和类型
        self.filelist: List[Tuple[str, str, int]] = _subconfigs  # 文件识别码， 文件名， 模组识别码

    def GetFiles(self):
        return self.filelist

    def GetFilesT(self):
        return tuple(zip(*self.filelist))

    def FindItem(self, _input: [str, int]) -> [list, bool]:
        for n, item in enumerate(self.filelist):
            if _input in item:
                return list(item) + [n]
        return False

    def Read(self, num: int) -> [dict, bool]:
        ck, cn, mk = self.filelist[num]
        with open(f"personal/config/{ck + cn}.json", 'r', encoding='utf-8') as c:
            _config = json.load(c)
        return _config

    @staticmethod
    def Save(_config: dict):
        _dir = "personal/config"
        if not path.exists(_dir):
            makedirs(_dir)
        _name = _config["ConfigKey"] + _config["ConfigName"]
        with open(f"personal/config/{_name}.json", 'w', encoding='utf-8') as c:
            json.dump(_config, c, ensure_ascii=False, indent=1)


sc = SubConfigs()
