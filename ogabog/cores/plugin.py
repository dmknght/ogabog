from ogabog.cores import argutils


class BaseShell(object):
    def __init__(self):
        self.opts = argutils.PluginArgumentParser()
        self.core_module = self.opts.add_argument_group("Framework arguments")
        self.group_module = self.opts.add_argument_group("Module arguments")
        self.args = None
        self.is_interactive = False
        """
        Shell type:
        0. system shell / command
        1. reverse shell
        2. bind shell
        """
        self.shell_type = 0
        self.shell = ""
        self.module_name = ""
        self.class_name = ""
        self.extension = ""
        self.file_only = False

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
        """
        Dummy make shell method for Base class
        :return:
        """
        pass

    # def handler(self):
    #     """
    #     Dummy handler of listener for Base class
    #     :return:
    #     """
    #     pass

    def set_write_file(self):
        # Allow user to provide --out without the full path
        # https://stackoverflow.com/a/30897095
        self.add_args(
            "--out",
            nargs="?",
            metavar="Path_to_write",
            default="/tmp/outfile",
            const="",
            help="Set save file path",
            required=self.file_only,
        )

    def run(self):
        """
        Show payload to terminal or generate file
        Then set listener or not as user's choice
        :return:
        """
        self.make_shell()
        # We check if user provided --out flag
        # If user didn't, the exception raises AttributeError
        write_path = ""
        try:
            # In some modules, --out flag will have default value
            # We try to figure it out did users want to write a file
            # or print output only
            if argutils.is_write_file():
                write_path = self.args.out
                if not write_path:
                    print("[!] Generating custom path")
                    write_path = f"/tmp/{self.module_name.replace('/', '_')}_{self.class_name}"
                    if self.extension:
                        write_path = f"{write_path}.{self.extension}"
                f = open(write_path, "w")
                f.write(self.shell)
                f.close()
                print(f"[+] New shell at {write_path}")
            else:
                if not self.file_only:
                    print(self.shell)
        except PermissionError:
            print(f"[x] Failed to write file at {write_path}: Permission Denied")
        except AttributeError:
            print(self.shell)

        # if self.args.listen:
        #     self.handler()


class ReverseShell(BaseShell):
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
        self.protocol = ""

    # def handler(self):
    #     """
    #     Create reverse shell handler
    #     :return:
    #     """
    #     from ogabog.cores import handler
    #     listen_addr = self.args.lhost if self.args.lhost else self.args.ip
    #     listen_port = self.args.lport if self.args.lport else self.args.port
    #
    #     if self.shell_type == "udp":
    #         handler.reverse_udp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)
    #     else:
    #         handler.reverse_tcp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)


class BindShell(BaseShell):
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
        self.protocol = ""

    # def handler(self):
    #     """
    #     Create reverse shell handler
    #     :return:
    #     """
    #     from ogabog.cores import handler
    #     listen_addr = self.args.lhost
    #     if not listen_addr:
    #         print("[x] Need --lhost to start listener")
    #         return
    #     listen_port = self.args.lport if self.args.lport else self.args.port
    #
    #     if self.shell_type == "udp":
    #         handler.bind_udp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)
    #     else:
    #         handler.bind_tcp(listen_addr, listen_port, self.module_name, self.class_name, self.args.timeout)
