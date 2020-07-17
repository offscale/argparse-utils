from argparse import ArgumentParser
from functools import partial
from unittest import TestCase, main as unittest_main

import pip

from argparse_utils.types.import_arg import import_arg


class TestImportArg(TestCase):
    def setUp(self):
        self.symbol_table = {}
        self.parser = ArgumentParser()

        self.parser.add_argument('--foo', type=self.symbol_table.__getitem__)
        self.parser.add_argument('--import', type=partial(import_arg, symbol_table=self.symbol_table))

    def test_provided_import(self):
        args = self.parser.parse_args((
            '--import', 'from pip import __version__',
            '--foo', '__version__'
        ))

        self.assertIsNone(getattr(args, 'import'))
        self.assertEqual(args.foo, pip.__version__)

        self.assertIn('__version__', self.symbol_table)
        self.assertEqual(self.symbol_table['__version__'], pip.__version__)

    def test_not_provided_import(self):
        self.assertRaises(
            KeyError,
            lambda: self.parser.parse_args((
                '--foo', '__version__'
            ))
        )

        # except KeyError as e:
        #    self.parser.error('Missing `--import` to bring this symbol into scope: {!s}'.format(e))


if __name__ == '__main__':
    unittest_main()
