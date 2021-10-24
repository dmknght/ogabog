from ogabog.cores import plugin


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
        self.opts.description = "https://gtfobins.github.io/gtfobins/base64/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"bridge -b \"{self.args.target_file}\""
