from pydantic import Field, BaseModel
from typing import List


class TimerConfigClass(BaseModel):
    Execute: List[int] = [0] * 10
    Time: List[List[int]] = [[0, 0]] * 10
    ConfigKeys: List[str] = [""] * 10
    Awake: List[bool] = [False] * 10


class MainConfig(BaseModel):
    Version: str = ""
    WorkDir: str = ""
    OcrPath: str = ""
    StopKeys: str = "ctrl+/"
    AutoUpdate: int = True
    TimerConfig: TimerConfigClass = Field(default_factory=TimerConfigClass)
    ConfigKey: str = ""
    ConfigLock: bool = True
    CurrentConfig: dict = {}
    OtherConfig: dict = {"License": False}
    ModulesEnable: list = []


def checkmain(configdict: dict):
    try:
        MainConfig(**configdict)
        return True
    except Exception as e:
        print(str(e))
        return False
