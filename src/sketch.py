from os import environ
# need java 17 for py5
environ['JAVA_HOME'] = environ.get('TMP_JAVA_HOME')

import py5
import numpy as np
import math
import cmath


SMP_NUM = 512
init_rad = 0.


def setup():
    py5.size(400, 400)
    py5.background(0xff000000)


def draw():
    global init_rad

    py5.background(0xff000000)

    plots = create_plots(SMP_NUM)
    py5.no_stroke()
    py5.fill(0xff0000ff)
    for p in plots:
        py5.ellipse(p.real, p.imag, 3, 3)

    dft = np.fft.fft(plots)
    x = 0.
    y = 0.
    py5.stroke(0xffffffff)
    py5.no_fill()
    for i in range(SMP_NUM):
        f = dft[i].item()
        r = abs(f) / SMP_NUM
        rad = cmath.phase(f)
        py5.ellipse(x, y, 2.*r, 2.*r)

        x += r * math.cos(i*init_rad + rad)
        y += r * math.sin(i*init_rad + rad)

    py5.no_stroke()
    py5.fill(0xffff0000)
    py5.ellipse(x, y, 10, 10)
    init_rad += math.tau / SMP_NUM


def create_plots(n):
    plots = np.array([])
    for i in range(n):
        x = py5.bezier_point(340, 40, 360, 60, i/n)
        y = py5.bezier_point(80, 40, 360, 320, i/n)
        plots = np.append(plots, complex(x, y))

    return plots


py5.run_sketch()
