import random
import re
import time
from gpiozero import LED, Servo, PWMLED

# Standard Traffic Light LEDs
red_led = LED(3)
yellow_led = LED(4)
green_led = LED(7)

# RGB LEDs using PWM
rgb1_red = PWMLED(14)
rgb1_green = PWMLED(15)
rgb1_blue = PWMLED(18)

rgb2_red = PWMLED(23)
rgb2_green = PWMLED(24)
rgb2_blue = PWMLED(25)

servo = Servo(17)

# 7-Segment Display GPIO Pins
segment_a = LED(5)
segment_b = LED(6)
segment_c = LED(13)
segment_d = LED(19)
segment_e = LED(26)
segment_f = LED(21)
segment_g = LED(20)

# Define 7-segment digit mapping
digit_map = {
    0: [1, 1, 1, 1, 1, 1, 0], 1: [0, 1, 1, 0, 0, 0, 0], 2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1], 4: [0, 1, 1, 0, 0, 1, 1], 5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1], 7: [1, 1, 1, 0, 0, 0, 0], 8: [1, 1, 1, 1, 1, 1, 1], 9: [1, 1, 1, 1, 0, 1, 1]
}

def display_digit(digit):
    segments = digit_map[digit]
    segment_a.value, segment_b.value, segment_c.value, segment_d.value, \
    segment_e.value, segment_f.value, segment_g.value = segments

def play_game():
    print("Guess a number from -100.00 to 100.00 in +000.00 or -000.00 format for nonzero numbers & 000.00 format for zero.")
    print("You have 7 attempts & 6 hints!")
    
    R_Number = round(random.uniform(-100.00, 100.00), 2)
    attempts = 0
    Guess = None
    hints_used = set()

    while Guess != R_Number and attempts < 7:
        try:
            U_Guess = input("")
            if not re.match(r'^(000\.00|[+-](?!000\.00)\d{3}\.\d{2})$', U_Guess):
                print("Invalid format! Use -000.00, 000.00, or +000.00 format.")
                continue
            
            U_Guess = float(U_Guess)
            if U_Guess < -100.00 or U_Guess > 100.00:
                print("Out of range! Enter a number from -100.00 to 100.00.")
                continue
        except ValueError:
            print("Invalid input! Examples: 7=+007.00, 0=000.00, -100.01=-100.01")
            continue
        
        Guess = round(U_Guess, 2)
        attempts += 1 

        if Guess == R_Number:  
            print(f"Good guess! 🎉 {Guess} is correct! You won in {attempts} attempts.")
            return True
        elif attempts == 7:
            print(f"Game over! The correct number was {R_Number:.2f}.")
            return False
        elif Guess < R_Number:
            print("Too low! 🔼 Try again.")
        else:
            print("Too high! 🔽 Try again.")
    
    return False

def move_servo(direction, duration):
    step = 0.05 if direction == "forward" else -0.05  
    start = -1 if direction == "forward" else 1       
    end = 1 if direction == "forward" else -1         
    threshold = 0.7 * end  
    move_time = duration / 2  
    steps = int(move_time / 0.05)  
    step_delay = move_time / steps  

    display_digit(8)
    red_led.on()
    time.sleep(1)
    
    red_led.off()
    green_led.on()
    time.sleep(0.5)

    for position in frange(start, end, step):
        servo.value = position
        time.sleep(step_delay)
        if (direction == "forward" and position >= threshold) or (direction == "backward" and position <= threshold):
            green_led.off()
            yellow_led.on()

    servo.value = end
    yellow_led.off()
    red_led.on()
    time.sleep(1)

def frange(start, stop, step):
    while (step > 0 and start <= stop) or (step < 0 and start >= stop):
        yield round(start, 2)
        start += step

def start_led_servo_sequence():
    print("Starting LED, Servo, and 7-Segment program!")    
    total_duration = 72
    for sec in range(total_duration):
        display_digit(sec % 10)
        time.sleep(1)
    move_servo("forward", total_duration)
    time.sleep(2)
    move_servo("backward", total_duration)
    time.sleep(2)

def main():
    if play_game():
        start_led_servo_sequence()
    else:
        print("Game lost. No movement.")

main()