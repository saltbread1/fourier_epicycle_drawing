if __name__ == '__main__':
    # need java 17 for py5
    from os import environ
    environ['JAVA_HOME'] = environ.get('TMP_JAVA17_HOME')

import py5
import outline


def setup():
    py5.size(512, 512)
    py5.background(0xff000000)

    curves = outline.svg2curves('sample.svg')
    py5.push()
    py5.translate(py5.width/2, py5.height/2)
    py5.no_fill()
    py5.stroke(0xffffffff)
    for curve in curves:
        curve.draw()
        # for point in curve.get_points(6):
        #     py5.point(point.real, point.imag)
    py5.pop()


def draw():
    pass


py5.run_sketch()
