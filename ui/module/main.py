# -*- coding:gbk -*-
from ..mix.main import Mix
from ..klein.main import Klein
from ..genshin.main import Genshin
from ..maa import MAA
from ..m7a import M7A
from .module import ModuleWindow


class Module(ModuleWindow):
    def __init__(self, main):
        super().__init__(main)
        self.mix = Mix(self.stack_module, self.widget_icon, main)
        self.kleins = Klein(self.stack_module, self.widget_icon, main)
        self.genshin = Genshin(self.stack_module, self.widget_icon, main)
        self.maa = MAA(self.stack_module, self.widget_icon, main)
        self.m7a = M7A(self.stack_module, self.widget_icon, main)

