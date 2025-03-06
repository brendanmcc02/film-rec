from tempUtils import *

_tempUtils = tempUtils()

def one():
    global _tempUtils
    del _tempUtils
    _tempUtils = tempUtils()
    _tempUtils.setVar(1)

def two():
    _tempUtils.setVar(2)

print(str(_tempUtils.var))
one()
print(str(_tempUtils.var))
two()
print(str(_tempUtils.var))
