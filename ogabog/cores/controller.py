# Control modules

# This string is the place of cutting the module name and project location
# All modules should be at folder "/module/" or bug happens
MODULE_DIR = "/modules/"


def start_module(un_args, module_name, class_name, modules):
    try:
        import importlib
        module = importlib.import_module("modules." + module_name.replace("/", "."))
        # https://stackoverflow.com/a/41678146
        # Import class with importlib
        # https://stackoverflow.com/a/17534365
        # initialize class to fix the problem can't use methods
        try:
            module = getattr(module, class_name)()
            module.init_name(module_name, class_name)
        except AttributeError:
            from ogabog.cores import searcher
            print(f"[x] Invalid class name \"{class_name}\" for module \"{module_name}\"")
            from argparse import Namespace
            platform, executable = module_name.split("/")
            args = Namespace(platform=platform, executable=executable)
            searcher.list_modules(modules.__path__[0], args)
            return
        # Parse args from cli, pass into module's args check
        module.args = module.get_opts().parse_args(un_args)
        module.run()

    except ModuleNotFoundError:
        print(f"[x] Invalid module name {module_name}")
    except AttributeError:
        # Error msg was handled
        pass


def program_handler(modules, args):
    """
    Handle main program by:
        1. Check args (for core framework)
        2. Get all invalid args to check in module's args
        3. Listing all available modules
        4. Import module with class name (user define) then
            show final result
    :param modules: imported module (usually <project.module>)
    :param args: custom Argparse class from argutils
    :return:
    """
    # https://stackoverflow.com/a/12818237
    usr_args, un_args = args.parse_known_args()
    if usr_args.list:
        from ogabog.cores import searcher
        # TODO show error for wrong flags of listing
        searcher.list_modules(modules.__path__[0], usr_args)
    # elif usr_args.search:
    #     # We do search with custom filter here
    #     # un_args -> keywords
    #     from ogabog.cores import searcher
    #     searcher.search(modules, un_args, usr_args)
    else:
        module_name = usr_args.p
        class_name = usr_args.c
        if module_name and class_name:
            start_module(un_args, module_name, class_name, modules)
        else:
            if module_name:
                if not class_name:
                    print("[x] No class name provided! Please add \"-c <ClassName>\" from list of classes below")
                    from ogabog.cores import searcher
                    from argparse import Namespace
                    platform, executable = module_name.split("/")
                    args = Namespace(platform=platform, executable=executable)
                    searcher.list_modules(modules.__path__[0], args)
            else:
                if class_name:
                    print("[x] No module name provided")
                else:
                    args.print_help()

#
# def check_env(name: str, list_name: list) -> str:
#     """
#     When user type shell, we usually have full path or only exe name
#     1. bash
#     2. /bin/bash
#     3. possibly /usr/bin/bash
#     We accept bash as /bin/bash from the list
#     # TODO 1 think about /usr/bin/bash
#     # TODO 2 more robofust for python-like cases like python, python3
#         python3.7, python3.8
#     :param name: user provide
#     :param list_name: list of choices. Usually a full path of command
#     :return: path in list or "" as not found
#     """
#     for each_name in list_name:
#         if name == each_name.split("/")[-1]:
#             return each_name
#     return ""
