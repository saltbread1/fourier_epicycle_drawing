if __name__ == '__main__':
    # need java 17 for py5
    from os import environ
    environ['JAVA_HOME'] = environ.get('TMP_JAVA17_HOME')

import py5
import numpy as np
import image_outline


def setup():
    py5.size(512, 512)
    py5.background(0xff000000)

    curves = image_outline.get_image_outline('sample.svg')
    py5.no_fill()
    py5.stroke(0xffffffff)
    for curve in curves:
        curve.draw()


def draw():
    pass


py5.run_sketch()
