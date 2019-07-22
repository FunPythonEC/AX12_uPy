from ax12 import ax12
from time import sleep
motor=ax12(dir_com=22, baudrate=1000000, serialid=2)
motor.set_ccw_angle_limit(1,1023)
sleep(1)
i=0
while i<=300:
    motor.goal_position(1,i)
    sleep(1)
    i+=10