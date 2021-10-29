import os
import importlib
from shellgen import modules


def get_classes(module_name: str) -> list[str]:
    """
    Get all names of classes in a module using importlib and isinstance
    :param module_name: full module to use import lib. Example: shellgen.linux.awk
    :return: list of names
    """
    result = []

    module = importlib.import_module(module_name)
    for class_name, obj in module.__dict__.items():
        if isinstance(obj, type):
            result.append(class_name)

    return result


def get_modules(path: str) -> dict[dict]:
    """
    Get all py modules, except pycache in current directory.
    :param path: absolute path
    :return: list dictionary [{"module_name": "classes"}]
    """
    result = {}

    for name in os.listdir(path):
        if not name.startswith("__") and name.endswith(".py"):
            module_name = name.split('.')[0]
            import_name = f"shellgen{path.split('shellgen')[1]}/{module_name}".replace("/", ".")
            classes = get_classes(import_name)
            result.update({module_name: classes})

    return result


def get_all_modules():
    result = {}

    path = modules.__path__[0]
    for name in os.listdir(path):
        if not name.startswith("__"):
            result.update({name: get_modules(f"{path}/{name}")})

    return result
