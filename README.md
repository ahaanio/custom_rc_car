This is a custom rc car build that can be controlled with an ir remote. I took apart my rc car and harvested the battery box and motors, and turned it into this.
So far, I've only achieved forward, backward, and stop, but it works really nice. I also took apart my laser tag system to extract the ir reciver I needed. The
only thing I had to buy was a L298N driver. The total parts I used for this prototype was: An rc chassis with a gearbox and a single dc motor, a RP2040 raspberry
pi pico, a half sized breadboard, male to female jumper wires, an L298N Motor Driver, a Duracell 9v Alkaline battery, an ir reciver from my laser tag guns, and
a random ir remote I found in my garage with NEC protocol. Note: If your remote has a different protocol then NEC, you can go on github and find peterhinch, who
has the driver files for ir remotes. For the assembly, start by putting your raspberry pi pico with header pins onto the breadboard, on top of the center divider.
Connect any GND pin from the pico to the negative rail on the breadboard. This rail will be your common ground. Next, take your ir reciver and use your male to 
female wires and slide it into each of the three pins on the reciver. The pinout may vary, but for me, when the bulb is facing you, the left most pin is the DATA 
pin, which connects to GP17 on the pico. The middle pin connects to the negative rail, and the right most pin goes to 3v3 OUT on the pico. Note: DO NOT connect 
the right most pin to VBUS. Putting 5v onto the reciver means it will return 5v to the GPIO pin, which runs on 3V. This risks breaking the pin, so just keep that 
in mind. Next, take your dc motor wires and your L298N driver and put the two wires of the dc motor into the out1 and out2 screw terminals on the driver. Screw them
tight. Then, take your battery of choice(keep it between 7.5V and 12V so you can use the jumper) and put its postive wire in the 12V screw terminal, and the negative
wire to the negative rail of your breadboard(remember, common ground is crucial). Take a jumper wire from your negative rail, and put it in the GND screw terminal 
of the driver. Screw those tight. Now, take two male to female jumper wires. Slide one into in1 and put the other end into GP15. Slide another wire into in2, and 
put the other end to GP16. Now the main circuit is done. When you turn the battery on, make sure that the onboard light on the L298N driver turns on. If it doesn't,
something with your wiring is wrong. While the battery is off, run the button mapping script for your ir remote in thonny IDE. Find the hex codes for the buttons
of your choice, and plug them in for the command lines in the main code. Then, turn on your battery, plug in your pico, run the script, and watch the motors run! 
