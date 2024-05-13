
import RPi.GPIO as GPIO
import time

# Установка GPIO режима
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Укажите номер пина, к которому подключен сервопривод
servo_pin = 13
acc_pin = 12

# Установка пина на вывод
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(acc_pin, GPIO.OUT)

# Создание объекта PWM с частотой 50 Гц
pwm = GPIO.PWM(servo_pin, 50)
pwm2 = GPIO.PWM(acc_pin, 50)

# Функция для установки положения сервопривода
def set_servo_position(angle, servo):
    duty_cycle = angle / 18 + 2  # Преобразование угла в Duty Cycle
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.2) # Задержка 300 миллисекунд (300 мкс)

# Начальное положение (центр)
pwm.start(0)
pwm2.start(0)

try:
    for i in range(150):
        # Поворот влево
        set_servo_position(90, pwm)
        set_servo_position(90, pwm2)

        # Возвращение в центр
        set_servo_position(180, pwm)
        set_servo_position(180, pwm2)
        
        # Поворот вправо
        set_servo_position(90, pwm)
        set_servo_position(90, pwm2)
        
        # Возвращение в центр
        set_servo_position(180, pwm)
        set_servo_position(180, pwm2)
finally:
    # Остановка PWM и выход из программы
    pwm.stop()
    pwm2.stop()
    GPIO.cleanup()

