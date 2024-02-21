import py5
import numpy as np
import math
import cmath
import networkx as nx
from ortoolpy import chinese_postman
import outline


class Epicycle:
    def __init__(self):
        self.curves = []
        self.plots = np.array([])
        self.plots_dft = np.array([])
        self.num_plots = 0
        self.init_rad = 0.

    def initialize(self, filename, plot_space):
        self.curves = outline.svg2curves(filename)
        self.plots = np.array([point for curve in self.curves for point in curve.get_points(plot_space)])
        print(len(self.plots))
        self.sort_plots(plot_space)
        self.plots_dft = np.fft.fft(self.plots)
        self.num_plots = len(self.plots)
        self.init_rad = 0.

    def sort_plots(self, plot_space):
        # create graph
        graph = nx.Graph()
        # graph.add_nodes_from(self.point2str(plot) for plot in self.plots)
        # for plot in self.plots:
        #     for curve in self.curves:
        #         dist, other = self.get_min_dist_point(plot, curve.get_points(plot_space))
        #         if dist < plot_space * 2.:
        #             graph.add_edge(self.point2str(plot), self.point2str(other))
        # print(1)
        # print(chinese_postman(graph))

    @staticmethod
    def point2str(point):
        return f'({point.real}, {point.imag})'

    @staticmethod
    def get_min_dist_point(point, points):
        min_dist = np.inf
        ret_point = None
        for other in points:
            if other == point:
                continue
            tmp_dist = abs(point - other)
            if tmp_dist < min_dist:
                ret_point = other
        return min_dist, ret_point

    def draw_outline(self):
        py5.push()
        py5.translate(py5.width / 2, py5.height / 2)
        py5.no_fill()
        py5.stroke(0xffffffff)
        for curve in self.curves:
            py5.stroke_weight(0.4)
            curve.draw()
            py5.stroke_weight(4)
            py5.stroke(0xffff0000)
            py5.point(curve.start.real, curve.start.imag)
            py5.stroke(0xff0000ff)
            py5.point(curve.end.real, curve.end.imag)
            py5.stroke(0xffffffff)
        # for plot in self.plots:
        #     py5.point(plot.real, plot.imag)
        py5.pop()

    def update_and_draw(self):
        x = 0.
        y = 0.

        py5.push()
        py5.translate(py5.width / 2, py5.height / 2)
        py5.stroke(0xff0000ff)
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

