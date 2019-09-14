import machine as m #control uart and dir_com
import utime #time control

#every instruction constants
PING 		= 		0x01
READ        = 		0x02
WRITE       = 		0x03
REG         = 		0x04
ACTION      = 		0x05
RESET       = 		0x06
SYNC        = 		0x83

BROADCAST_ID = 0xfe
HEADER = [255,255]

# CONTROL TABLE (ADDRESSES)
# (see the official Dynamixel AX-12 User's manual p.12)
MODEL_NUMBER 				= 0x00
VERSION_OF_FIRMWARE 		= 0x02
SET_ID 						= 0x03
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

#object to initialize the servo
class ax12(object):

	#for the constructor, only dir_com needs to be specifiec
	#which represents which pin will control the direction of communication.
	def __init__(self, dir_com, baudrate=1000000, serialid=2):

		self.baudrate=baudrate
		self.serialid=serialid
		self.dir_com=m.Pin(dir_com,m.Pin.OUT) #a pin for the communication direction is defined

		#uart object defined
		try:
			self.uart = m.UART(self.serialid,self.baudrate)
			self.uart.init(self.baudrate, bits=8, parity=None, stop=1, txbuf=0)
		except Exception as e:
			print(e)

#METHODS
#in the methods, every parameter that needs to be specified as a Low/High Byte
#is defined with the help of the le() function
#==============================EEPROM METHODS======================================
#WRITING METHODS ONLY

	def set_id(self, ID, NID):
		sendPacket(bytearray(makePacket(ID,WRITE,[SET_ID, NID])), self.uart, self.dir_com)

	def set_baud_rate(self,ID,baudrate):
		sendPacket(bytearray(makePacket(ID,WRITE,[BAUD_RATE, baudrate])), self.uart, self.dir_com)

	def set_delay(self,ID,delay):
		sendPacket(bytearray(makePacket(ID,WRITE,[RETURN_DELAY_TIME, delay])), self.uart, self.dir_com)

	def set_cw_angle_limit(self,ID,angle):
		sendPacket(bytearray(makePacket(ID,WRITE,[CW_ANGLE_LIMIT]+le(angle))), self.uart, self.dir_com)

	def set_ccw_angle_limit(self,ID,angle):
		sendPacket(bytearray(makePacket(ID,WRITE,[CCW_ANGLE_LIMIT]+le(angle))), self.uart, self.dir_com)

	def set_temperature_limit(self,ID,temp):
		sendPacket(bytearray(makePacket(ID,WRITE,[HIGHEST_LIMIT_TEMPERATURE, temp])), self.uart, self.dir_com)

	def set_lowest_voltage(self,ID,volt):
		sendPacket(bytearray(makePacket(ID,WRITE,[HIGHEST_LIMIT_VOLTAGE, volt])), self.uart, self.dir_com)

	def set_highest_voltage(self,ID,volt):
		sendPacket(bytearray(makePacket(ID,WRITE,[LOWEST_LIMIT_VOLTAGE, volt])), self.uart, self.dir_com)

	def set_max_torque(self,ID,torque):
		sendPacket(bytearray(makePacket(ID,WRITE,[MAX_TORQUE]+le(torque))), self.uart, self.dir_com)

	def set_alarm_led(self,ID,alarm):
		sendPacket(bytearray(makePacket(ID,WRITE,[ALARM_LED, alarm])), self.uart, self.dir_com)

	def set_alarm_shutdown(self,ID,alarm):
		sendPacket(bytearray(makePacket(ID,WRITE,[ALARM_SHUTDOWN, alarm])), self.uart, self.dir_com)

#READING METHODS ONLY
#will be soon implemented

#==============================RAM METHODS=========================================
#WRITING METHODS ONLY

	def set_torque_enable(self,ID,enable):
		sendPacke(bytearray(makePacket(ID,WRITE,[TORQUE_ENABLE, enable])), self.uart, self.dir_com)

	def set_led(self,ID,led):
		sendPacket(bytearray(makePacket(ID,WRITE,[LED, led])), self.uart, self.dir_com)

	def goal_position(self,ID,angle):
		sendPacket(bytearray(makePacket(ID,WRITE,[GOAL_POSITION]+le(int(angle/300*1023)))), self.uart, self.dir_com)

	def goal_speed(self,ID,speed):
		sendPacket(bytearray(makePacket(ID,WRITE,[MOVING_SPEED]+le(speed))), self.uart, self.dir_com)

	def set_torque_limit(self,ID,torque):
		sendPacket(bytearray(makePacket(ID,WRITE,[TORQUE_LIMIT]+le(torque))), self.uart, self.dir_com)

	def set_led(self,ID,led):
		sendPacket(bytearray(makePacket(ID,WRITE,[led])), self.uart, self.dir_com)
		

#READING METHODS ONLY
#will be soon implemented

#=================================================================


#function to send instruction
def sendPacket(packet, uart, dir_com):
	dir_com.value(1)
	uart.write(packet)
	
	tinit=utime.ticks_us()
	while (utime.ticks_us()-tinit)<500:
		pass
	dir_com.value(0)
	resp=uart.read()
	if resp != None:
		return list(resp)



#function to construct a packet easily
def makePacket(ID, instr, params=None):

	pkt = []
	pkt += [ID]
	if params:
		pkt += [len(params)+2]
	else:
		pkt += [2]
	pkt += [instr]  # instruction
	if params:
		pkt += params
	pkt += [checksum(pkt)]
	pkt = HEADER+pkt  # header and reserved byte
	print(pkt)
	return pkt

#turn Low-High byte into decimal
def word(l, h):
	"""
	Given a low and high bit, converts the number back into a word.
	"""
	return (h << 8) + l

def le(h):
	"""
	Little-endian, takes a 16b number and returns an array arrange in little
	endian or [low_byte, high_byte].
	"""
	h &= 0xffff  # make sure it is 16 bits
	return [h & 0xff, h >> 8]

def checksum(packet): #needed to include checksum easily in packet
	#Instruction Checksum = ~( ID + Length + Instruction + Parameter1 + … Parameter N )
	return le(~(sum(packet)))[0]