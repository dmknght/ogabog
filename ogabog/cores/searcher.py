import os
from ogabog.cores.const import *
from ogabog.cores.print_utils import *

MODULE_DIR = "/modules/"


def get_classes(module_name: str):
    """
    List all classes in the module with the description
    :param module_name: name of module to show
    :return: tuple(name of class, description)
    """
    try:
        import importlib
        module = importlib.import_module("shellgen.modules." + module_name.replace("/", "."))
        for class_name, obj in module.__dict__.items():
            if isinstance(obj, type):
                shell_type, is_interactive = 0, False
                try:
                    shell_type = getattr(module, class_name)().shell_type
                    is_interactive = getattr(module, class_name)().is_interactive
                except AttributeError:
                    print(f"  [!] Class {class_name} has no attribute \"shell_type\"")
                try:
                    is_interactive = getattr(module, class_name)().is_interactive
                except AttributeError:
                    print(f"  [!] Class {class_name} has no attribute \"is_interactive\"")
                yield class_name, shell_type, is_interactive
        del module
    except ModuleNotFoundError:
        print(f"(Searcher) Can't import module {module_name}")


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


def do_filter_list(import_path, args):
    # TODO list for 1 module only?
    descriptions = ()
    for module_name in index_modules(import_path):
        if args.executable:
            if not module_name.endswith(args.executable):
                continue
        for idx, (class_name, shell_type, is_interactive) in enumerate(get_classes(module_name)):
            # Filter user search by interactive and shell type. Default value of namespace is None if
            # user didn't pass value
            if args.interactive is not None and args.interactive != is_interactive:
                pass
            elif args.shell_type and SHELL_TYPE_TO_INT[args.shell_type] != shell_type:
                pass
            else:
                help_module_name = color_bright_white(module_name.replace(".", "/"))
                desc = color_bright_magenta("Interactive") if is_interactive else color_magenta("Non-Interactive")
                desc += f" {COLORED_SHELL_TYPE[shell_type]}"
                descriptions += ((help_module_name, class_name, desc),) if \
                    help_module_name not in [x[0] for x in descriptions] else (("", class_name, desc),)
    return descriptions


def list_modules(import_path, args, keywords=""):
    if not import_path.endswith("/"):
        import_path += "/"
    if args.platform:
        # If user defines platform, we set code from importlib
        import_path += args.platform

    descriptions = do_filter_list(import_path, args)
    if not descriptions:
        print("No results found")
    else:
        if args.module_only:
            [print(x[0]) for x in descriptions if x[0]]
        else:
            header = ("Module", "Classes", "Descriptions")
            if descriptions:
                print_table(header, *descriptions)
