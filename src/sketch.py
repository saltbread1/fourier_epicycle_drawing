if __name__ == '__main__':
    # need java 17 for py5
    from os import environ
    environ['JAVA_HOME'] = environ.get('TMP_JAVA17_HOME')

import py5
import epicycle

renderer = epicycle.Epicycle()


def setup():
    py5.size(512, 512)
    py5.background(0xff000000)
    renderer.initialize('sample.svg', 8)


def draw():
    py5.background(0xff000000)
    renderer.draw_outline()
    #renderer.update_and_draw()


py5.run_sketch()
