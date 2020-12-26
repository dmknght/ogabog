# Control modules
import os

# This string is the place of cutting the module name and project location
# All modules should be at folder "/module/" or bug happens
MODULE_DIR = "/modules/"


def index_modules(directory: str) -> list:
    """
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


def list_classes(module_name: str):
    try:
        import importlib
        module = importlib.import_module("modules." + module_name.replace("/", "."))
        for key, obj in module.__dict__.items():
            if isinstance(obj, type):
                yield key
        del module
    except ModuleNotFoundError:
        print("Can't import module " + module_name)


def list_modules(modules: list):
    for module in modules:
        print(module.replace(".", "/"))
        for class_name in list_classes(module):
            print("  " + class_name)
