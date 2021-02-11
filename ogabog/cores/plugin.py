# import argparse
from ogabog.cores import argutils


class Module(object):
    def __init__(self):
        self.opts = argutils.PluginArgumentParser()
        self.core_module = self.opts.add_argument_group("Framework arguments")
        self.group_module = self.opts.add_argument_group("Module arguments")
        self.args = None
        self.shell = ""
        self.module_name = ""
        self.class_name = ""

        self.group_module.add_argument(
            "--out",
            metavar="Path_to_write",
            default="/tmp/outfile",
            help="Set save file path",
            required=True
        )

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

    def init_name(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name

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
        self.add_args(
            "--listen",
            action='store_true',
            help="Create listener",
        )
        self.group_handler = self.opts.add_argument_group("Handler arguments")
        self.group_handler.add_argument(
            "--lhost",
            help="Listener's address",
            metavar="IP",
            required=False
        )
        self.group_handler.add_argument(
            "--lport",
            help="Listener's port",
            metavar="Port",
            required=False
        )
        self.group_handler.add_argument(
            "--timeout",
            help="Socket timeout",
            metavar="Timeout",
            type=int,
            default=3,
            required=False
        )
        self.is_udp = False

    def handler(self):
        """
        Create reverse shell handler
        :return:
        """
        from ogabog.cores import handler
        listen_addr = self.args.lhost if self.args.lhost else self.args.ip
        listen_port = self.args.lport if self.args.lport else self.args.port

        if self.is_udp:
            handler.reverse_udp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)
        else:
            handler.reverse_tcp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)

    def run(self):
        """
        Show payload to terminal or generate file
        Then set listener or not as user's choice
        :return:
        """
        self.make_shell()
        if not self.args.out:
            print(self.shell)
        else:
            try:
                f = open(self.args.out, "w")
                f.write(self.shell)
                f.close()
                print(f"[+] New shell at {self.args.out}")
            except:
                print(f"[x] Error while writing shell to {self.args.out}")
        if self.args.listen:
            self.handler()


class BindShell(Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--port",
            help="Port address",
            required=True
        )
        self.add_args(
            "--listen",
            action='store_true',
            help="Create listener",
        )
        self.group_handler = self.opts.add_argument_group("Handler arguments")
        self.group_handler.add_argument(
            "--lhost",
            help="Listener's address",
            metavar="IP",
            required=False
        )
        self.group_handler.add_argument(
            "--lport",
            help="Listener's port",
            metavar="Port",
            required=False
        )
        self.group_handler.add_argument(
            "--timeout",
            help="Socket timeout",
            metavar="Timeout",
            type=int,
            default=3,
            required=False
        )
        self.is_udp = False

    def handler(self):
        """
        Create reverse shell handler
        :return:
        """
        from ogabog.cores import handler
        listen_addr = self.args.lhost if self.args.lhost else self.args.ip
        listen_port = self.args.lport if self.args.lport else self.args.port

        if self.is_udp:
            handler.bind_udp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)
        else:
            handler.bind_tcp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)

    def run(self):
        """
        Show payload to terminal or generate file
        Then set listener or not as user's choice
        :return:
        """
        self.make_shell()
        if not self.args.out:
            print(self.shell)
        else:
            try:
                f = open(self.args.out, "w")
                f.write(self.shell)
                f.close()
                print(f"[+] New shell at {self.args.out}")
            except:
                print(f"[x] Error while writing shell to {self.args.out}")
        if self.args.listen:
            self.handler()
