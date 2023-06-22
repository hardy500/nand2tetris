class SymbolTable:
  def __init__(self):
    # Each variable is bound to a running mem address, starting at 16
    self.var_counter = 16
    self.label_counter = 0

    self.table = {
        # Predefined
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        # Registers
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        # IO Memory-Map
        "SCREEN": 16384,
        "KBD": 24576,
    }

  def inc_label_counter(self):
    self.label_counter += 1

  def add_label(self, label: str):
    if label in self.table:
      raise RuntimeError("Label already exist")
    else:
      self.table[label] = self.label_counter

  def add_var(self, var: str):
    if var not in self.table:
      self.table[var] = self.var_counter
      self.var_counter += 1

  def lookup(self, var: str):
    self.add_var(var)
    return self.table.get(var)