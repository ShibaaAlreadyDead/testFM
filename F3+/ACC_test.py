from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import RPi.GPIO as GPIO
import serial
import time
import datetime
from lk911 import change_ACC

ser_uart = serial.Serial()
port_uart = '/dev/ttyS0'
chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"

def com_uart_start():
    """
    Configure and open the UART communication.
    """
    global ser_uart, port_uart
    print(port_uart)
    ser_uart.baudrate = 115200
    ser_uart.parity = 'N'
    ser_uart.stopbits = 1
    ser_uart.bytesize = 8
    ser_uart.timeout = 1
    ser_uart.close()
    ser_uart.port = port_uart
    ser_uart.open()
WORK = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set pins to output
GPIO.setup(13, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

# Initial position (center)
servo_pin = 13
acc_pin = 12
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(acc_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm2 = GPIO.PWM(acc_pin, 50)

def set_servo_position(angle):
    """
    Set the position of the servo motor.
    """
    duty_cycle = angle / 18.0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)

def set_servo_position2(angle):
    """
    Set the position of the second servo motor.
    """
    duty_cycle = angle / 18.0 + 2.5
    pwm2.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)

def write_to_file(data, filename='test_ACC.txt'):
    """
    Write data to a file.
    """
    with open(filename, 'a') as file:
        file.write(f'{data}\n')

def push_button():
    """
    Simulate pushing a button.
    """
    GPIO.output(16, 0)
    time.sleep(1)
    GPIO.output(16, 1)

def stop_servo():
    """
    Stop the servo motors.
    """
    set_servo_position(90)
    set_servo_position2(90)

def stop_test():
    """
    Stop the servo motors and clean up GPIO.
    """
    WORK = 0
    pwm.stop()
    pwm2.stop()
    GPIO.cleanup()

def rotate(count_start=0):
    """
    Rotate the servo motors for a certain number of times.
    """
    pwm.start(0)
    pwm2.start(0)
    for i in range(150):
        set_servo_position(90)
        set_servo_position2(90)
        set_servo_position(180)
        set_servo_position2(180)
        set_servo_position(90)
        set_servo_position2(90)
        count_start += 1

def set_default():
    """
    Set the default position of the servo motors.
    """
    set_servo_position2(0)
    set_servo_position(0)

def find_ccid(data):
    """
    Find and print the CCID from the UART data.
    """
    ccid_start = data.index(b'ICCID SIM1:') + 13
    ccid_end = data.find(b'\r\n', ccid_start)
    ccid = data[ccid_start:ccid_end].decode('utf-8').split()[0][:-2]
    print("Found CCID:", ccid)
    change_ACC(ccid, chrome_driver_path)

def uart_listen():
    """
    Listen to UART data and perform actions based on received data.
    """
    global WORK
    print("Start listen UART")
    found_ccid = False
    MAX_count = 10
    ccid = ''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    service = ChromeService(executable_path=chrome_driver_path)

    while WORK:
        data = ser_uart.readline()

        if data:
            write_to_file(f'{datetime.datetime.now().time()} {data}', 'test_ACC.txt')
            print(f'{datetime.datetime.now().time()} {data}')

        if b'ICCID SIM1:' in data and not found_ccid:
            find_ccid(data)

        if b'ACC ready for start' in data:
            rotate()

        if b'Int:00012000' in data:
            stop_servo()

        if b'SYS: acc waiting for stop 2' in data:
            set_default()

    stop_servo()  

def main():
    """
    Main function to start UART communication and listen for data.
    """
    com_uart_start()
    uart_listen()

if __name__ == '__main__':
    main()
