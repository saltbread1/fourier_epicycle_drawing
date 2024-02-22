from abc import ABCMeta, abstractmethod
import numpy as np
import py5


class Curve(metaclass=ABCMeta):
    def __init__(self, start, end, color=0xffffffff):
        self.start = start
        self.end = end
        self.color = color

    def translate(self, c):
        self.start += c
        self.end += c

    def scale(self, c):
        self.start = self.complex_scale(self.start, c)
        self.end = self.complex_scale(self.end, c)

    def reverse(self):
        tmp = self.start
        self.start = self.end
        self.end = tmp

    @staticmethod
    def complex_scale(x, c):
        return complex(x.real * c.real, x.imag * c.imag)

    @abstractmethod
    def get_length(self):
        pass

    @abstractmethod
    def get_points(self, dl):
        pass

    @abstractmethod
    def draw(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Curve):
            return False
        return self.start == other.start and self.end == other.end


class Line(Curve):
    def __init__(self, start, end, color=0xffffffff):
        super().__init__(start, end, color)

    def get_length(self):
        return abs(self.start - self.end)

    def get_points(self, dl):
        return np.array([(1.-t)*self.start + t*self.end for t in np.arange(0, 1, dl/abs(self.end - self.start))])

    def draw(self):
        py5.stroke(self.color)
        py5.line(self.start.real, self.start.imag, self.end.real, self.end.imag)


class CubicBezier(Curve):
    def __init__(self, start, control1, control2, end, color=0xffffffff):
        super().__init__(start, end, color)
        self.control1 = control1
        self.control2 = control2

    def translate(self, c):
        super().translate(c)
        self.control1 += c
        self.control2 += c

    def scale(self, c):
        super().scale(c)
        self.control1 = self.complex_scale(self.control1, c)
        self.control2 = self.complex_scale(self.control2, c)

    def reverse(self):
        super().reverse()
        tmp = self.control1
        self.control1 = self.control2
        self.control2 = tmp

    def get_length(self):
        bezier_points = np.array([self.get_bezier_point(t) for t in np.arange(0, 1, 0.01)])
        l = 0.
        for i in range(1, len(bezier_points)):
            curr = bezier_points[i]
            prev = bezier_points[i-1]
            l += abs(curr - prev)
        return l

    def get_points(self, dl):
        # bezier_points = np.array([self.get_bezier_point(t) for t in np.arange(0, 1, 0.01)])
        # cache = 0.
        # ret = [bezier_points[0]]
        # for i in range(1, len(bezier_points)):
        #     curr = bezier_points[i]
        #     prev = bezier_points[i-1]
        #     cache += abs(curr - prev)
        #     if cache > dl:
        #         ret.append(curr)
        #         cache = 0.
        # return np.array(ret)
        return np.array([self.get_bezier_point(t) for t in np.arange(0, 1, dl / self.get_length())])

    def get_bezier_point(self, t):
        term0 = (1.-t)*(1.-t)*(1.-t)*self.start
        term1 = 3.*t*(1.-t)*(1.-t)*self.control1
        term2 = 3.*t*t*(1.-t)*self.control2
        term3 = t*t*t*self.end
        return term0 + term1 + term2 + term3

    def draw(self):
        py5.stroke(self.color)
        py5.bezier(self.start.real, self.start.imag,
                   self.control1.real, self.control1.imag,
                   self.control2.real, self.control2.imag,
                   self.end.real, self.end.imag)
