from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError

board_num = 1
channel = 0
ai_range = ULRange.BIP5VOLTS
from ctypes import *

_cbw = WinDLL("cbw64.dll")

data_value = c_ushort()
err_val = _cbw.cbAIn(0, 6, 1, byref(data_value))
try:
    # Get a value from the device
    value = ul.a_in(board_num, channel, ai_range)
    # Convert the raw value to engineering units
    eng_units_value = ul.to_eng_units(board_num, ai_range, value)

    # Display the raw value
    print("Raw Value: " + str(value))
    # Display the engineering value
    print("Engineering Value: " + '{:.3f}'.format(eng_units_value))
except ULError as e:
    # Display the error
    print("A UL error occurred. Code: " + str(e.errorcode)
          + " Message: " + e.message)