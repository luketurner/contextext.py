from re import sub


def quote_cmd(cmd):
    """
    >>> quote_cmd('quote: %1, dont: "%1, dont: %1", dont: "%1"')
    'quote: "%1", dont: "%1, dont: %1", dont: "%1"'
    """
    return sub('(?<!")%1(?!")', '"%1"', cmd)


def to_alphanumeric(name):
    return sub('\\W', '_', name)


def escape_quotes(string):
    return string.replcae('"', '\\"')


def valid_extensions(exts):
    return (ext if ext is "*" else sub('[^\\w.]', '_', ext)
            for ext in exts if (ext is "*" or ext is "Directory" or ext is "Background" or ext[0] is "."))