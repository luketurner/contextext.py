from .entry import ContextEntry

def new(name, text, command, *extensions):
    entry = ContextEntry()
    entry.name(name)
    entry.text(text)
    entry.command(command)
    entry.extensions(set(extensions))
    return entry
