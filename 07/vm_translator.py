import os

COMMENT = "//"

class Parser:
  def __init__(self, vm_file: str):
    self.vm_file = vm_file
    self.vm = open(vm_file, "r")
    self.commands = {
            'add': 'ARITHMETIC',
            'sub': 'ARITHMETIC',
            'neg': 'ARITHMETIC',
             'eq': 'ARITHMETIC',
             'gt': 'ARITHMETIC',
             'lt': 'ARITHMETIC',
            'and': 'ARITHMETIC',
             'or': 'ARITHMETIC',
            'not': 'ARITHMETIC',
           'push': 'PUSH',
            'pop': 'POP',
          'label': 'LABEL',
           'goto': 'GOTO',
        'if-goto': 'IF',
       'function': 'FUNCTION',
         'return': 'RETURN',
           'call': 'CALL'
    }

    self.current_instruction = None
    self.initialize_file()

  def initialize_file(self):
    self.vm.seek(0)
    line = self.vm.readline().strip()
    while not (line and line[:2] != COMMENT): # is instruction?
      line = self.vm.readline().strip()
    self.load_next_instruction(line)

  def load_next_instruction(self, line=None):
    line = line if line else self.vm.readline().strip()
    self.next_instruction = line.split(COMMENT)[0].strip().split()

  def advance(self):
    self.current_instruction = self.next_instruction
    self.load_next_instruction()

  def argn(self, n: int):
    if len(self.current_instruction) >= n+1:
      return self.current_instruction[n]
    return None

  @property
  def has_more_commands(self):
    return bool(self.next_instruction)

  @property
  def command_type(self):
    return self.commands.get(self.current_instruction[0].lower())

  @property
  def arg1(self):
    if self.command_type == "ARITHMETIC":
      return self.argn(0)
    return self.argn(1)

  @property
  def arg2(self):
    return self.argn(2)

class AsmWriter:
  """
  Contract between methods:
  1. Content of the A and D regs are not guaranteed,
     so methods must set them to the values they need
  2. Methods must always leave @SP pointing to the correct location
  """

  def __init__(self, asm_filename: str):
    self.asm = open(asm_filename, "w")
    self.current_file = None
    self.bool_count = 0     # Number of bool comparison so far
    self.addr = {
        "local": "LCL",
        "argument": "ARGS",
        "this": "THIS",
        "that": "THAT",
        "pointer": 3,
        "temp": 5,
        "static": 16
    }

  def write(self, command: str):
    self.asm.write(command + "\n")

  def set_filename(self, vm_filename: str):
    self.current_file = vm_filename.replace(".vm", "").split("/")[-1]

  def write_arithmetic(self, op: str):
    if op not in ["neg", "not"]:
      self.popD()
    self.decrSP()
    self.setA()

    if op == "add":
      self.write("M=M+D")
    elif op == "sub":
      self.write("M=M-D")
    elif op == "and":
      self.write("M=M&D")
    elif op == "or":
      self.write("M=M|D")
    elif op == "neg":
      self.write("M=-M")
    elif op == "not":
      self.write("M=!M")
    elif op in ["eq", "gt", "lt"]:
      self.write("D=M-D")
      self.write(f"@BOOL{self.bool_count}")

      if op == "eq":
        self.write("D;JEQ")
      elif op == "gt":
        self.write("JGT")
      elif op == "lt":
        self.write("D;JLT")

      self.setA()
      self.write(f"@ENDBOOL{self.bool_count}")
      self.write("0;JMP")

      self.write(f"(BOOL{self.bool_count})")
      self.write("0;JMP")

      self.write(f"(BOOL{self.bool_count})")
      self.setA()
      self.write("M=-1")

      self.write(f"(ENDBOOL{self.bool_count})")
      self.bool_count += 1
    else:
      raise ValueError(op)
    self.incrSP()

  def decrSP(self):
    self.write("@SP")
    self.write("M=M-1")

  def incrSP(self):
    self.write("@SP")
    self.write("M=M+1")

  def setA(self):
    self.write("@SP")
    self.write("A=M")

  def write_push_pop(self, command: str, segment: str, index: str):
    self.resolve_addr(segment, index)
    if command == "PUSH":
      if segment == "constant":
        self.write("D=A")
      else:
        self.write("D=M")
      self.pushD()
    elif command == "POP":
      self.write("D=A")
      self.write("@R13")
      self.write("M=D")
      self.popD()
      self.write("@R13")
      self.write("A=M")
      self.write("M=D")
    else:
      raise ValueError(f"{command} is an invalid argument")

  def close(self):
    self.asm.close()

  def resolve_addr(self, segment: str, index: str):
    addr = self.addr.get(segment)
    if segment == "constant":
      self.write("@" + index)
    elif segment == "static":
      self.write("@" + self.current_file + "." + index)
    elif segment in ["pointer", "temp"]:
      self.write("@R" + addr + index)
    elif segment in ["local", "argument", "this", "that"]:
      self.write("@" + addr)
      self.write("D+M")
      self.write("@" + index)
      self.write("A=D+A")
    else:
      raise ValueError(f"{segment} is an invalid argument")

  def pushD(self):
    self.write("@SP")
    self.write("A=M")
    self.write("M=D")
    self.write("@SP")
    self.write("M=M+1")

  def popD(self):
    self.write("@SP")
    self.write("M=M-1")
    self.write("A=M")
    self.write("D=M")

class Main:
  def __init__(self, file_path: str):
    self.parse_file(file_path)
    self.asm_writer = AsmWriter(self.asm_file)
    for vm_file in self.vm_files:
      self.translate(vm_file)
    self.asm_writer.close()

  def parse_file(self, file_path: str):
    if ".vm" in file_path:
      self.asm_file = file_path.replace(".vm", ".asm")
      self.vm_files = [file_path]

  def translate(self, vm_file: str):
    parser = Parser(vm_file)
    self.asm_writer.set_filename(vm_file)
    while parser.has_more_commands:
      parser.advance()
      self.asm_writer.write("// " + " ".join(parser.current_instruction))
      if parser.command_type == "PUSH":
        self.asm_writer.write_push_pop("PUSH", parser.arg1, parser.arg2)
      elif parser.command_type == "POP":
        self.asm_writer.write_push_pop("POP", parser.arg1, parser.arg2)
      elif parser.command_type == "ARITHMETIC":
        self.asm_writer.write_arithmetic(parser.arg1)


if __name__ == "__main__":
  import sys
  file_path = sys.argv[1]
  Main(file_path)