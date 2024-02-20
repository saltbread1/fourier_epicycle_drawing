import os
import xml.etree.ElementTree as ET
import svg.path
import curve


def get_image_outlines(filename):
    filepath = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images', filename)
    tree = ET.parse(filepath)
    root = tree.getroot()

    # get translate and scale
    g = root.find('.//{http://www.w3.org/2000/svg}g')
    transform = g.get('transform')
    translate = None
    scale = None
    if transform is not None:
        parts = transform.split()
        for part in parts:
            if part.startswith('translate'):
                translate_str = part[10:-1]  # should be such format: 'x,y'
                x, y = map(float, translate_str.split(','))
                translate = complex(x, y)
            if part.startswith('scale'):
                scale_str = part[6:-1]  # should be such format: 'x,y'
                x, y = map(float, scale_str.split(','))
                scale = complex(x, y)

    # parse paths
    paths = root.findall('.//{http://www.w3.org/2000/svg}path')
    curves = []
    for path in paths:
        d = path.get('d')
        svg_path = svg.path.parse_path(d)
        for attr in svg_path:
            if isinstance(attr, svg.path.Move):
                pass
            elif isinstance(attr, svg.path.Line):
                curves.append(curve.Line(attr.start, attr.end))
            elif isinstance(attr, svg.path.CubicBezier):
                curves.append(curve.CubicBezier(attr.start, attr.control1, attr.control2, attr.end))
            elif isinstance(attr, svg.path.Close):
                curves[-1].close()
            else:
                print(f'Unknown attribute: {attr}')

    if scale is not None:
        for cv in curves:
            cv.scale(scale)
    if translate is not None:
        for cv in curves:
            cv.translate(translate)
    for cv in curves:
        print(cv.start, cv.end)

    return curves
