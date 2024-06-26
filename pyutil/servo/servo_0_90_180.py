import RPi.GPIO as GPIO # type: ignore
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the servo signal
SERVO_PIN = 26
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Initialize PWM on the servo pin with a frequency of 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    """Helper function that controls the servo angle."""
    duty_cycle = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Rotate the servo to 0 degrees
        set_angle(0)
        time.sleep(2)

        # Rotate the servo to 90 degrees
        set_angle(90)
        time.sleep(2)

        # Rotate the servo to 180 degrees
        set_angle(180)
        time.sleep(2)

except Exception as e:
    if isinstance(e, KeyboardInterrupt):
        print("Program interrupted by user.")
    else:
        print(f"An error occurred: {e}")
finally:
    # Clean up the GPIO pins and stop the PWM
    pwm.stop()
    GPIO.cleanup()