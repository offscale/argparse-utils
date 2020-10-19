from _ast import Import, ImportFrom
from ast import parse

from argparse_utils.backports.resolve_name import resolve_name

symbols = {}


def import_arg(name, update_locals=True, symbol_table=None):
    if symbol_table is None:
        global symbols
    else:
        symbols = symbol_table

    if not name.startswith("from") and not name.startswith("import"):
        name = "import {name}".format(name=name)

    import_node = parse(name).body[0]

    def parse_name(node, import_from, module):
        if node.asname is None:
            alias = module or node.name
            if import_from:
                imports = ".".join((alias, node.name))
                alias = node.name
            else:
                imports = alias
        else:
            alias, imports = node.asname, node.name
        return alias, resolve_name(imports)

    assert isinstance(import_node, (Import, ImportFrom))

    # print_ast(import_node)
    for name in import_node.names:
        import_from = isinstance(import_node, ImportFrom)
        k, v = parse_name(
            node=name,
            module=import_node.module if import_from else None,
            import_from=import_from,
        )
        if k in symbols:
            if isinstance(symbols[k], list):
                symbols[k].append(v)
            else:
                symbols[k] = [symbols[k], v]
        else:
            symbols[k] = v

    if update_locals:
        globals().update(symbols)
