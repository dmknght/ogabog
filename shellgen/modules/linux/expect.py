from ogabog.cores import plugin, const


class Shell(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "https://gtfobins.github.io/gtfobins/expect/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = 0
        self.is_interactive = True

    def make_shell(self):
        self.shell = f"expect -c \"spawn {self.args.shell}; interact\""


class ReadFile(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        self.shell_type = 3
        self.is_interactive = False
        self.add_args(
            "--target-file",
            default="/etc/os-release",
            help="File to read on target machine"
        )
        self.opts.description = "https://gtfobins.github.io/gtfobins/expect/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"expect \"{self.args.target_file}\""
