import time
from machine import Pin
from lib.ir_rx.nec import NEC_8

in1 = Pin(15, Pin.OUT)
in2 = Pin(16, Pin.OUT)
ir_pin = Pin(17, Pin.IN)

FORWARD_CODE  = 0x45  
BACKWARD_CODE = 0x46  
STOP_CODE     = 0x47  

def move_forward():
    in1.value(1)
    in2.value(0)
    print("Forward")

def move_backward():
    in1.value(0)
    in2.value(1)
    print("Backward")

def stop_car():
    in1.value(0)
    in2.value(0)
    print("Stopped")

def ir_callback(data, addr, ctrl):
    if data < 0:
        return
    
    if data == FORWARD_CODE:
        move_forward()
    elif data == BACKWARD_CODE:
        move_backward()
    elif data == STOP_CODE:
        stop_car()

ir_decoder = NEC_8(ir_pin, ir_callback)

while True:
    time.sleep(1)
