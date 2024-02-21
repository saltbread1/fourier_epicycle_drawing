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
        self.curves = self.create_curve(filename, 8)
        print(len(self.curves))
        # self.plots = np.array([point for curve in self.curves for point in curve.get_points(plot_space)])
        # print(len(self.plots))
        # self.sort_plots(plot_space)
        # self.plots_dft = np.fft.fft(self.plots)
        # self.num_plots = len(self.plots)
        # self.init_rad = 0.

    def create_curve(self, filename, dist_thresh):
        curves = outline.svg2curves(filename)
        # anchors = np.array([point for curve in curves for point in [curve.start, curve.end]])
        # for curve in curves:
        #     if curve.get_length() < dist_thresh:
        #         curves.remove(curve)
        #         print(curve.start, curve.end)

        # for curve in curves:
        #     # set of start and end
        #     min_dists = [np.inf, np.inf]
        #     other_points = [None, None]
        #
        #     for other in curves:
        #         if curve.__eq__(other):
        #             continue
        #         for anchor in [other.start, other.end]:
        #             tmp_dists = [abs(anchor - curve.start), abs(anchor - curve.end)]
        #             # min_dists = [min(tmp_dists[i], min_dists[i]) for i in range(2)]
        #             if tmp_dists[0] < min_dists[0] and tmp_dists[1] > dist_thresh:
        #                 min_dists[0] = tmp_dists[0]
        #                 other_points[0] = anchor
        #             if tmp_dists[1] < min_dists[1] and tmp_dists[0] > dist_thresh:
        #                 min_dists[1] = tmp_dists[1]
        #                 other_points[1] = anchor
        #     if min_dists[0] < dist_thresh:
        #         curve.start = other_points[0]
        #     if min_dists[1] < dist_thresh:
        #         curve.end = other_points[1]
        #
        # for curve in curves:
        #     if curve.start == curve.end:
        #         curves.remove(curve)
        #         print(1)

        return curves

    def create_eulerian_graph(self):
        graph = nx.Graph()
        for curve in self.curves:
            start = self.complex2string(curve.start)
            end = self.complex2string(curve.end)
            graph.add_node(start)
            graph.add_node(end)
            graph.add_edge(start, end, weight=curve.get_length())
        

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
    def complex2string(c):
        return f'{c.real}, {c.imag}'

    @staticmethod
    def string2complex(str):
        x, y = str.split(',')
        return complex(float(x), float(y))

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
        # curves
        py5.stroke(0xffffffff)
        py5.stroke_weight(0.4)
        for curve in self.curves:
            curve.draw()
        # end points
        py5.stroke_weight(2)
        py5.stroke(0xff0000ff)
        for curve in self.curves:
            py5.point(curve.end.real, curve.end.imag)
        # start points
        py5.stroke_weight(3)
        py5.stroke(0xffff0000)
        for curve in self.curves:
            py5.point(curve.start.real, curve.start.imag)
        # all plots
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

