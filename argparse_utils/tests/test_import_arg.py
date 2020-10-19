
from functools import partial
from platform import python_version_tuple
from unittest import TestCase, main as unittest_main

import argparse

if python_version_tuple() < ("3", "8"):
    # Taken from https://github.com/python/cpython/pull/10205
    def _registry_get(self, registry_name, value, default=None):
        try:
            return self._registries[registry_name].get(value, default)
        except TypeError:
            # probably TypeError: unhashable type: 'dict', e.g. {}.get
            return default

    argparse._ActionsContainer._registry_get = _registry_get

import pip

from argparse_utils.types.import_arg import import_arg



class TestImportArg(TestCase):
    def setUp(self):
        self.symbol_table = {}
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("--foo", type=self.symbol_table.__getitem__)
        self.parser.add_argument(
            "--import", type=partial(import_arg, symbol_table=self.symbol_table)
        )

    def test_provided_import(self):
        args = self.parser.parse_args(
            ("--import", "from pip import __version__", "--foo", "__version__")
        )

        self.assertIsNone(getattr(args, "import"))
        self.assertEqual(args.foo, pip.__version__)

        self.assertIn("__version__", self.symbol_table)
        self.assertEqual(self.symbol_table["__version__"], pip.__version__)

    def test_not_provided_import(self):
        self.assertRaises(
            KeyError, lambda: self.parser.parse_args(("--foo", "__version__"))
        )

        # except KeyError as e:
        #    self.parser.error('Missing `--import` to bring this symbol into scope: {!s}'.format(e))


if __name__ == "__main__":
    unittest_main()
