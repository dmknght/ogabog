from ogabog.cores.print_utils import *


LINUX_SHELL: list = [
    '/bin/bash',
    '/bin/dash',
    '/bin/sh',
    '/bin/ash',
    '/bin/bsh',
    '/bin/csh',
    '/bin/ksh',
    '/bin/zsh',
    '/bin/pdksh',
    '/bin/tcsh'
]

SHELL_TYPE_TO_INT = {
    "System-Shell": 0,
    "Reverse-Shell": 1,
    "Bind-Shell": 2,
    "Command": 3
}

COLORED_SHELL_TYPE = (
    color_bright_red("System-Shell"),
    color_bright_cyan("Reverse-Shell"),
    color_cyan("Bind-Shell"),
    color_red("Command")
)
