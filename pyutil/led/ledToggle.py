import RPi.GPIO as GPIO # type: ignore
import time

LED = 21

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for led toggling
GPIO.setup(26, GPIO.OUT)
GPIO.setup(LED, GPIO.IN, pull_up_down=GPIO.PUD_UP)

prev_state = GPIO.input(LED)
print(f"original state of btn: {prev_state}")

try:
    while True:
        if GPIO.input(LED) != prev_state:
            print(f"Btn state changed to: {GPIO.input(LED)}")
            GPIO.output(26, GPIO.input(LED))
            prev_state = GPIO.input(LED)
            time.sleep(0.5)

except Exception as e:
    if isinstance(e, KeyboardInterrupt):
        print("Program interrupted by user.")
    else:
        print(f"An error occurred: {e}")
finally:
    # Clean up the GPIO pins and stop the PWM
    GPIO.cleanup()