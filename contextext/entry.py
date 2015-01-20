import re
from .constants import _VERSION, _ROOT_KEY

class ContextEntry(object):
    _text = ""
    _cmd = ""
    _name = ""
    _extensions = set()

    def _install_code(self, ext_root):
        """
        Returns something like this:
        [HKEY_CURRENT_USER\Software\Classes\.torrent]

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell]

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem]
        @="Menu text here"

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem\command]
        @="cmd.exe"
        
        """        
        return "".join(["[", ext_root, "]",
                       "\n\n[", ext_root, "\\shell", "]",
                       "\n\n[", ext_root, "\\shell\\", self.name(), "]",
                       '\n@="', self.text(), '"',
                       "\n\n[", ext_root, "\\shell\\", self.name(), "\\command]",
                       '\n@="', self.command(), '"'])

    def _removal_code(self, ext_root):
        """
        Returns something like this:
        
        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem\command]

        [HKEY_CURRENT_USER\Software\Classes\.torrent\shell\TestContextItem]
        """
        return "".join(["[-", ext_root, "\\shell\\", self.name(), "]",
                       "\n\n[-", ext_root, "\\shell\\", self.name(), "\\command]"])

    def removal_diff(self, includeVersion = False):
        if includeVersion:
            return _VERSION + "\n\n" + self.removal_diff()
        else:
            return "\n\n".join(self._removal_code(_ROOT_KEY + ext) for ext in self.extensions())

    def diff(self, includeVersion = False):
        if includeVersion:
            return _VERSION + "\n\n" + self.diff()
        else:
            return "\n\n".join(self._install_code(_ROOT_KEY + ext) for ext in self.extensions())

    def name(self, new_name = None):
        if new_name is not None:
            self._name = str(new_name)
        return self._name
    
    def text(self, new_text = None):
        if new_text is not None:
            self._text = str(new_text)
        return self._text

    def command(self, new_cmd = None):
        if new_cmd is not None:
            self._cmd = str(new_cmd)
        return self._cmd

    def extensions(self, new_exts = None):
        if type(new_exts) is set:
            self._extensions = new_exts
        elif new_exts is not None:
            raise ArgumentException("extensions() method expected a set, got a "
                                    + type(new_exts) + ": " + str(new_exts))
        return self._extensions

    def _cmdquote(self, cmd):
        return re.sub('(?<!")%1(?!")', '"%1"', cmd)
