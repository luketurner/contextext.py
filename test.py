import contextext as c

a = c.new("Name", "description", "command %1", ".ext1", ".ext2")

print(a.diff(True))
