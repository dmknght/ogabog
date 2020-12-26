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
    if module_name:
        import importlib

        module = importlib.import_module("modules." + module_name.replace("/", "."))
        # sub_args = module.get_opts().parse_args(un_args)
        # print(sub_args)
