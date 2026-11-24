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
buzzer = PWM(Pin(21))

FORWARD_CODE  = 0x45  
BACKWARD_CODE = 0x47
LEFT_CODE = 0x8
RIGHT_CODE = 0x5a

SPEED_1 = 0x44
SPEED_2 = 0x43
SPEED_3 = 0x7
SPEED_4 = 0x9

LEFT_45_CODE  = 0x16
LEFT_90_CODE  = 0xc
RIGHT_45_CODE = 0xd
RIGHT_90_CODE = 0x5e

TUNE_CODE = 0x46

TUNE_NOTES = [
    (659, 120), (0, 30), (659, 120), (0, 120), (659, 120), (0, 120),
    (523, 120), (0, 30), (659, 120), (0, 120), (784, 200), (0, 220),
    (392, 200), (0, 220),
    (523, 180), (0, 120), (392, 180), (0, 120), (330, 180), (0, 120),
    (440, 140), (0, 40), (494, 140), (0, 40), (466, 100), (440, 140), (0, 40),
    (392, 130), (659, 130), (784, 130), (880, 160), (0, 40),
    (698, 120), (784, 120), (0, 40), (659, 140), (0, 40),
    (523, 110), (587, 110), (494, 160), (0, 250)
]

time_45_deg   = 180
time_90_deg   = 350
current_speed = 65535
turn_speed    = 46000

tune_playing = False
note_index = 0
note_start_time  = time.ticks_ms()
last_signal_time = time.ticks_ms()
last_beep_time   = time.ticks_ms()
moving = False
reversing = False
beep_on = False

def beep(freq, ms):
    buzzer.freq(freq)
    buzzer.duty_u16(30000)
    time.sleep_ms(ms)
    buzzer.duty_u16(0)

def startup_chime():
    beep(659, 100)  # E5
    time.sleep_ms(30)
    beep(659, 100)  # E5
    time.sleep_ms(110)
    beep(659, 100)  # E5
    time.sleep_ms(110)
    beep(523, 100)  # C5
    time.sleep_ms(30)
    beep(659, 100)  # E5
    time.sleep_ms(110)
    beep(784, 150)  # G5
    time.sleep_ms(220)
    beep(392, 180)  # G4
    
def apply_speed():
    ena.duty_u16(current_speed)
    enb.duty_u16(current_speed)
  
def precise_turn(direction, duration_ms):
    global moving, reversing
    reversing = False
    moving = False
    ena.duty_u16(turn_speed)
    enb.duty_u16(turn_speed)
    
    if direction == "RIGHT":
        in1.value(0)
        in2.value(1)
        in3.value(1)
        in4.value(0)

    if direction == "LEFT":
        in1.value(1)
        in2.value(0)
        in3.value(0)
        in4.value(1)
        
    time.sleep_ms(duration_ms)
    stop_car()
    
def move_forward():
    global moving, reversing
    moving = True
    reversing = False
    apply_speed()
    in1.value(1)
    in2.value(0)
    in3.value(1)
    in4.value(0)

def move_backward():
    global moving, reversing  
    moving = True
    reversing = True
    apply_speed()
    in1.value(0)
    in2.value(1)
    in3.value(0)
    in4.value(1)

def stop_car():
    global moving, reversing, beep_on
    moving = False
    reversing = False
    beep_on = False
    if not tune_playing:
        buzzer.duty_u16(0)
    ena.duty_u16(0)
    enb.duty_u16(0)
    in1.value(0)
    in2.value(0)
    in3.value(0)
    in4.value(0)

def turn_right():
    global moving, reversing
    reversing = False
    moving = True
    ena.duty_u16(turn_speed)
    enb.duty_u16(turn_speed)
    in1.value(0)
    in2.value(1)
    in3.value(1)
    in4.value(0)

def turn_left():
    global moving, reversing 
    moving = True
    reversing = False
    ena.duty_u16(turn_speed)
    enb.duty_u16(turn_speed)
    in1.value(1)
    in2.value(0)
    in3.value(0)
    in4.value(1)

def ir_callback(data, addr, ctrl):
    global current_speed, last_signal_time, tune_playing, note_index, note_start_time
    last_signal_time = time.ticks_ms()
    
    if data < 0:
       return
    
    if data == FORWARD_CODE:
        move_forward()
    elif data == BACKWARD_CODE:
        move_backward()
    elif data == RIGHT_CODE:
        turn_right()
    elif data == LEFT_CODE:
        turn_left()
    
    elif data == LEFT_45_CODE:
        precise_turn("LEFT", time_45_deg)
    elif data == LEFT_90_CODE:
        precise_turn("LEFT", time_90_deg)
    elif data == RIGHT_45_CODE:
        precise_turn("RIGHT", time_45_deg)
    elif data == RIGHT_90_CODE:
        precise_turn("RIGHT", time_90_deg)
        
    elif data == SPEED_1:
        current_speed = 25000
        if moving: apply_speed()
        if not tune_playing: beep(400, 50)
    elif data == SPEED_2:
        current_speed = 38000
        if moving: apply_speed()
        if not tune_playing: beep(550, 50)
    elif data == SPEED_3:
        current_speed = 52000
        if moving: apply_speed()
        if not tune_playing: beep(700, 50)
    elif data == SPEED_4:
        current_speed = 65535
        if moving: apply_speed()
        if not tune_playing: beep(900, 50)
    
    elif data == TUNE_CODE:
        tune_playing = not tune_playing
        if tune_playing:
            note_index = 0
            note_start_time = time.ticks_ms()
            freq, _ = TUNE_NOTES[0]
            if freq > 0:
                buzzer.freq(freq)
                buzzer.duty_u16(12000)
            else:
                buzzer.duty_u16(0)
        else:
            buzzer.duty_u16(0)

ir_decoder = NEC_8(ir_pin, ir_callback)
startup_chime()

while True:
    now = time.ticks_ms()
    
    if moving and (time.ticks_diff(now, last_signal_time) > 600):
        stop_car()
    
    if reversing:
        if not tune_playing:
            if time.ticks_diff(now, last_beep_time) > 250:
                last_beep_time = now
                beep_on = not beep_on
                if beep_on:
                    buzzer.freq(900)
                    buzzer.duty_u16(2000)
                else:
                    buzzer.duty_u16(0)
    else:
        if beep_on and not tune_playing:
            buzzer.duty_u16(0)
            beep_on = False
                
    if tune_playing:
        freq, duration = TUNE_NOTES[note_index]
        if time.ticks_diff(now, note_start_time) >= duration:
            note_index = (note_index + 1) % len(TUNE_NOTES)
            note_start_time = now
            next_freq, _ = TUNE_NOTES[note_index]
            if next_freq > 0:
                buzzer.freq(next_freq)
                buzzer.duty_u16(12000)
            else:
                buzzer.duty_u16(0)
        
    time.sleep_ms(10)


