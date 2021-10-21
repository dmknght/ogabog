def color_red(text: str):
    return f"\033[31m{text}\033[0m"


def color_green(text: str):
    return f"\033[32m{text}\033[0m"


def color_yellow(text: str):
    return f"\033[33m{text}\033[0m"


def color_blue(text: str):
    return f"\033[34m{text}\033[0m"


def color_magenta(text: str):
    return f"\033[35m{text}\033[0m"


def color_cyan(text: str):
    return f"\033[36m{text}\033[0m"


def color_white(text: str):
    return f"\033[37m{text}\033[0m"


def color_bright_red(text: str):
    return f"\033[91m{text}\033[0m"


def color_bright_green(text: str):
    return f"\033[92m{text}\033[0m"


def color_bright_yellow(text: str):
    return f"\033[93m{text}\033[0m"


def color_bright_blue(text: str):
    return f"\033[94m{text}\033[0m"


def color_bright_magenta(text: str):
    return f"\033[95m{text}\033[0m"


def color_bright_cyan(text: str):
    return f"\033[96m{text}\033[0m"


def color_bright_white(text: str):
    return f"\033[97m{text}\033[0m"


def print_table(headers, *args, **kwargs):
    ################################################
    # print beautiful table in terminal style
    # author @routersploit project
    # ALL input data must be string
    ################################################

    extra_fill = kwargs.get("extra_fill", 2)
    header_separator = kwargs.get("header_separator", "-")

    def custom_len(text: str):
        try:
            return len(text) - (4 * text.count("\x1b") + 1)
        except TypeError:
            return 0

    # CRAFTING HEADER #
    fill = []

    # headers_line += label: Filling_header
    # headers_line = headers_line + "Lable 1 | Label 2"
    headers_line = '  |  '
    headers_separator_line = '  +'

    for idx, header in enumerate(headers):
        column = [custom_len(arg[idx]) for arg in args]
        column.append(len(header))
        current_line_fill = max(column) + extra_fill
        fill.append(current_line_fill)
        # label: Filling_header
        headers_line = "%s%s" % (
            "".join((headers_line, "{header:<{fill}}".format(header=header, fill=current_line_fill))),
            "|  "
        )

        headers_separator_line = "%s-%s" % (
            "-".join((
                headers_separator_line,
                '{:<{}}'.format(header_separator * current_line_fill, current_line_fill)
            )),
            "+"
        )

    # End of crafting header

    # Print header
    print(f"{headers_separator_line}\n{headers_line}")

    # Print contents
    for arg in args:
        content_line = '  |  '  # print first character before contents
        for idx, element in enumerate(arg):
            if idx == 0 and element != "":
                print(headers_separator_line)
            content_line = "%s%s" % (
                "".join((
                    content_line,
                    '{:{}}'.format(element, fill[idx] + int(4.5 * element.count("\x1b")))
                )),
                "|  "
            )
        print(content_line)

    # Print end line
    print(headers_separator_line)
