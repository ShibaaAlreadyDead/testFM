import RPi.GPIO as GPIO
import time

# Установка GPIO режима
GPIO.setmode(GPIO.BCM)

# Укажите номер пина, к которому подключен сервопривод
servo_pin = 18

# Установка пина на вывод
GPIO.setup(servo_pin, GPIO.OUT)

# Создание объекта PWM с частотой 50 Гц
pwm = GPIO.PWM(servo_pin, 50)

# Функция для установки положения сервопривода
def set_servo_position(angle):
    duty_cycle = angle / 18.0 + 2.5
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Задержка 300 миллисекунд (300 мкс)

# Начальное положение (центр)
pwm.start(7.5)
time.sleep(1)

try:
    # Поворот влево
    set_servo_position(0)

    # Возвращение в центр
    set_servo_position(90)

    # Поворот вправо
    set_servo_position(180)

    # Возвращение в центр
    set_servo_position(90)

finally:
    # Остановка PWM и выход из программы
    pwm.stop()
    GPIO.cleanup()
