import py5
import numpy as np
import math
import networkx as nx
from ortoolpy import chinese_postman
import codecs
import outline
from curve import Line


class Epicycle:
    def __init__(self):
        self.circle_center = 0
        self.image_center = 0
        self.smp_size = 0.
        self.plots_dft_x = np.array([])
        self.plots_dft_y = np.array([])
        self.init_rad = 0.
        self.point_list = []

    def initialize(self, filename, smp_dist_interval, circle_center=0, image_center=0):
        self.circle_center = circle_center
        self.image_center = image_center

        curves = outline.svg2curves(filename, image_center - circle_center)
        path = self.calc_drawing_path(curves)
        curves = [self.get_curve_from_anchor(curves, anchor) for anchor in path]
        plots = [point for curve in curves for point in curve.get_points(smp_dist_interval)]
        self.smp_size = len(plots)
        print(f'sample size: {self.smp_size}')
        self.plots_dft_x = np.fft.fft([p.real for p in plots])
        self.plots_dft_y = np.fft.fft([p.imag for p in plots])

        self.start_animation()

    def start_animation(self):
        self.init_rad = 0.
        self.point_list = []

    def calc_drawing_path(self, curves):
        # create graph based on a curve set
        # this is probably disconnected graph
        g = nx.Graph()
        for curve in curves:
            start = (curve.start.real, curve.start.imag)
            end = (curve.end.real, curve.end.imag)
            g.add_node(start)
            g.add_node(end)
            g.add_edge(start, end, weight=curve.get_length())

        # make it a single connected graph
        while True:
            components = list(nx.connected_components(g))
            if len(components) == 1:
                break
            component = components[0]
            this_points = [complex(x[0], x[1]) for x in component]
            min_dist = math.inf
            min_points = None
            for this_point in this_points:
                other_points = [complex(x[0], x[1]) for x in g if x not in component]
                tmp_dist, other_point = self.get_min_dist_point(this_point, other_points)
                if tmp_dist < min_dist:
                    min_dist = tmp_dist
                    min_points = [this_point, other_point]
            g.add_edge((min_points[0].real, min_points[0].imag),
                       (min_points[1].real, min_points[1].imag),
                       weight=min_dist)
        print(f'the number of edges: {len(g.edges())}')

        cache_g = nx.Graph(g)

        # solve Chinese Postman Problem
        total_weight, one_stroke_path = chinese_postman(g)

        # not to stray too far from the outline
        ret = []
        for edge in one_stroke_path:
            if edge[1] in nx.neighbors(cache_g, edge[0]):
                ret.append(edge)
                continue
            nodes = nx.shortest_path(cache_g, edge[0], edge[1])
            path = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
            if sum(cache_g[u][v]['weight'] for u, v in path) < total_weight * 0.02:
                ret.extend(path)
            else:
                ret.append(edge)
        return ret

    @staticmethod
    def get_curve_from_anchor(curves, anchor):
        start = complex(anchor[0][0], anchor[0][1])
        end = complex(anchor[1][0], anchor[1][1])
        for curve in curves:
            if curve.start == start and curve.end == end:
                return curve.copy()
            elif curve.start == end and curve.end == start:
                return curve.reverse()
        return Line(start, end, 0xffff0000)

    @staticmethod
    def get_min_dist_point(point, all_points):
        min_dist = math.inf
        other_point = None
        for other in all_points:
            if other == point:
                continue
            tmp_dist = abs(point - other)
            if tmp_dist < min_dist:
                min_dist = tmp_dist
                other_point = other
        return min_dist, other_point

    def update_and_draw(self, deg, dt):
        py5.push()
        py5.translate(py5.width / 2, py5.height / 2)
        py5.translate(self.circle_center.real, self.circle_center.imag)
        py5.no_fill()
        py5.stroke(0xffffffff)
        for n in range(len(self.point_list)-1):
            p0 = self.point_list[n]
            p1 = self.point_list[n+1]
            py5.line(p0.real, p0.imag, p1.real, p1.imag)

        if self.init_rad >= math.tau:
            py5.pop()
            return

        f = 0.
        py5.stroke(0xff0000ff)
        for n in range(deg):
            rad = self.init_rad * n
            x = (self.plots_dft_x[n].real * math.cos(rad) + self.plots_dft_x[n].imag * math.sin(rad)) * 2. / self.smp_size
            y = (self.plots_dft_y[n].real * math.cos(rad) + self.plots_dft_y[n].imag * math.sin(rad)) * 2. / self.smp_size
            if n == 0:
                x *= 0.5
                y *= 0.5
            r = math.sqrt(x*x+y*y)
            py5.ellipse(f.real, f.imag, 2. * r, 2. * r)
            f += complex(x, y)

        self.point_list.append(f)
        self.init_rad += dt

        py5.no_stroke()
        py5.fill(0xffff0000)
        py5.ellipse(f.real, f.imag, 8, 8)
        py5.pop()

    def export_fourier_series(self, deg, filename='fourier_series.txt'):
        series_x = f'{self.plots_dft_x[0].real / self.smp_size:.3f}'
        series_y = f'{self.plots_dft_y[0].real / self.smp_size:.3f}'
        for n in range(1, deg):
            rx = abs(self.plots_dft_x[n]) * 2. / self.smp_size
            ry = abs(self.plots_dft_y[n]) * 2. / self.smp_size
            phix = math.atan2(self.plots_dft_x[n].real, self.plots_dft_x[n].imag)
            phiy = math.atan2(self.plots_dft_y[n].real, self.plots_dft_y[n].imag)
            opx = '+' if phix > 0 else '-' if phix < 0 else ''
            opy = '+' if phiy > 0 else '-' if phiy < 0 else ''
            series_x += f' + {rx:.3f}sin({n}t{opx}{abs(phix):.3f})'
            series_y += f' + {ry:.3f}sin({n}t{opy}{abs(phiy):.3f})'
        print(f'x = {series_x}\ny = {series_y}', file=codecs.open(filename, 'w', 'utf-8'))
