import os
import xml.etree.ElementTree as ET
import svg.path

IMG_NAME = 'sample.svg'
img_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images', IMG_NAME)

tree = ET.parse(img_path)
root = tree.getroot()

paths = root.findall('.//{http://www.w3.org/2000/svg}path')

for path in paths:
    d = path.get('d')
    svg_path = svg.path.parse_path(d)
    for attr in svg_path:
        if isinstance(attr, svg.path.Move):
            print(attr.start)
        elif isinstance(attr, svg.path.Line):
            print(attr)
        elif isinstance(attr, svg.path.CubicBezier):
            print(attr)
        else:
            print(attr)


