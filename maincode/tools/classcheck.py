import ast
import importlib.util
import pkgutil
import sys
from os import path, getcwd
from pathlib import Path
from typing import Any


def get_base_name(base_node):
    """获取基类名称"""
    if isinstance(base_node, ast.Name):
        return base_node.id
    elif isinstance(base_node, ast.Attribute):
        # 处理 module.Class 形式的基类
        return ast.unparse(base_node)
    elif isinstance(base_node, ast.Subscript):
        # 处理泛型基类如 List[str]
        return ast.unparse(base_node)
    return ""


def find_subclasses_of_base(file_path, base_class_name):
    """查找指定基类的所有子类"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()

        tree = ast.parse(source_code)

        subclasses = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # 检查是否继承自指定基类
                for base in node.bases:
                    base_name = get_base_name(base)
                    if base_name == base_class_name:
                        subclasses.append(node.name)
                        break
        if subclasses:
            if len(subclasses) == 1:
                return subclasses[0]
            else:
                return False
        return None

    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []
    except SyntaxError as e:
        print(f"语法错误: {e}")
        return []


def instantiate_class(file_path: str, class_name: str) -> Any:
    """实例化指定类"""
    file_path_obj = Path(file_path)
    module_name = f"dynamic_{file_path_obj.stem}_{hash(file_path)}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    class_obj = getattr(module, class_name)
    return class_obj


def collect_scripts() -> dict[str: list]:
    packagelist = ["maincode", "script"]
    package = importlib.import_module(".".join(packagelist))
    script_dict = {}
    for importer, scriptname, ispkg in pkgutil.iter_modules(package.__path__):
        _list = list(packagelist)
        if ispkg:
            _list.append(scriptname)
            modulepackage = importlib.import_module(".".join(_list))
            for i, m, p in pkgutil.iter_modules(modulepackage.__path__):
                if not p and m == "main":
                    _list.append(m)
                    break
            else:
                continue
        else:
            _list.append(scriptname)
        script_dict[scriptname] = _list
    _script_dict = {}
    for (sname, slist) in script_dict.items():
        script_path = path.join(getcwd(), "/".join(slist) + ".py")
        file_path = Path(script_path).absolute()

        # 生成模块名
        module_name = file_path.stem

        # 使用importlib加载模块
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"无法从文件 {file_path} 创建spec")

        module = importlib.util.module_from_spec(spec)

        # 执行模块代码
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise RuntimeError(f"执行模块时出错: {e}")

        # 获取模块中的所有变量（过滤掉内置属性和私有属性）
        script_run = False
        script_name = ""
        for name in dir(module):
            # 跳过内置属性和私有属性
            if not name.startswith('_'):
                value = getattr(module, name)
                if callable(value) and name == "script_run":
                    script_run = True
                elif name == "script_name":
                    script_name = value
        if script_name and script_run:
            _script_dict[script_name] = slist
    return _script_dict


if __name__ == '__main__':
    _path = r"/maincode/modules/00mix/main.py"
    # 使用示例
    subclasses = find_subclasses_of_base(_path, "ModuleClass")
    if subclasses:
        print(f"找到 {len(subclasses)} 个 BaseClass 的子类:")
        for subclass in subclasses:
            print(f"  {subclass['name']} (行号: {subclass['lineno']})")
    else:
        print("未找到 BaseClass 的子类")