import argparse
from argparse import ArgumentError
# from ogabog.cores.controller import check_env
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
        module_name = ""
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
                        print(f"Help module: {module_name}")
                        module.show_help(module_name, class_name)
                        return
                    except AttributeError:
                        print(f"Class not found {class_name}! Show help for all classes!")
                        pass
                except ValueError:
                    pass

                # https://stackoverflow.com/a/22578562
                # Old method with inspect to get class names and print help
                # New method to get all names of classes in module
                # https://stackoverflow.com/a/21563930
                import importlib
                module = importlib.import_module("modules." + module_name.replace("/", "."))
                print(f"Help module: {module_name}")
                for key, obj in module.__dict__.items():
                    if isinstance(obj, type):
                        print(f"\n{key}")
                        # Show custom help of each module
                        obj().show_help(module_name, key)

            else:
                # Wrong module name
                self._print_message(self.format_help(), file)
                self._print_message(f"\nInvalid module name {module_name}")
        except ValueError:
            self._print_message(self.format_help(), file)
        except ModuleNotFoundError:
            self._print_message(self.format_help(), file)
            self._print_message(f"\nInvalid module name {module_name}")


class PluginArgumentParser(argparse.ArgumentParser):
    def _check_value(self, action, value):
        """
        Custom function from original check value of choices
        https://github.com/python/cpython/blob/master/Lib/argparse.py#L2494
        :param action:
        :param value:
        :return:
        """

        if action.choices is not None and value not in action.choices\
                and value not in [x.split("/")[-1] for x in action.choices]:
            raise ArgumentError(action, "invalid choice: {} from {}".format(value, action.choices))
            # Comment: Here we try to convert user's choice to full path from list of choice
            # Then we use flag --env to convert / not convert it to full path / binary name only
            # For now the "value" is local variable only so it doesn't work
            # check_value = check_env(value, action.choices)
            # if not check_value:
            #     raise ArgumentError(action, "invalid choice: {} from {}".format(value, action.choices))
            # else:
            #     value = check_value


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
