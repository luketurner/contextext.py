# contextext.py - an API for the Windows Explorer Context Menu

Having new items in the Windows Explorer context menu can be nice. 
But it's a pain to add them manually.
This is a simple Python library that makes it easier.

## Todo list

* Escape quotations when generating .reg values
* Add support for direct saving with windows API
* Add support for loading existing extensions with windows API

## Examples

Iterating over existing items:

```python
for entry in c.ext(".txt").all():
	print(entry.text(), entry.command())
```

Creating new items:

```python
entry = c.new("Launch dev server", "cmd /C node %1", ".js") # create a new context menu item
print("Making these changes:")
print(entry.diff()) # print the corresponding registry keys
entry.save() # save the new entry to the registry
with f = open("uninstall.reg", "w"):
	f.write(entry.removal_diff())
```