import py5
import numpy as np
import math
import cmath
import networkx as nx
from ortoolpy import chinese_postman
import outline
from curve import Line, CubicBezier


class Epicycle:
    def __init__(self):
        self.curves = []
        self.path = []
        self.plots = np.array([])
        self.plots_dft = np.array([])
        self.num_plots = 0
        self.init_rad = 0.

    def initialize(self, filename, plot_space):
        curves = self.create_curve(filename, 8)
        path = self.calc_drawing_path(curves)
        self.curves = self.sort_curves(curves, path)
        # self.curves = curves
        self.path = path
        print(len(curves), len(path), len(self.curves))
        self.plots = np.array([point for curve in self.curves for point in curve.get_points(plot_space)])
        print(len(self.plots))
        self.plots_dft = np.fft.fft(self.plots)
        self.num_plots = len(self.plots)
        self.init_rad = 0.

    def create_curve(self, filename, dist_thresh):
        curves = outline.svg2curves(filename)

        # gather together nearby points
        # for this_curve in curves:
        #     # set of start and end
        #     min_dists = [np.inf, np.inf]
        #     other_points = [None, None]
        #
        #     for other_curve in curves:
        #         if this_curve.__eq__(other_curve):
        #             continue
        #         for other_anchor in [other_curve.start, other_curve.end]:
        #             tmp_dists = [abs(other_anchor - this_curve.start), abs(other_anchor - this_curve.end)]
        #             # avoid curve.start = curve.end
        #             if tmp_dists[0] < min_dists[0] and tmp_dists[1] > dist_thresh:
        #                 min_dists[0] = tmp_dists[0]
        #                 other_points[0] = other_anchor
        #             if tmp_dists[1] < min_dists[1] and tmp_dists[0] > dist_thresh:
        #                 min_dists[1] = tmp_dists[1]
        #                 other_points[1] = other_anchor
        #     if min_dists[0] < dist_thresh:
        #         this_curve.start = other_points[0]
        #     if min_dists[1] < dist_thresh:
        #         this_curve.end = other_points[1]
        #
        # for this_curve in curves:
        #     if this_curve.start == this_curve.end:
        #         curves.remove(this_curve)
        #         print(1)

        return curves

    def calc_drawing_path(self, curves):
        # create graph based on a curve set
        graph = nx.Graph()
        for curve in curves:
            start = self.complex2string(curve.start)
            end = self.complex2string(curve.end)
            graph.add_node(start)
            graph.add_node(end)
            graph.add_weighted_edges_from([(start, end, curve.get_length())])

        # make it a single connected graph
        for component in nx.connected_components(graph):
            if len(list(nx.connected_components(graph))) == 1:
                break
            this_points = [self.string2complex(x) for x in component]
            min_dist = np.inf
            min_points = None
            for this_point in this_points:
                other_points = [self.string2complex(x) for x in graph if x not in component]
                tmp_dist, other_point = self.get_min_dist_point(this_point, other_points)
                if tmp_dist < min_dist:
                    min_dist = tmp_dist
                    min_points = [this_point, other_point]
            edge = [(self.complex2string(min_points[0]), self.complex2string(min_points[1]), min_dist)]
            graph.add_weighted_edges_from(edge)

        # solve Chinese Postman Problem
        _, path = chinese_postman(graph)
        return path

    def sort_curves(self, curves, path):
        # return [self.get_curve(curves, anchor) for anchor in path]
        ret = []
        tmp = 0
        for anchor in path:
            curve = self.get_curve(curves, anchor)
            if curve is not None:
                ret.append(curve)
            else:
                tmp += 1
        print(tmp)
        return ret

    def get_curve(self, curves, anchor):
        start = self.string2complex(anchor[0])
        end = self.string2complex(anchor[1])
        for curve in curves:
            if curve.start == start and curve.end == end:
                return curve
            elif curve.start == end and curve.end == start:
                curve.reverse()
                return curve
        return Line(start, end)

    @staticmethod
    def complex2string(c):
        return f'{c.real},{c.imag}'

    @staticmethod
    def string2complex(str):
        x, y = str.split(',')
        return complex(float(x), float(y))

    @staticmethod
    def get_min_dist_point(point, all_points):
        min_dist = np.inf
        other_point = None
        for other in all_points:
            if other == point:
                continue
            tmp_dist = abs(point - other)
            if tmp_dist < min_dist:
                min_dist = tmp_dist
                other_point = other
        return min_dist, other_point

    def draw_outline(self):
        py5.push()
        py5.translate(py5.width / 2, py5.height / 2)
        py5.no_fill()
        # curves
        py5.stroke(0xffffffff)
        py5.stroke_weight(0.4)
        for curve in self.curves:
            curve.draw()
        # start points
        py5.stroke_weight(4)
        py5.stroke(0xffff0000)
        for curve in self.curves:
            py5.point(curve.start.real, curve.start.imag)
        # end points
        py5.stroke_weight(2)
        py5.stroke(0xff0000ff)
        for curve in self.curves:
            py5.point(curve.end.real, curve.end.imag)
        # all plots
        # for plot in self.plots:
        #     py5.point(plot.real, plot.imag)
        # anchors of path
        py5.stroke_weight(3)
        py5.stroke(0xff00ff00)
        for p in self.path:
            start = self.string2complex(p[0])
            end = self.string2complex(p[1])
            py5.point(start.real, start.imag)
            py5.point(end.real, end.imag)
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

