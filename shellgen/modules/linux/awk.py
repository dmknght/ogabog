from ogabog.cores import plugin


class ReverseShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--ip",
            help="IP address"
        )
        self.add_args(
            "--Port",
            help="Port address"
        )


class BindShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--ip",
            help="IP address"
        )
