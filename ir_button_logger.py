import time
from machine import Pin
from lib.ir_rx.nec import NEC_8

ir_pin = Pin(17, Pin.IN)

def ir_callback(data, addr, ctrl):
    if data >= 0:
        print(hex(data))

ir_decoder = NEC_8(ir_pin, ir_callback)

while True:
    time.sleep(1)
