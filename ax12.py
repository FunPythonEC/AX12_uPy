import machine as m
import time
import utime

PING 		= 		0x01
READ_DATA   = 		0x02
WRITE_DATA  = 		0x03
REG_WRITE   = 		0x04
ACTION      = 		0x05
RESET       = 		0x06
SYNC_WRITE  = 		0x83

BROADCAST_ID = 0xfe
PACKET_HEADER = bytes((0xff, 0xff))

# CONTROL TABLE (ADDRESSES)
# (see the official Dynamixel AX-12 User's manual p.12)

MODEL_NUMBER 				= 0x00
VERSION_OF_FIRMWARE 		= 0x02
ID 							= 0x03
BAUD_RATE 					= 0x04
RETURN_DELAY_TIME 			= 0x05
CW_ANGLE_LIMIT 				= 0x06
CCW_ANGLE_LIMIT 			= 0x08
HIGHEST_LIMIT_TEMPERATURE 	= 0x0b
LOWEST_LIMIT_VOLTAGE 		= 0x0c
HIGHEST_LIMIT_VOLTAGE 		= 0x0d
MAX_TORQUE 					= 0x0e
STATUS_RETURN_LEVEL 		= 0x10
ALARM_LED 					= 0x11
ALARM_SHUTDOWN 				= 0x12
DOWN_CALIBRATION 			= 0x14
UP_CALIBRATION 				= 0x16
TORQUE_ENABLE 				= 0x18
LED 						= 0x19
CW_COMPLIENCE_MARGIN 		= 0x1a
CCW_COMPLIENCE_MARGIN 		= 0x1b
CW_COMPLIENCE_SLOPE 		= 0x1c
CCW_COMPLIENCE_SLOPE 		= 0x1d
GOAL_POSITION 				= 0x1e
MOVING_SPEED 				= 0x20
TORQUE_LIMIT 				= 0x22
PRESENT_POSITION 			= 0x24
PRESENT_SPEED 				= 0x26
PRESENT_LOAD 				= 0x28
PRESENT_VOLTAGE 			= 0x2a
PRESENT_TEMPERATURE 		= 0x2b
REGISTRED_INSTRUCTION 		= 0x2c
MOVING 						= 0x2e
LOCK 						= 0x2f
PUNCH 						= 0x30