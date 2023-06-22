#!/usr/bin/env python3
import sys
from my_parser import MyParser
from symboltable import SymbolTable

def main():
  if len(sys.argv) > 2:
    print(sys.argv)
    print("Usage: assembly.py file.asm")
    sys.exit()
  else:
    arg = sys.argv[1]

  filename = arg.split("/")[0]
  symtable = SymbolTable()
  parser = MyParser()
  queue1, queue2 = [], []

  with open(arg, "r") as f:
    for line in f:
      idx = line.find("//")
      line = line[:idx]
      if not line.strip():
        continue
      line = line.replace(" ", "")
      queue1.append(line)

    while queue1:
      line = queue1.pop(0)
      if "(" in line and ")" in line:
        idx_L = line.rfind("(")
        idx_R = line.find(")")
        line = line[idx_L + 1: idx_R]
        symtable.add_label(line)
        continue
      else:
        symtable.inc_label_counter()
      queue2.append(line)

    while queue2:
      line = queue2.pop(0)
      mac_code = parser.parse_inst(line)
      print(line, "\t->\t\t", mac_code)

      with open(filename+".hack", "a") as f:
        f.write(mac_code + "\n")

if __name__ == "__main__":
  main()
