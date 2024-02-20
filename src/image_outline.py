import os
import xml.etree.ElementTree as ET
import svg.path
import curve


def get_image_outlines(filename):
    filepath = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images', filename)
    tree = ET.parse(filepath)
    root = tree.getroot()

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
            else:
                print(f'Unknown attribute: {attr}')

    return curves
