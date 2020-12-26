import argparse


class Module(object):
    def __init__(self):
        self.opts = argparse.ArgumentParser()
        self.core_module = self.opts.add_argument_group("Framework arguments")
        self.group_module = self.opts.add_argument_group("Module arguments")

    def add_args(self, *args, **kwargs):
        self.group_module.add_argument(*args, **kwargs)

    def get_opts(self):
        return self.opts

    def show_help(self, module_name, class_name):
        self.core_module.add_argument(
            "-p",
            metavar=module_name,
            default=module_name,
            help="Select module " + module_name,
            required=True
        )
        self.core_module.add_argument(
            "-c",
            metavar=class_name,
            default=class_name,
            help="Select class " + class_name,
            required=True
        )
        self.opts.print_help()
