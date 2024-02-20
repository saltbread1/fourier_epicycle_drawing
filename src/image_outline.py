from os import path
import xml.etree.ElementTree as ET
import svg.path

IMG_NAME = 'sample.svg'
img_path = path.join(path.dirname(__file__), '..', 'resources', 'images', IMG_NAME)
print(img_path)

tree = ET.parse(img_path)
root = tree.getroot()

print(ET.tostring(root))

