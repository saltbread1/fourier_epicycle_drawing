from abc import ABCMeta, abstractmethod
import numpy as np
import py5


class Curve(metaclass=ABCMeta):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @abstractmethod
    def get_points(self, dl):
        pass

    @abstractmethod
    def draw(self):
        pass


class Line(Curve):
    def __init__(self, start, end):
        super().__init__(start, end)

    def get_points(self, dl):
        return np.array([(1.-t)*self.start + t*self.end for t in np.arange(0, 1, dl/abs(self.end - self.start))])

    def draw(self):
        py5.line(self.start.real, self.start.imag, self.end.real, self.end.imag)


class CubicBezier(Curve):
    def __init__(self, start, control1, control2, end):
        super().__init__(start, end)
        self.control1 = control1
        self.control2 = control2

    def get_points(self, dl):
        points = np.array([self.calc_bezier(t) for t in np.arange(0, 1, 0.01)])
        cache = 0.
        ret = [points[0]]
        for i in range(1, len(points)):
            curr = points[i]
            prev = points[i-1]
            cache += abs(curr - prev)
            if cache > dl:
                ret.append(curr)
                cache = 0.
        return np.array(ret)

    def calc_bezier(self, t):
        term0 = (1.-t)*(1.-t)*(1.-t)*self.start
        term1 = 3.*t*(1.-t)*(1.-t)*self.control1
        term2 = 3.*t*t*(1.-t)*self.control2
        term3 = t*t*t*self.end
        return term0 + term1 + term2 + term3

    def draw(self):
        py5.bezier(self.start.real, self.start.imag,
                   self.control1.real, self.control1.imag,
                   self.control2.real, self.control2.imag,
                   self.end.real, self.end.imag)
