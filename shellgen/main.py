from ogabog.cores import argutils, controller
import modules

args = argutils.core_args()
# https://stackoverflow.com/a/12818237
args, un_args = args.parse_known_args()

if args.l:
    modules = controller.index_modules(modules.__path__[0])
    controller.list_modules(modules)
else:
    module_name = args.p
    class_name = args.c
    if module_name and class_name:
        try:
            import importlib
            module = importlib.import_module("modules." + module_name.replace("/", "."))
            # https://stackoverflow.com/a/41678146
            # Import class with importlib
            # https://stackoverflow.com/a/17534365
            # initialize class to fix the problem can't use methods
            module = getattr(module, class_name)()
            # Parse args from cli, pass into module's args check
            module_args = module.get_opts().parse_args(un_args)
            module.show_shell(module_args)
        except ModuleNotFoundError:
            print("Invalid module name " + module_name)
        except AttributeError:
            # TODO confuse here between import class and other bugs
            print("Invalid class name " + class_name + " for module " + module_name)
