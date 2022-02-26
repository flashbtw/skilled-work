from ti_hub import *
from ti_plotlib import text_at
from ti_system import *

class DisplayController:
  def __init__(self, row, text, side):
    self.row = row
    self.text = text
    self.side = side
  def initialize(self):
    text_at(self.row, self.text, self.side)
  def update(self, valueOfMeasurement):
    text_at(self.row, self.text + valueOfMeasurement, self.side)

class Utility:
  def correctly(key):
    i = 0
    str = "0123456789.-"
    while i < len(str):
      if str[i] == key:
        return True
      i += 1
    return False 

  def input(row, text):
    use_buffer()
    val = ""
    str = text
    text_at(row, str + "_", "left")
    paint_buffer()
    key = ""
    while key != "enter":
      key = get_key(1)
      if correctly(key):
        val += key
        str += key
        text_at(row, str + "_", "left")
      if key == "del" and len(val) > 0:
        val = val[:len(val) - 1]
        str = str[:len(str) - 1]
        text_at(row, str + "_", "left")
      paint_buffer()
    text_at(row, str, "left")
    return float(val)

  def average(value1, value2, value3):
    return (value1+value2+value3) / 3

def rotation(port, p, s):
  wert = 0
  if p == 0:
    wert = 9
  elif p == 1 or p == -3:
    wert = 5
  elif p == 2 or p == -2:
    wert = 6
  elif p == 3 or p == -1:
    wert = 10
  port.write_port(wert)
  return (p + s) % 4
