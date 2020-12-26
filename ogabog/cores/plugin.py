import argparse


class Module(object):
    def __init__(self):
        self.opts = argparse.ArgumentParser()
        self.core_module = self.opts.add_argument_group("Framework arguments")
        self.group_module = self.opts.add_argument_group("Module arguments")
        self.args = None
        self.shell = ""

    def add_args(self, *args, **kwargs):
        """
        Add arguments to group "module" from plugin's call
        :param args:
        :param kwargs:
        :return:
        """
        self.group_module.add_argument(*args, **kwargs)

    def get_opts(self):
        """
        Return options, which is parser of argparse
        :return: argparse
        """
        return self.opts

    def show_help(self, module_name, class_name):
        """
        Show custom help which added argument from core framework
        All arguments are must added to use this plugin so we add
          it to the required
        :param module_name: name of imported module
        :param class_name: name of current class
        :return:
        """
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

    def make_shell(self):
        pass

    def run(self):
        """
        Dummy method to show payload
        :return:
        """
        self.make_shell()
        print(self.shell)


class ReverseShell(Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--ip",
            help="IP address",
            required=True
        )
        self.add_args(
            "--port",
            help="Port address",
            required=True
        )


class BindShell(Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--port",
            help="Port address",
            required=True
        )
        self.opts.description = "[BindShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
