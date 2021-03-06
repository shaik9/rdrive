import sys
from functools_plus.functools_plus import *

def test():
    from math import radians, degrees, pi

    class Angle(object):
        def __init__(self,rad):
            self._rad = rad
            print hasattr(Angle.deg,'__annotations__')

        @property
        @annotate(name='spam', tomato=42)
        def rad(self):
            '''The angle in radians'''
            return self._rad
        @rad.setter
        def rad(self,angle):
            if isinstance(angle,Angle): angle = angle.rad
            self._rad = float(angle)


        @annotate(name='spam', tomato=42)
        @Property
        def deg():
            '''The angle in degrees'''
            def fget(self):
                return degrees(self._rad)
            def fset(self,angle):
                if isinstance(angle,Angle): angle = angle.deg
                self._rad = radians(angle)


    def almostEquals(x,y):
        return abs(x-y) < 1e-9

    a = Angle(pi/3)
    assert a.rad == pi/3 and almostEquals(a.deg, 60)
    a.rad = pi/4
    assert a.rad == pi/4 and almostEquals(a.deg, 45)
    a.deg = 30
    assert a.rad == pi/6 and almostEquals(a.deg, 30)
    print Angle.rad.__doc__
    print Angle.deg.__doc__
    
class m(property):
    pass


def Property(function):
    keys = 'fget', 'fset', 'fdel'
    func_locals = {'doc':function.__doc__}
    def probeFunc(frame, event, arg):
        if event == 'return':
            locals = frame.f_locals
            func_locals.update(dict((k,locals.get(k)) for k in keys))
            sys.settrace(None)
        return probeFunc
    sys.settrace(probeFunc)
    function()
    return m(**func_locals)


if __name__ == '__main__':
    test()
