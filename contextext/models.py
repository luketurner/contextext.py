import re

REG_ROOT_KEY = "HKEY_CURRENT_USER\\Software\\Classes\\"
REG_VERSION = "Windows Registry Editor Version 5.00"


class ContextEntry(object):
    """ Contains data for a context menu entry.

    TODO Doctest currently not working until I figure out how to do multiline strings without print()

    >>> entry = ContextEntry("name", "text", "command", (".py", ".txt"))

    >>> entry.install_diff
    'Windows Registry Editor Version 5.00\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.py]\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.py\\shell]\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.py\\shell\\name]\n@="text"\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.py\\shell\\name\\command]\n@="command"\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.txt]\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.txt\\shell]\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.txt\\shell\\name]\n@="text"\n\n[HKEY_CURRENT_USER\\Software\\Classes\\.txt\\shell\\name\\command]\n@="command"'

    >>> entry.removal_diff
    'Windows Registry Editor Version 5.00\n\n[-HKEY_CURRENT_USER\\Software\\Classes\\.py\\shell\\name]\n\n[-HKEY_CURRENT_USER\\Software\\Classes\\.py\\shell\\name\\command]\n\n[-HKEY_CURRENT_USER\\Software\\Classes\\.txt\\shell\\name]\n\n[-HKEY_CURRENT_USER\\Software\\Classes\\.txt\\shell\\name\\command]'

    """

    def __init__(self, name=None, text=None, command=None, extensions=None):
        self.name = "" if name is None else name
        self.text = "" if text is None else text
        self.command = "" if command is None else command
        self.extensions = set(() if extensions is None else extensions)

    @property
    def removal_diff(self):
        return REG_VERSION + "\n\n" + self.partial_removal_diff

    @property
    def partial_removal_diff(self):
        return "\n\n".join(self._removal_diff_for_extension(ext, self.name)
                           for ext in self.extensions)

    @property
    def partial_install_diff(self):
        return "\n\n".join(self._install_diff_for_extension(ext, self.name, self.text, self.command)
                           for ext in self.extensions)

    @property
    def install_diff(self):
        return REG_VERSION + "\n\n" + self.partial_install_diff

    def __repr__(self):
        return "<ContextEntry {0} {1}>".format(self.name, self.extensions)

    @staticmethod
    def _quote_cmd(cmd):
        return re.sub('(?<!")%1(?!")', '"%1"', cmd)

    @staticmethod
    def _install_diff_for_extension(ext, name, text, command):
        """
        Returns something like this:
        [HKEY_CURRENT_USER\Software\Classes\.torrent]

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell]

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem]
        @="Menu text here"

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem\command]
        @="cmd.exe"

        """
        root = REG_ROOT_KEY + ext
        return "".join(["[", root, "]",
                        "\n\n[", root, "\\shell", "]",
                        "\n\n[", root, "\\shell\\", name, "]",
                        '\n@="', text, '"',
                        "\n\n[", root, "\\shell\\", name, "\\command]",
                        '\n@="', command, '"'])

    @staticmethod
    def _removal_diff_for_extension(ext, name):
        """
        Returns something like this:

        [-HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem\command]

        [-HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem]
        """
        root = REG_ROOT_KEY + ext
        return "".join(["[-", root, "\\shell\\", name, "]",
                       "\n\n[-", root, "\\shell\\", name, "\\command]"])