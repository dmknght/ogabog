import argparse
import sys

DEF_FLAG_MODULE = "-p"


class ArgumentParser(argparse.ArgumentParser):
    # Disable exit on error to get parameters of arguments
    # https://stackoverflow.com/a/16942165
    def error(self, message):
        print(message)

    def print_help(self, file=None):
        try:
            # Find the args that contains "-p" flag
            pos = sys.argv.index(DEF_FLAG_MODULE)
            module_name = sys.argv[pos + 1]
            if not module_name.startswith("-"):
                print("Module " + module_name)
                # This could be the actual name of module, we try import it
                # Classes like bind / reverse in 1 module
                # https://stackoverflow.com/a/22578562
                # Old method with inspect to get class names and print help
                import importlib
                module = importlib.import_module("modules." + module_name.replace("/", "."))
                # New method to get all names of classes in module
                # Try to print_help() with args
                # https://stackoverflow.com/a/21563930
                for key, obj in module.__dict__.items():
                    if isinstance(obj, type):
                        print("\n" + key)
                        # TODO overwrite the usage help
                        # Help by now `usage: main.py [-h] [--ip IP] [--Port PORT]`
                        # Expected help: `usage: main.py -p <module_name> -c <classname> [-h] [--ip IP] [--Port PORT]`
                        obj().show_help(module_name, key)

            else:
                # Wrong module name
                self._print_message(self.format_help(), file)
                self._print_message("\nInvalid module name\n")
        except ValueError:
            self._print_message(self.format_help(), file)
        except ModuleNotFoundError:
            self._print_message(self.format_help(), file)
            self._print_message("\nInvalid module name\n")


def core_args():
    # https://github.com/zeropointdynamics/zelos/blob/0c5bd57b4bab56c23c27dc5301ba1a42ee054726/src/zelos/config_gen.py#L77
    parser = ArgumentParser()
    group_core = parser.add_argument_group("Core")
    group_core.add_argument(
        "-l",
        action='store_true',
        default=False,
        help="List all modules"
    )
    group_core.add_argument(
        DEF_FLAG_MODULE,
        metavar='Module',
        help="Select module"
    )
    group_core.add_argument(
        "-c",
        metavar='Class',
        help="Class of module"
    )
    return parser
