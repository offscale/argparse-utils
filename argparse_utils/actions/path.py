from argparse import ArgumentTypeError
from os import path


# Originally from https://stackoverflow.com/a/33181083
class PathType(object):
    def __init__(self, exists=True, type="file", dash_ok=True):
        """

        :param exists:
                True: a path that does exist
                False: a path that does not exist, in a valid parent directory
                None: don't care
        :type exists: bool or None

        :param type: file, dir, symlink, None, or a function returning True for valid paths
                     None: don't care
        :type type: str or bool or None or (() -> bool or None) or ((str) -> bool or None)

        :param dash_ok: whether to allow "-" as stdin/stdout
        :type dash_ok: bool
        """

        assert exists in (True, False, None)
        assert type in ("file", "dir", "symlink", None) or hasattr(type, "__call__")

        self._exists = exists
        self._type = type
        self._dash_ok = dash_ok

    def __call__(self, string):
        """

        :param string:
        :type string: str
        """
        if string == "-":
            # the special argument "-" means sys.std{in,out}
            if self._type == "dir":
                raise ArgumentTypeError(
                    "standard input/output (-) not allowed as directory path"
                )
            elif self._type == "symlink":
                raise ArgumentTypeError(
                    "standard input/output (-) not allowed as symlink path"
                )
            elif not self._dash_ok:
                raise ArgumentTypeError("standard input/output (-) not allowed")
        else:
            e = path.exists(string)
            if self._exists:
                if not e:
                    raise ArgumentTypeError("path does not exist: '{}'".format(string))

                if self._type is None:
                    pass
                elif self._type == "file":
                    if not path.isfile(string):
                        raise ArgumentTypeError(
                            "path is not a file: '{}'".format(string)
                        )
                elif self._type == "symlink":
                    if not path.islink(string):
                        raise ArgumentTypeError(
                            "path is not a symlink: '{}'".format(string)
                        )
                elif self._type == "dir":
                    if not path.isdir(string):
                        raise ArgumentTypeError(
                            "path is not a directory: '{}'".format(string)
                        )
                else:
                    raise ArgumentTypeError("path not valid: '{}'".format(string))
            else:
                if not self._exists and e:
                    raise ArgumentTypeError("path exists: '{}'".format(string))

                p = path.dirname(path.normpath(string)) or "."
                if not path.isdir(p):
                    raise ArgumentTypeError(
                        "parent path is not a directory: '{}'".format(p)
                    )
                elif not path.exists(p):
                    raise ArgumentTypeError(
                        "parent directory does not exist: '{}'".format(p)
                    )
