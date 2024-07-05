import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 设置继电器连接GPIO引脚
relay_pin = 21

# 设置GPIO引脚为输出模式
GPIO.setup(relay_pin,GPIO.OUT)
def turn_on_fan():
	try:
		# 执行一次就可以
		GPIO.output(relay_pin,GPIO.HIGH)
		print('继电器打开')
	except KeyboardInterrupt:
		# 当用户按下ctrl+c时，清理
		print('程序已停止')
		GPIO.cleanup()

def turn_off_fan():
	try:
		# 关闭继电器
		GPIO.output(relay_pin,GPIO.LOW)
		print('继电器关闭')
	except KeyboardInterrupt:
		# 当用户按下ctrl+c时，清理
		print('程序已停止')
		GPIO.cleanup()
if __name__ == '__main__':
	# turn_on_fan()
	# time.sleep(5) # 保持开5秒
	turn_off_fan()
