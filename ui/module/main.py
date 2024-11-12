from ..mix.main import Mix
from ..klein.main import Klein
from ..genshin.main import Genshin
from ..maa import MAA
from ..m7a import M7A
from ..snow.main import Snow
from ..common.main import Common
from .module import ModuleWindow


class Module(ModuleWindow):
    def __init__(self, main):
        super().__init__(main)
        self.mix = Mix(self.stack_module, main)
        self.kleins = Klein(self.stack_module, main)
        self.genshin = Genshin(self.stack_module, main)
        self.maa = MAA(self.stack_module, main)
        self.m7a = M7A(self.stack_module, main)
        self.snow = Snow(self.stack_module, main)
        self.common = Common(self.stack_module, main)
