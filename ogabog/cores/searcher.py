import os

MODULE_DIR = "/modules/"


def get_classes(module_name: str):
    """
    List all classes in the module with the description
    :param module_name: name of module to show
    :return: tuple(name of class, description)
    """
    try:
        import importlib
        module = importlib.import_module("modules." + module_name.replace("/", "."))
        for key, obj in module.__dict__.items():
            if isinstance(obj, type):
                desc = getattr(module, key)().get_opts().description
                yield key, desc
        del module
    except ModuleNotFoundError:
        print(f"Can't import module {module_name}")


def index_modules(directory: str):
    """
    List all modules inside folder
    Source URL:
      https://github.com/threat9/routersploit/blob/fb12ae80086699d23465cacbcc6dc5b291dd2af2/routersploit/core/exploit/utils.py#L84
    License:
    Copyright 2018, The RouterSploit Framework (RSF) by Threat9
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

        * Redistributions of source code must retain the above copyright notice, this list of conditions
         and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions
         and the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of RouterSploit Framework nor the names of its contributors may be used to endorse
         or promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
     INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
     ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
     INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
     PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
     HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
     (INCLUDING NEGLIGENCE OR OTHERWISE)ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
     EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    The above licensing was taken from the BSD licensing and is applied to RouterSploit Framework as well.

    Note that the RouterSploit Framework is provided as is, and is a royalty free open-source application.

    Feel free to modify, use, change, market, do whatever you want with it as long as you give the appropriate credit.
    :param directory: directory that contains modules
    :return: list of all modules that we can import
    """
    modules = []
    for root, dirs, files in os.walk(directory):
        _, package, root = root.rpartition(MODULE_DIR.replace("/", os.sep))
        root = root.replace(os.sep, ".")
        files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
        modules.extend(map(lambda x: ".".join((root, os.path.splitext(x)[0])), files))
    return modules


# def search(modules, keyword, args):
#     # TODO filter for language / interpreter / execution
#     """
#     Completed: Platform filter
#     :param modules:
#     :param keyword:
#     :param args:
#     :return:
#     """
#     import_path = modules.__path__[0]
#
#     if args.platform:
#         # If user defines platform, we set code from importlib
#         import_path += "/" + args.platform
#
#     import importlib
#     for module_name in index_modules(import_path):
#         module = importlib.import_module("modules." + module_name)
#         # if args.c:
#         #     # If user define specific class, we use it to print
#         #     module_attr = getattr(module, args.c)()
#         #     print(module_attr)
#         # else:
#             # Else use for loop for everything
#         for class_name, obj in module.__dict__.items():
#             """
#             Try filter class name by user
#             1. If no class name: skip -> search all
#             2. If class name:
#                 a. If user's class name not in class name -> skip
#                 b. If user's class name in class name, show
#             """
#             if args.c and args.c.lower() not in class_name.lower():
#                 continue
#             if isinstance(obj, type):
#                 # TODO search class_name with keywords
#                 # if class_name.lower()
#                 # TODO search desc with keywords
#                 desc = getattr(module, class_name)().get_opts().description
# for module in index_modules(import_path):
#     print(module)
# module = importlib.import_module(import_path)
# print(import_path)
# if args.c:
#     module = getattr(module, args.c)()
# else:
#     pass
# print(getattr(module))
# try:
#     # module = getattr(module, class_name)()
# except:
#     pass
# TODO handle no module path here


def list_modules(import_path, args):
    if not import_path.endswith("/"):
        import_path += "/"
    sz_modules = 0
    sz_classes = 0
    if args.platform:
        # If user defines platform, we set code from importlib
        import_path += args.platform

    for module_name in index_modules(import_path):
        if args.executable:
            if not module_name.endswith(args.executable):
                continue
        print(module_name.replace(".", "/"))
        sz_modules += 1
        # https://stackoverflow.com/a/38228621
        for class_name, desc in get_classes(module_name):
            try:
                description = desc.split("\n")[0]
                print(f"  {class_name}{' ': <{20 - len(class_name)}} {description}")
                sz_classes += 1
            except ValueError:
                print(f"  {class_name}{' ': <{20 - len(class_name)}} {desc}")
    print(f"\nTotal: {sz_classes} class[es] of {sz_modules} module[s]")
