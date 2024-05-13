import RPi.GPIO as GPIO
import serial
import time
import datetime
from admin911 import change_1_min_GPS

WORK = 1
ser_uart = serial.Serial(port='/dev/ttyS0', baudrate=115200, parity='N', stopbits=1, bytesize=8, timeout=1)

"""
GPIO Pins
"""
GPIO_PIN_JAMMER_GSM = 25
GPIO_PIN_JAMMER_GPS = 22
GPIO_PIN_JAMMER_3G = 27
GPIO_PIN_SERVO = 13
GPIO_PIN_ACC = 12
GPIO_PIN_BUTTON = 16
"""
Set GPIO pin 
"""
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(GPIO_PIN_JAMMER_GSM, GPIO.OUT)
    GPIO.setup(GPIO_PIN_JAMMER_GPS, GPIO.OUT)
    GPIO.setup(GPIO_PIN_JAMMER_3G, GPIO.OUT)
    GPIO.setup(GPIO_PIN_SERVO, GPIO.OUT)
    GPIO.setup(GPIO_PIN_ACC, GPIO.OUT)
    GPIO.setup(GPIO_PIN_BUTTON, GPIO.OUT)
    GPIO.output(GPIO_PIN_JAMMER_GSM, 1)
    GPIO.output(GPIO_PIN_JAMMER_GPS, 1)
    GPIO.output(GPIO_PIN_JAMMER_3G, 1)
    stop_servo()

def jammer(enable=True):
    '''
    Enable or disable jammer.
    '''
    GPIO.output(GPIO_PIN_JAMMER_GSM, 0 if enable else 1)
    GPIO.output(GPIO_PIN_JAMMER_GPS, 0 if enable else 1)
    GPIO.output(GPIO_PIN_JAMMER_3G, 0 if enable else 1)

def rotate():
    '''
    Rotate the servo motors.
    '''
    pwm = GPIO.PWM(GPIO_PIN_SERVO, 50)
    pwm2 = GPIO.PWM(GPIO_PIN_ACC, 50)
    pwm.start(0)
    pwm2.start(0)
    for _ in range(3):
        for angle in [90, 180]:
            set_servo_position(pwm, angle)
            set_servo_position(pwm2, angle)
    pwm.stop()
    pwm2.stop()

def set_servo_position(pwm, angle):
    '''
    Set the position of the servo motor.
    '''
    duty_cycle = angle / 18.0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)

def stop_servo():
    '''
    Stop the servo motors.
    '''
    set_servo_position(GPIO_PIN_SERVO, 90)
    set_servo_position(GPIO_PIN_ACC, 90)

def push_button():
    '''
    Simulate pushing a button.
    '''
    GPIO.output(GPIO_PIN_BUTTON, 0)
    time.sleep(1)
    GPIO.output(GPIO_PIN_BUTTON, 1)

def write_to_file(data, filename='test_parking.txt'):
    with open(filename, 'a') as file:
        file.write(f'{data}\n')

def uart_listen():
    print("Start listen UART")
    global WORK
    flag_parking = False
    found_imei = False
    gps_not_found_count = 0
    CSQ_not_found = 0
    sleep_count = 0
    while WORK:
        data = ser_uart.readline()
        if data:
            write_to_file(f'{datetime.datetime.now().time()} {data}', 'test_parking.txt')
            print(f'{datetime.datetime.now().time()} {data}')
        if b'IMEI1:' in data and found_imei:
            imei_start = data.index(b'IMEI1:') + 7
            imei_end = data.index(b'\r\n', imei_start)
            imei = data[imei_start:imei_end].decode('utf-8')
            print("Found IMEI:", imei)
            found_imei = True
            change_1_min_GPS(imei)
        if b'GSM: powering up\r\n' in data:
            CSQ_not_found += 1
            jammer()
            print("Jammer ON")
            if CSQ_not_found == 2:
                jammer(enable=False)  
        if b'SYS: GPS process\r\n' in data:
            jammer()
            print("Jammer ON")
            gps_not_found_count += 1
        if b'SYS: parking==0, set parking=1\r\n' in data:
            jammer(enable=False)  
        if b'SYS: set parking flag, set acc start event\r\n' in data:
            jammer(enable=False)  
            rotate()
        if b'Int:00010000\r\n' in data:
            stop_servo()
        if b'SYS: GPS position was found\r\n' in data:
            time.sleep(900)  
        if CSQ_not_found == 2 and gps_not_found_count == 3:
            jammer(enable=False) 
        if b'TIME: alarm period: 0 day 0 hour 5 minute 0 secund\r\n' in data:
            sleep_count +=1
        if b'TIME: alarm period: 0 day 0 hour 5 minute 0 secund\r\n' in data and sleep_count ==3:
            WORK = 0

def main():
    setup_gpio()
    uart_listen()

if __name__ == "__main__":
    main()
