from importlib import import_module

PATH_SEPARATOR = '.'


def import_class(class_path: str):
    """
    Gets class reference from a module path
    :param class_path: path to the Class from the root module
    :return: class reference
    """

    module = PATH_SEPARATOR.join(class_path.split(PATH_SEPARATOR)[:-1])
    class_name = class_path.split(PATH_SEPARATOR)[-1]
    return getattr(import_module(module), class_name)
