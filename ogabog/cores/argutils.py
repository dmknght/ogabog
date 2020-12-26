import argparse
import sys

DEF_FLAG_MODULE = "-p"
DEF_FLAG_CLASS = "-c"


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """
        Disable exit on error to get parameters of arguments
        https://stackoverflow.com/a/16942165
        :param message: error message
        :return:
        """
        print(message)

    def print_help(self, file=None):
        """
        Custom help module for argparse
        If module is not defined, we print only help
        If module is defined, we print help for module
        :param file:
        :return:
        """
        try:
            # Find the args that contains "-p" flag
            pos = sys.argv.index(DEF_FLAG_MODULE)
            module_name = sys.argv[pos + 1]
            # Ignore if argv starts with "-". Module name shouldn't have it
            if not module_name.startswith("-"):
                # If user defines class name, try to print only class name then quit
                try:
                    pos = sys.argv.index(DEF_FLAG_CLASS)
                    class_name = sys.argv[pos + 1]
                    import importlib
                    module = importlib.import_module("modules." + module_name.replace("/", "."))
                    try:
                        module = getattr(module, class_name)()
                        print("Module " + module_name)  # TODO better msg for print module name and classes
                        module.show_help(module_name, class_name)
                        return
                    except AttributeError:
                        pass
                except ValueError:
                    pass

                # https://stackoverflow.com/a/22578562
                # Old method with inspect to get class names and print help
                # New method to get all names of classes in module
                # https://stackoverflow.com/a/21563930
                import importlib
                module = importlib.import_module("modules." + module_name.replace("/", "."))
                print("Module " + module_name)  # TODO better msg for print module name and classes
                for key, obj in module.__dict__.items():
                    if isinstance(obj, type):
                        print("\n" + key)
                        # Show custom help of each module
                        obj().show_help(module_name, key)

            else:
                # Wrong module name
                self._print_message(self.format_help(), file)
                self._print_message("\nInvalid module name " + module_name)
        except ValueError:
            self._print_message(self.format_help(), file)
        except ModuleNotFoundError:
            self._print_message(self.format_help(), file)
            self._print_message("\nInvalid module name " + module_name)


def core_args():
    """
    Add custom arguments for framework (core)
    :return: ArgumentParser object
    """
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
        DEF_FLAG_CLASS,
        metavar='Class',
        help="Class of module"
    )
    return parser
