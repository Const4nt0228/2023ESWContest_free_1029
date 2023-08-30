import RPi.GPIO as GPIO
from time import sleep
import keyboard


class servo_module:
    def __init__(self):
        print('servo_init')
        self.servo1_pin = 20
        self.servo2_pin = 21

        # GPIO 초기화
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo1_pin, GPIO.OUT)
        GPIO.setup(self.servo2_pin, GPIO.OUT)

        # PWM 객체 생성
        self.servo1_pwm = GPIO.PWM(self.servo1_pin, 50)  # 50Hz 주파수로 PWM 생성
        self.servo2_pwm = GPIO.PWM(self.servo2_pin, 50)

        # PWM 시작
        self.servo1_pwm.start(0)
        self.servo2_pwm.start(0)
        # 서보모터 각도 변수
        self.servo1_angle = 0
        self.servo2_angle = 0

    def servo_start(self):
        try:
            while True:
                if keyboard.is_pressed('w'):
                    self.servo1_angle += 5
                    if self.servo1_angle > 170:
                        self.servo1_angle = 170
                    self.set_servo_angle(self.servo1_pwm, self.servo1_angle)
                elif keyboard.is_pressed('s'):
                    self.servo1_angle -= 5
                    if self.servo1_angle < 10:
                        self.servo1_angle = 10
                    self.set_servo_angle(self.servo1_pwm, self.servo1_angle)
                else:
                    self.servo1_pwm.ChangeDutyCycle(0)

                if keyboard.is_pressed('a'):
                    self.servo2_angle += 5
                    if self.servo2_angle > 170:
                        self.servo2_angle = 170
                    self.set_servo_angle(self.servo2_pwm, self.servo2_angle)
                elif keyboard.is_pressed('d'):
                    self.servo2_angle -= 5
                    if self.servo2_angle < 10:
                        self.servo2_angle = 10
                    self.set_servo_angle(self.servo2_pwm, self.servo2_angle)
                else:
                    self.servo2_pwm.ChangeDutyCycle(0)

                sleep(0.1)  # 입력 처리 주기
        except KeyboardInterrupt:
            pass
        finally:
            self.servo1_pwm.stop()
            self.servo2_pwm.stop()
            GPIO.cleanup()

    # 서보모터 각도 설정 함수
    def set_servo_angle(self, pwm, angle):
        duty_cycle = (angle / 18) + 2
        pwm.ChangeDutyCycle(duty_cycle)


if __name__ == "__main__":
    main = servo_module()
    main.servo_start()
