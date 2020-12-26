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
        self.opts.description = "Generate reverse shell using awk command"


class BindShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "Generate bind shell using awk command"
