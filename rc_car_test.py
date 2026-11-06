import time
from machine import Pin, PWM
from lib.ir_rx.nec import NEC_8
                                
in1 = Pin(15, Pin.OUT)
in2 = Pin(16, Pin.OUT)
in3 = Pin(18, Pin.OUT)
in4 = Pin(19, Pin.OUT)

ena = PWM(Pin(14))
enb = PWM(Pin(13))

ena.freq(1000)
enb.freq(1000)

ir_pin = Pin(17, Pin.IN)

FORWARD_CODE  = 0x45  
BACKWARD_CODE = 0x46  
STOP_CODE = 0x47
LEFT_CODE = 0x8
RIGHT_CODE = 0x5a
SPEED_1 = 0x44
SPEED_2 = 0x43
SPEED_3 = 0x7
SPEED_4 = 0x9

current_speed = 65535

def apply_speed():
    ena.duty_u16(current_speed)
    enb.duty_u16(current_speed)

def move_forward():
    apply_speed()
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)
    print(f"Forward at {current_speed}")

def move_backward():
    apply_speed()
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)
    print(f"Backward at {current_speed}")

def stop_car():
    ena.duty_u16(0)
    enb.duty_u16(0)
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)
    print("Stopped")

def turn_right():
    apply_speed()
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)
    print("Turned right")

def turn_left():
    apply_speed()
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)
    print("Turned left")

def ir_callback(data, addr, ctrl):
    global current_speed
    if data < 0:
        return
    
    if data == FORWARD_CODE:
        move_forward()
    elif data == BACKWARD_CODE:
        move_backward()
    elif data == STOP_CODE:
        stop_car()
    elif data == RIGHT_CODE:
        turn_right()
    elif data == LEFT_CODE:
        turn_left()
        
    elif data == SPEED_1:
        current_speed = 25000
        apply_speed()
        print("Speed Mode: 1")
    elif data == SPEED_2:
        current_speed = 38000
        apply_speed()
        print("Speed Mode: 2")
    elif data == SPEED_3:
        current_speed = 52000
        apply_speed()
        print("Speed Mode: 3")
    elif data == SPEED_4:
        current_speed = 65535
        apply_speed()
        print("Speed Mode: 4")

ir_decoder = NEC_8(ir_pin, ir_callback)

while True:
    time.sleep(1)
