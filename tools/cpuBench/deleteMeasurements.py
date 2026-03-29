#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import datetime

# Delete measurement nodes for a specific architecture from an XML file.
def main():
   parser = argparse.ArgumentParser(description='Merge XML files')
   parser.add_argument('inp')
   parser.add_argument('arch')
   parser.add_argument('outp')
   args = parser.parse_args()

   root = ET.parse(args.inp).getroot()
   root.attrib['date'] = str(datetime.date.today())

   for instrNode in root.iter('instruction'):
      for archNode in instrNode.findall(f'architecture[@name="{args.arch}"]'):
         for measurementNode in archNode.iter('measurement'):
            archNode.remove(measurementNode)

   with open(args.outp, "w") as f:
      rough_string = ET.tostring(root, 'utf-8')
      reparsed = minidom.parseString(rough_string)
      f.write('\n'.join([line for line in reparsed.toprettyxml(indent=' '*2).split('\n') if line.strip()]))


if __name__ == "__main__":
    main()
