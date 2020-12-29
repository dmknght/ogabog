from ogabog.cores import plugin, const


class TTY(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[TTYShell] Expect TTY shell escape.https://www.metahackers.pro/spawing-tty-shells/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = """expect -c \"spawn {}; interact\"""".format(self.args.shell)
