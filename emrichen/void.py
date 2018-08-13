class VoidType:
    def __str__(self):
        return '<<<Void>>>'

    __repr__ = __str__


Void = VoidType()
