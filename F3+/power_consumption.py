from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import serial
import time
import subprocess
import datetime
from lk911 import change_5min
from admin911 import b2b
import RPi.GPIO as GPIO


"""
define push-button and power
"""

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.output(16, 1)


chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"

WORK = 1

ser_uart = serial.Serial()
port_uart = '/dev/ttyS0'

counter_time_periods = 0
MAX_time_periods = 12

"""
# save log to file
"""
def write_to_file(data, filename='test_consumption.txt'):
    with open(filename, 'a') as file:
        file.write(f'{data}\n')

def push_button():
    GPIO.output(16, 0)
    time.sleep(1)
    GPIO.output(16, 1)
"""
#set com UART
"""
def com_uart_start():
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
"""
#run iot recoder 
"""

def run_iot_recorder():
    command = ["/home/pi/Desktop/test_FM/pythonProject1/iot_recoder-linux-arm", "-p", "USBCC-1A60487C0", "-t", "6000",
               "-c", "-o", "power_consumption"]
    cmd = ' '.join(command)
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

push_button()

def uart_listen():
    print("Start listen UART")
    global WORK, counter_time_periods

    found_imei = False
    imei = ""
    found_string = False
    found_ccid = False
    block_executed = False

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    service = ChromeService(executable_path=chrome_driver_path)

    driver = webdriver.Chrome(service=service, options=options)

    while WORK:
        data = ser_uart.readline()

        if data:
            write_to_file(f'{datetime.datetime.now().time()} {data}', 'test_consumption.txt')
            print(f'{datetime.datetime.now().time()} {data}')
            run_iot_recorder()

        if b'GSM: IMEI1:' in data and not found_imei:
            found_imei = True
            imei_start = data.index(b'IMEI1:') + 7
            imei_end = data.find(b'- saved\r\n', imei_start)
            imei = data[imei_start:imei_end].decode('utf-8')
            print("Found IMEI:", imei)
            
        if b'GSM: SIM1 CCID:' in data and not found_ccid:
            found_ccid = True
            ccid_start = data.index(b'GSM: SIM1 CCID:') + 15
            ccid_end = data.find(b'- saved\r\n', ccid_start)
            ccid = data[ccid_start:ccid_end].decode('utf-8').split()[0][:-1]
            print("Found CCID:", ccid)
            
        if b'SYS: OTK OK' in data:
            push_button()
            """
# set owner in admin911 and set 5 min Search in lk911fm
"""
        if b'TIME: alarm period: 0 day 0 hour 5 minute 0 secund' in data and found_string and not block_executed:
            b2b(imei)  
            time.sleep(10)
            change_5min(ccid, chrome_driver_path)
            block_executed = True
            
        if b'TIME: alarm period: 0 day 0 hour 5 minute 0 secund' in data and not found_string:
            found_string = True
            """
# after 10 T enters, stop
            
        """
        if b'SYS: sleep' in data: 
            counter_time_periods +=1

        if counter_time_periods >= MAX_time_periods:
            GPIO.output(17,1)		
            WORK = 0
            

def main():
    com_uart_start()
    uart_listen()

if __name__ == '__main__':
    main()
