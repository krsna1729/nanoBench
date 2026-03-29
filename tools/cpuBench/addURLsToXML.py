#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import re
import urllib.request
from xml.dom import minidom
from utils import *

def main():
   parser = argparse.ArgumentParser(description='')
   parser.add_argument("input", help="Input XML file")
   parser.add_argument("output", help="Output XML file")
   args = parser.parse_args()

   html = urllib.request.urlopen('https://www.felixcloutier.com/x86/').read().decode('utf-8').replace(u'\u2013', '-').replace(u'\u2217', '*')
   lines = re.findall("href='/x86/(.*?)'>(.*?)</a>.*?</td><td>(.*?)</td>", html) # Example: ('/x86/adc', 'ADC', 'Add with Carry'),
   lineDict = {(line[0],line[1]):line for line in lines}

   root = ET.parse(args.input).getroot()
   for instrNode in root.iter('instruction'):
      iclass = instrNode.attrib['iclass']
      iform = instrNode.attrib['iform']
      extension = instrNode.attrib['extension']

      if extension in ['MONITORX', 'SSE4a', 'SVM', 'TBM', 'TSX_LDTRK', 'XOP', 'RAO_INT', 'APXEVEX', 'APXLEGACY', 'CMPCCXADD', '3DNOW']:
         continue

      matchingLines = []
      if iclass == 'INT':
         matchingLines = [lineDict[('intn:into:int3:int1', 'INT n')]]
      if iclass == 'MOV':
         matchingLines = [lineDict[('mov', 'MOV')]]
      elif iclass == 'MOV_CR':
         matchingLines = [lineDict[('mov-1', 'MOV')]]
      elif iclass == 'MOV_DR':
         matchingLines = [lineDict[('mov-2', 'MOV')]]
      elif iclass == 'VMRESUME':
         matchingLines = [lineDict[('vmlaunch:vmresume', 'VMRESUME')]]
      elif iclass == 'SCASQ':
         matchingLines = [lineDict[('scas:scasb:scasw:scasd', 'SCAS')]]
      elif iclass == 'UD2':
         matchingLines = [lineDict[('ud', 'UD')]]
      elif iclass in ['CMPSD', 'VCMPSD', 'CMPSD_XMM']:
         if extension == 'BASE':
            matchingLines = [lineDict[('cmps:cmpsb:cmpsw:cmpsd:cmpsq', 'CMPSD')]]
         else:
            matchingLines = [lineDict[('cmpsd', 'CMPSD')]]
      elif iclass in ['IRETW', 'IRETD', 'IRETQ']:
         matchingLines = [lineDict[('iret:iretd:iretq', 'IRET')]]
      elif iclass in ['MOVQ', 'VMOVQ']:
         if 'GPR' in iform:
            matchingLines = [lineDict[('movd:movq', 'MOVQ')]]
         else:
            matchingLines = [lineDict[('movq', 'MOVQ')]]
      elif iclass in ['MOVSD', 'VMOVSD', 'MOVSD_XMM']:
         if extension == 'BASE':
            matchingLines = [lineDict[('movs:movsb:movsw:movsd:movsq', 'MOVSD')]]
         else:
            matchingLines = [lineDict[('movsd', 'MOVSD')]]
      elif iclass == 'VGATHERDPD':
         if '512' in extension:
            matchingLines = [lineDict[('vgatherdps:vgatherdpd', 'VGATHERDPD')]]
         else:
            matchingLines = [lineDict[('vgatherdpd:vgatherqpd', 'VGATHERDPD')]]
      elif iclass == 'VGATHERDPS':
         if '512' in extension:
            matchingLines = [lineDict[('vgatherdps:vgatherdpd', 'VGATHERDPS')]]
         else:
            matchingLines = [lineDict[('vgatherdps:vgatherqps', 'VGATHERDPS')]]
      elif iclass == 'VGATHERQPD':
         if '512' in extension:
            matchingLines = [lineDict[('vgatherqps:vgatherqpd', 'VGATHERQPD')]]
         else:
            matchingLines = [lineDict[('vgatherdpd:vgatherqpd', 'VGATHERQPD')]]
      elif iclass == 'VGATHERQPS':
         if '512' in extension:
            matchingLines = [lineDict[('vgatherqps:vgatherqpd', 'VGATHERQPS')]]
         else:
            matchingLines = [lineDict[('vgatherdps:vgatherqps', 'VGATHERQPS')]]
      elif iclass == 'VPGATHERDD':
         if '512' in extension:
            matchingLines = [lineDict[('vpgatherdd:vpgatherdq', 'VPGATHERDD')]]
         else:
            matchingLines = [lineDict[('vpgatherdd:vpgatherqd', 'VPGATHERDD')]]
      elif iclass == 'VPGATHERDQ':
         if '512' in extension:
            matchingLines = [lineDict[('vpgatherdd:vpgatherdq', 'VPGATHERDQ')]]
         else:
            matchingLines = [lineDict[('vpgatherdq:vpgatherqq', 'VPGATHERDQ')]]
      elif iclass == 'VPGATHERQD':
         if '512' in extension:
            matchingLines = [lineDict[('vpgatherqd:vpgatherqq', 'VPGATHERQD')]]
         else:
            matchingLines = [lineDict[('vpgatherdd:vpgatherqd', 'VPGATHERQD')]]
      elif iclass == 'VPGATHERQQ':
         if '512' in extension:
            matchingLines = [lineDict[('vpgatherqd:vpgatherqq', 'VPGATHERQQ')]]
         else:
            matchingLines = [lineDict[('vpgatherdq:vpgatherqq', 'VPGATHERQQ')]]
      elif iclass.startswith('PMOVSX') or iclass.startswith('VPMOVSX'):
         matchingLines = [lineDict[('pmovsx', 'PMOVSX')]]
      elif iclass.startswith('PMOVZX') or iclass.startswith('VPMOVZX'):
         matchingLines = [lineDict[('pmovzx', 'PMOVZX')]]
      elif iclass.startswith('REP'):
         matchingLines = [lineDict[('rep:repe:repz:repne:repnz', 'REP')]]
      elif iclass.startswith('VBROADCAST'):
         matchingLines = [lineDict[('vbroadcast', 'VBROADCAST')]]
      elif iclass.startswith('VMASKMOV'):
         matchingLines = [lineDict[('vmaskmov', 'VMASKMOV')]]
      elif iclass.startswith('VPANDN'):
         matchingLines = [lineDict[('pandn', 'PANDN')]]
      elif iclass.startswith('VPAND'):
         matchingLines = [lineDict[('pand', 'PAND')]]
      elif iclass.startswith('VPBROADCASTM'):
         matchingLines = [lineDict[('vpbroadcastm', 'VPBROADCASTM')]]
      elif iclass.startswith('VPMASKMOV'):
         matchingLines = [lineDict[('vpmaskmov', 'VPMASKMOV')]]
      elif iclass.startswith('VPOR'):
         matchingLines = [lineDict[('por', 'POR')]]
      elif iclass.startswith('VPXOR'):
         matchingLines = [lineDict[('pxor', 'PXOR')]]
      else:
         for line in lines:
            mnemonic = line[1].upper()
            if iclass in [mnemonic, 'V'+mnemonic, mnemonic+'_LOCK', mnemonic+'_FAR', mnemonic+'_NEAR', mnemonic+'_SSE4', mnemonic+'64']:
               matchingLines.append(line)
            if 'CC' in mnemonic and iclass.startswith(mnemonic.replace('CC', '')) and not iclass in ['JMP', 'JMP_FAR', 'LOOP', 'SETSSBSY']:
               matchingLines.append(line)

      if len(matchingLines) > 1:
         print('Duplicate link found for ' + iclass)
         print(matchingLines)
         exit(1)
      if len(matchingLines) == 0:
         print('No link found for ' + iclass + ' (extension: ' + extension + ')')
         continue

      instrNode.attrib['url'] = 'uops.info/html-instr/' + canonicalizeInstrString(instrNode.attrib['string']) + '.html'
      if matchingLines:
         instrNode.attrib['summary'] = str(matchingLines[0][2])
         instrNode.attrib['url-ref'] = 'felixcloutier.com/x86/' + matchingLines[0][0]

   with open(args.output, "w") as f:
      rough_string = ET.tostring(root, 'utf-8')
      reparsed = minidom.parseString(rough_string)
      f.write('\n'.join([line for line in reparsed.toprettyxml(indent=' '*2).split('\n') if line.strip()]))


if __name__ == "__main__":
    main()
