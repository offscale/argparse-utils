from argparse import Action


class ChannelAction(Action):
    """
    Argparse action for handling channels
    """

    def __call__(self, parser, namespace, values, option_string=None):
        if values.isdigit():
            values = int(values)
            if values not in (1, 3):
                parser.error('channels must be `1` or `3`')
            values = (None, 'grayscale', None, 'rgb')[values]
        setattr(namespace, self.dest, values)
