from ti_hub import *
from ti_plotlib import text_at
from ti_system import *
from Utils import *

def main():
  
  #Constants
  CLOCKWISE_ROTATION_THRESHOLD = 175
  ANTI_CLOCKWISE_ROTATION_THRESHOLD = -175
  
  # Objects
  Display_Drehrichtung = DisplayController(1, "Drehrichtung: ", "left")
  Display_Spannung = DisplayController(2, "Spannungswert: ", "left")
  Display_Drehrichtung.initialize()
  Display_Spannung.initialize()
  
  spannung_port1 = analog_in("BB 6")
  spannung_port2 = analog_in("BB 7")
  # BB Port 1-4
  motor_port = bb_port(15)
  # Reset Motor Port
  motor_port.write_port(0)
  # declare and initalize variables
  pos = 0; step = 0
  #-- Motorsteuerung --
  key = get_key()
  spannungsmessung1 = []
  spannungsmessung2 = []
  while key != "esc":
    key = get_key()
    # take 3 voltage measurements
    for i in range(3):
      spannungsmessung1.append(spannung_port1.measurement())
      spannungsmessung2.append(spannung_port2.measurement())
      sleep_ms(1)
    # average all 3 measurements
    spannung_1 = Utility.average(spannungsmessung1[0], spannungsmessung1[1], spannungsmessung1[2])
    spannung_2 = Utility.average(spannungsmessung2[0], spannungsmessung2[1], spannungsmessung2[2])
    # clear both arrays
    spannungsmessung1.clear()
    spannungsmessung2.clear()
    durchschnitt_spannung=(spannung_1 + spannung_2) / 2
    # round on whole numbers
    durchschnitt_spannung=str("%1.0f" % durchschnitt_spannung)
    # output voltage measurement on screen
    Display_Spannung.update(durchschnitt_spannung)
    # decide which direction to rotate
    if spannung_1 - spannung_2 > CLOCKWISE_ROTATION_THRESHOLD:
      # output clockwise to screen
      Display_Drehrichtung.update("Im Uhrzeigersinn")
      # set motor rotation
      step = -1
    elif spannung_1 - spannung_2 < ANTI_CLOCKWISE_ROTATION_THRESHOLD:
      # output anti-clockwise to screen
      Display_Drehrichtung.update("Gegen Uhrzeigersinn")
      # set motor rotation
      step = 1
    else:
      # output none to screen
      Display_Drehrichtung.update("Keine")
      # set motor rotation to none
      step = 0
    # get position of motor
    pos = rotation(motor_port, pos, step)
  # reset Motor Port when user ends the program
  motor_port.write_port(0)

main()
