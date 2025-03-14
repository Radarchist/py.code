from gpiozero import LED, Servo, PWMLED
import time

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

# 7-Segment Display GPIO Pins (example: A-G connected to GPIO pins)
segment_a = LED(5)
segment_b = LED(6)
segment_c = LED(13)
segment_d = LED(19)
segment_e = LED(26)
segment_f = LED(21)
segment_g = LED(20)

# Define 7-segment digit mapping (0-9)
digit_map = {
    0: [1, 1, 1, 1, 1, 1, 0],
    1: [0, 1, 1, 0, 0, 0, 0],
    2: [1, 1, 0, 1, 1, 0, 1],
    3: [1, 1, 1, 1, 0, 0, 1],
    4: [0, 1, 1, 0, 0, 1, 1],
    5: [1, 0, 1, 1, 0, 1, 1],
    6: [1, 0, 1, 1, 1, 1, 1],
    7: [1, 1, 1, 0, 0, 0, 0],
    8: [1, 1, 1, 1, 1, 1, 1],
    9: [1, 1, 1, 1, 0, 1, 1]
}

# Function to display a digit on the 7-segment display
def display_digit(digit):
    segments = digit_map[digit]
    segment_a.value = segments[0]
    segment_b.value = segments[1]
    segment_c.value = segments[2]
    segment_d.value = segments[3]
    segment_e.value = segments[4]
    segment_f.value = segments[5]
    segment_g.value = segments[6]

# Define rainbow colors with distinct intensities
rainbow_colors_1 = [
    (255, 0, 0),   # Red
    (255, 127, 0), # Orange
    (255, 255, 0), # Yellow
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (75, 0, 130),  # Indigo
    (238, 130, 238) # Violet
]  # First Rainbow (Brighter)

rainbow_colors_2 = [
    (127, 0, 0),   # Dimmer Red
    (127, 63, 0),  # Dimmer Orange
    (127, 127, 0), # Dimmer Yellow
    (0, 127, 0),   # Dimmer Green
    (0, 0, 127),   # Dimmer Blue
    (37, 0, 65),   # Dimmer Indigo
    (119, 65, 119) # Dimmer Violet
]  # Second Rainbow (Darker)

def set_rgb_color(rgb_red, rgb_green, rgb_blue, red_value, green_value, blue_value):
    """Set RGB LED color using 0-255 values, converted to 0-1 scale."""
    rgb_red.value = red_value / 255
    rgb_green.value = green_value / 255
    rgb_blue.value = blue_value / 255

def move_servo(direction, duration):
    step = 0.05 if direction == "forward" else -0.05  
    start = -1 if direction == "forward" else 1       
    end = 1 if direction == "forward" else -1         
    threshold = 0.7 * end  
    
    # Calculate the time it takes to move the servo to complete one full 180-degree turn
    move_time = duration / 2  # Each 180-degree turn takes half of the total time (36 seconds)
    steps = int(move_time / 0.05)  # Calculate number of steps based on the duration and step size
    step_delay = move_time / steps  # Time delay for each step to complete the 180-degree turn in the desired time

    # Display 8 initially before movement
    display_digit(8)  
    red_led.on()
    yellow_led.off()
    green_led.off()
    set_rgb_color(rgb1_red, rgb1_green, rgb1_blue, *rainbow_colors_1[0])  # RGB1: First Color
    set_rgb_color(rgb2_red, rgb2_green, rgb2_blue, *rainbow_colors_2[0])  # RGB2: Dim First Color
    time.sleep(1)  # Delay before starting movement

    # Green Light - Ready to Move
    red_led.off()
    green_led.on()
    set_rgb_color(rgb1_red, rgb1_green, rgb1_blue, *rainbow_colors_1[3])  # RGB1: Green
    set_rgb_color(rgb2_red, rgb2_green, rgb2_blue, *rainbow_colors_2[3])  # RGB2: Dim Green
    time.sleep(0.5)  # Delay before starting movement

    # Move the Servo and Update Colors for the clockwise turn
    for position in frange(start, end, step):
        servo.value = position
        time.sleep(step_delay) 
        
        # Update RGB colors for both rainbows
        for i in range(len(rainbow_colors_1)):
            set_rgb_color(rgb1_red, rgb1_green, rgb1_blue, *rainbow_colors_1[i])  # Brighter Rainbow
            set_rgb_color(rgb2_red, rgb2_green, rgb2_blue, *rainbow_colors_2[i])  # Dimmer Rainbow

        # Yellow Light - Near Stop
        if (direction == "forward" and position >= threshold) or (direction == "backward" and position <= threshold):
            green_led.off()
            yellow_led.on()

    # Set the final colors after the servo completes the counter-clockwise turn
    servo.value = end
    yellow_led.off()
    red_led.on()
    set_rgb_color(rgb1_red, rgb1_green, rgb1_blue, *rainbow_colors_1[-1])  # RGB1: Last Color
    set_rgb_color(rgb2_red, rgb2_green, rgb2_blue, *rainbow_colors_2[-1])  # RGB2: Dim Last Color
    time.sleep(1)  # Delay before next movement

def frange(start, stop, step):
    while (step > 0 and start <= stop) or (step < 0 and start >= stop):
        yield round(start, 2)
        start += step

def main():
    print("Traffic Light, Servo, Separate Rainbow Spectrum, and 7-Segment Display Synchronization")    
    total_duration = 72  # Total duration of the program in seconds

    # Loop for 72 seconds to count and display the proper digits
    for sec in range(total_duration):
        if sec % 10 == 0:
            display_digit(0)
        elif sec % 10 == 1:
            display_digit(1)
        elif sec % 10 == 2:
            display_digit(2)
        elif sec % 10 == 3:
            display_digit(3)
        elif sec % 10 == 4:
            display_digit(4)
        elif sec % 10 == 5:
            display_digit(5)
        elif sec % 10 == 6:
            display_digit(6)
        elif sec % 10 == 7:
            display_digit(7)
        elif sec % 10 == 8:
            display_digit(8)
        elif sec % 10 == 9:
            display_digit(9)

        time.sleep(1)  # Sleep for 1 second

    # Perform the first 180-degree turn (clockwise)
    move_servo("forward", total_duration)
    time.sleep(2)  # Wait a little before starting the second turn
    
    # Perform the second 180-degree turn (counter-clockwise)
    move_servo("backward", total_duration)
    time.sleep(2)

main()