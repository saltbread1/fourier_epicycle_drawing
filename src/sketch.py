if __name__ == '__main__':
    # need java 17 for py5
    from os import environ
    environ['JAVA_HOME'] = environ.get('TMP_JAVA17_HOME')

import py5
import epicycle

renderer = epicycle.Epicycle()


def setup():
    py5.size(512, 512)
    py5.frame_rate(60)
    py5.background(0xff000000)
    renderer.initialize('sample.svg', 0.5)
    renderer.export_fourier_series(256)


def draw():
    py5.background(0xff000000)
    renderer.update_and_draw(256, 0.008)


def key_pressed():
    renderer.start_animation()


py5.run_sketch()
