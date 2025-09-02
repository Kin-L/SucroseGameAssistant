from pydantic import Field, BaseModel
from typing import List


class TimerConfigClass(BaseModel):
    Execute: List[int] = Field(default_factory=lambda: [0] * 10)
    Time: List[List[int]] = Field(default_factory=lambda: [[0, 0] for _ in range(10)])
    ConfigKeys: List[str] = Field(default_factory=lambda: [""] * 10)
    Awake: List[bool] = Field(default_factory=lambda: [False] * 10)


class MainConfig(BaseModel):
    Version: str = ""
    WorkDir: str = ""
    OcrPath: str = ""
    StopKeys: str = "ctrl+/"
    AutoUpdate: int = 1  # 修正为整数类型
    TimerConfig: TimerConfigClass = Field(default_factory=TimerConfigClass)
    ConfigKey: str = ""
    ConfigLock: bool = True
    CurrentConfig: dict = Field(default_factory=dict)
    OtherConfig: dict = Field(default_factory=lambda: {"License": False})
    ModulesEnable: list = Field(default_factory=list)


def checkmain(configdict: dict):
    try:
        MainConfig(**configdict)
        return True
    except Exception as e:
        print(str(e))
        return False
