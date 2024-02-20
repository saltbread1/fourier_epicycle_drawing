import py5
import numpy as np
import math
import cmath
import outline


class Epicycle:
    def __init__(self):
        self.curves = []
        self.plots = np.array([])
        self.plots_dft = np.array([])
        self.num_plots = 0
        self.init_rad = 0.

    def initialize(self, filename, speed):
        self.curves = outline.svg2curves(filename)
        self.plots = np.array([point for curve in self.curves for point in curve.get_points(speed)])
        self.plots_dft = np.fft.fft(self.plots)
        self.num_plots = len(self.plots)
        self.init_rad = 0.

    def draw_outline(self):
        py5.push()
        py5.translate(py5.width / 2, py5.height / 2)
        py5.no_fill()
        py5.stroke(0x80ffffff)
        py5.stroke_weight(0.32)
        for curve in self.curves:
            curve.draw()
            # for point in curve.get_points(6):
            #     py5.point(point.real, point.imag)
        py5.pop()

    def update_and_draw(self):
        x = 0.
        y = 0.

        py5.push()
        py5.translate(py5.width / 2, py5.height / 2)
        py5.stroke(0xa00000ff)
        py5.no_fill()
        for i in range(self.num_plots):
            f = self.plots_dft[i].item()
            r = abs(f) / self.num_plots
            rad = cmath.phase(f)
            py5.ellipse(x, y, 2. * r, 2. * r)

            x += r * math.cos(i * self.init_rad + rad)
            y += r * math.sin(i * self.init_rad + rad)

        self.init_rad += math.tau / self.num_plots

        py5.no_stroke()
        py5.fill(0xffff0000)
        py5.ellipse(x, y, 8, 8)
        py5.pop()

