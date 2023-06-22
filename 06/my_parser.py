from symboltable import SymbolTable as SymTable
class MyParser:
  prefix_a = "0"
  prefix_c = "111"

  def __init__(self):
    self.symtable = SymTable()
    # Init instructions
    self.cmp = {
      "0" : "0101010",
      "1" : "0111111",
      "-1": "0111010",
      "D" : "0001100",
      "A" : "0110000",
      "!D": "0001101",
      "!A": "0110001",
      "-D": "0001111",
      "-A": "0110011",
      "D+1": "0011111",
      "1+D": "0011111",
      "A+1": "0110111",
      "1+A": "0110111",
      "D-1": "0001110",
      "A-1": "0110010",
      "D+A": "0000010",
      "A+D": "0000010",
      "D-A": "0010011",
      "A-D": "0000111",
      "D&A": "0000000",
      "A&D": "0000000",
      "D|A": "0010101",
      "A|D": "0010101",
      "M":  "1110000",
      "!M": "1110001",
      "-M": "1110011",
      "M+1": "1110111",
      "1+M": "1110111",
      "M-1": "1110010",
      "D+M": "1000010",
      "M+D": "1000010",
      "D-M": "1010011",
      "M-D": "1000111",
      "D&M": "1000000",
      "M&D": "1000000",
      "D|M": "1010101",
      "M|D": "1010101",
    }

    self.dest = {
      "null": "000",
      "M"   : "001",
      "D"   : "010",
      "MD"  : "011",
      "DM"  : "011",
      "A"   : "100",
      "AM"  : "101",
      "MA"  : "101",
      "AD"  : "110",
      "DA"  : "110",
      "AMD" : "111",
      "ADM" : "111",
      "MAD" : "111",
      "MDA" : "111",
      "DAM" : "111",
      "DMA" : "111",

    }


    self.jmp = {
      "null":"000",
      "JGT": "001",
      "JEQ": "010",
      "JGE": "011",
      "JLT": "100",
      "JNE": "101",
      "JLE": "110",
      "JMP": "111",
    }

  def cmp_lookup(self, cmp_inst: str) -> str:
    if cmp_inst not in self.cmp:
      return self.cmp["0"]
    else:
      return self.cmp[cmp_inst]

  def dest_lookup(self, dest_inst: str) -> str:
    if dest_inst not in self.dest:
      return self.dest["null"]
    else:
      return self.dest[dest_inst]

  def jmp_lookup(self, jmp_inst: str) -> str:
    if jmp_inst not in self.jmp:
      return self.jmp["null"]
    else:
      return self.jmp[jmp_inst]

  def parse_inst(self, inst:str) -> str:
    if '@' in inst:
      return self.parse_a_inst(inst[1:]) # start at pos '@' + 1
    else:
      return self.parse_c_inst(inst)

  def parse_a_inst(self, inst: str) -> str:
    if inst.isdigit():
      return self.prefix_a + format(int(inst), '015b')
    else:
      if any(char.isdigit() for char in inst) and any(char.isalpha() for char in inst):
        raise RuntimeError("Invalid A-instruction")
      addr = self.symtable.lookup(inst)
      return self.prefix_a + format(int(addr), "015b")

  def parse_c_inst(self, inst: str) -> str:
    idxe = inst.find('=')
    idxsc = inst.find(';')

    dest_inst = "null" if idxe == -1 else inst[:idxe]
    cmp_inst = inst[idxe + 1:idxsc] if idxsc != -1 else inst[idxe + 1:]
    jmp_inst = "null" if idxsc == -1 else inst[idxsc + 1:]

    return self.prefix_c + self.cmp_lookup(cmp_inst) + self.dest_lookup(dest_inst) + self.jmp_lookup(jmp_inst)