import RPi.GPIO as GPIO
import serial
import time
import subprocess
from lk911 import change_5min
import datetime

WORK = 1
ser_uart = serial.Serial(port='/dev/ttyS0', baudrate=115200, parity='N', stopbits=1, bytesize=8, timeout=1)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.output(16, 1)


def write_to_file(data, filename='test_update.txt'):
    with open(filename, 'a') as file:
        file.write(f'{data}\n')


def push_button():
    GPIO.output(16, 0)
    time.sleep(1)
    GPIO.output(16, 1)


def com_uart_start(port_uart):
    ser_uart.port = port_uart
    ser_uart.open()


push_button()


def uart_listen():
    found_ccid = False
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    print("Start listen UART")
    sleep_5_min_executed = False
    sms_executed = False
    counter_time_periods = 0
    MAX_time_periods = 7
    found_ccid = False
    global WORK
    while WORK:
        data = ser_uart.readline()
        if data:
            write_to_file(f'{datetime.datetime.now().time()} {data}', 'test_update.txt')
            print(f'{datetime.datetime.now().time()} {data}')
            
            if b'GSM: SIM1 CCID:' in data and not found_ccid:
                found_ccid = True
                ccid_start = data.index(b'GSM: SIM1 CCID:') + 15
                ccid_end = data.find(b'- saved\r\n', ccid_start)
                ccid = data[ccid_start:ccid_end].decode('utf-8').split()[0][:-1]
                print("Found CCID:", ccid)

            if b'SYS: OTK OK\r\n' in data:
                print("found OTK OK")
                push_button()
                time.sleep(20)
                change_5min(ccid, chrome_driver_path)

            if b'TIME: alarm period: 0 day 0 hour 5 minute 0 secund\r\n' in data:
                counter_time_periods +=1
                if not sleep_5_min_executed:
                    print("Found Sleep 5 min", sleep_5_min_executed)
                    push_button()
                if sleep_5_min_executed:
                    print("Found Sleep 5 min", sleep_5_min_executed)
                    push_button()

            if b'GSM: time remaining 15:00\r\n' in data:
                send_smsreg()

            if b'GSM: time remaining 3:00\r\n' in data and not sms_executed:
                send_sms()
                print("Trying to send SMS")
                sms_executed = True
                sleep_5_min_executed = True
            if b'GSM: time remaining 2:45\r\n' in data:
                sleep_5_min_executed = None
                send_second_sms()

        if counter_time_periods == MAX_time_periods:
            WORK = 0
     



def send_sms():
    cmd = "echo -n ':update=uri=xxx.XXX' > /home/pi/modem/dial_sms/outbox/OUT101_FM_02_+79111263034_00.txt"
    execute_ssh_command(cmd)


def send_second_sms():
    cmd = "echo -n ':update' > /home/pi/modem/dial_sms/outbox/OUT101_FM_02_+79111263034_00.txt"
    execute_ssh_command(cmd)


def send_smsreg():
    cmd = "echo -n 'Test' > /home/pi/modem/dial_sms/outbox/OUT101_FM_02_+79111263034_00.txt"
    execute_ssh_command(cmd)


def execute_ssh_command(cmd):
    ip = '192.168.245.43'
    username = 'root'
    password = 't00r1234'
    proc = subprocess.Popen(f'sshpass -p {password} ssh {username}@{ip} {cmd}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    retcode = proc.wait()
    stdout = proc.stdout.read().decode()
    stderr = proc.stderr.read().decode()


def main():
    com_uart_start()
    uart_listen()

if __name__ == '__main__':
    main()

