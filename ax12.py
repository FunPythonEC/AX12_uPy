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

	#for the constructor, only dir_com needs to be specific
	#which represents which pin will control the direction of communication
	#rtime is usuall known by user but correspond to RETURN_DELAY_TIME
	def __init__(self, dir_com, baudrate=1000000, serialid=2, rtime=500):

		self.baudrate=baudrate
		self.serialid=serialid
		self.rtime=rtime
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
#for all methods a parameter called rxbuf have been added which specifies the amount of bytes
#that would be wanted to be received when reading, by default it is 15
#==============================EEPROM METHODS======================================
#WRITING METHODS ONLY

	def set_id(self, ID, NID, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[SET_ID, NID])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_baud_rate(self,ID,baudrate, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[BAUD_RATE, baudrate])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_return_delay_time(self,ID,delay):
		sendPacket(bytearray(makePacket(ID,WRITE,[RETURN_DELAY_TIME, delay])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_cw_angle_limit(self,ID,angle, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[CW_ANGLE_LIMIT]+le(angle))), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_ccw_angle_limit(self,ID,angle, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[CCW_ANGLE_LIMIT]+le(angle))), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_temperature_limit(self,ID,temp, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[HIGHEST_LIMIT_TEMPERATURE, temp])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_lowest_voltage(self,ID,volt, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[HIGHEST_LIMIT_VOLTAGE, volt])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_highest_voltage(self,ID,volt, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[LOWEST_LIMIT_VOLTAGE, volt])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_max_torque(self,ID,torque, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[MAX_TORQUE]+le(torque))), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_status_return_level(self,ID,status,rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[STATUS_RETURN_LEVEL,status])), self.uart, self.dir_com, self.rtime,rxbuf)

	def set_alarm_led(self,ID,alarm, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[ALARM_LED, alarm])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_alarm_shutdown(self,ID,alarm, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[ALARM_SHUTDOWN, alarm])), self.uart, self.dir_com, self.rtime, rxbuf)

#READING METHODS ONLY

	def read_model_number(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID, READ,[MODEL_NUMBER])), self.uart, self.dir_com, self.rtime, rxbuf)
		return resp

	def read_firmware(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID, READ,[VERSION_OF_FIRMWARE])), self.uart, self.dir_com, self.rtime, rxbuf)
		return resp

	def read_id(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[SET_ID])), self.uart, self.dir_com, self.rtime, rxbuf)
		return resp

	def read_baud_rate(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID, READ,[BAUD_RATE])), self.uart, self.dir_com, self.rtime, rxbuf)
		return resp

	def read_return_delay_time(self, ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[RETURN_DELAY_TIME])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_cw_angle_limit(self, ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[CW_ANGLE_LIMIT])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_ccw_angle_limit(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[CCW_ANGLE_LIMIT])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_temperature_limit(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[HIGHEST_LIMIT_TEMPERATURE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_lowest_voltage(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[LOWEST_LIMIT_VOLTAGE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_highest_voltage(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[HIGHEST_LIMIT_VOLTAGE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_max_torque(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[MAX_TORQUE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_status_return_level(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[STATUS_RETURN_LEVEL])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_alarm_led(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[ALARM_LED])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_alarm_shutdown(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[ALARM_SHUTDOWN])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_down_calibration(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[DOWN_CALIBRATION])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_up_calibration(self,ID,rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[UP_CALIBRATION])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp


#==============================RAM METHODS=========================================
#WRITING METHODS ONLY

	def set_torque_enable(self,ID,enable, rxbuf=15):
		sendPacke(bytearray(makePacket(ID,WRITE,[TORQUE_ENABLE, enable])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_led(self,ID,led, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[LED, led])), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_cw_compliance_margin(self,ID,margin, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[CW_COMPLIENCE_MARGIN,margin])), self.uart, self.dir_com, self.rtime,rxbuf)

	def set_ccw_compliance_margin(self,ID,margin, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[CCW_COMPLIENCE_MARGIN,margin])), self.uart, self.dir_com, self.rtime,rxbuf)

	def set_cw_compliance_slope(self,ID,margin, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[CW_COMPLIENCE_SLOPE,margin])), self.uart, self.dir_com, self.rtime,rxbuf)

	def set_ccw_compliance_slope(self,ID,margin, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[CCW_COMPLIENCE_SLOPE,margin])), self.uart, self.dir_com, self.rtime,rxbuf)

	def goal_position(self,ID,angle,rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[GOAL_POSITION]+le(int(angle/300*1023)))), self.uart, self.dir_com, self.rtime, rxbuf)

	def goal_speed(self,ID,speed, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[MOVING_SPEED]+le(speed))), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_torque_limit(self,ID,torque, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[TORQUE_LIMIT]+le(torque))), self.uart, self.dir_com, self.rtime, rxbuf)

	def set_lock(self,ID,status, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[LOCK,status])), self.uart, self.dir_com, self.rtime,rxbuf)

	def set_punch(self,ID, punch, rxbuf=15):
		sendPacket(bytearray(makePacket(ID,WRITE,[PUNCH]+le(punch))), self.uart, self.dir_com, self.rtime,rxbuf)

#READING METHODS ONLY

	def read_torque_enable(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[TORQUE_ENABLE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_led(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[LED])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_cw_compliance_margin(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[CW_COMPLIENCE_MARGIN])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_ccw_compliance_margin(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[CCW_COMPLIENCE_MARGIN])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_cw_compliance_slope(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[CW_COMPLIENCE_SLOPE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_ccw_compliance_slope(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[CCW_COMPLIENCE_SLOPE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_goal_position(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[GOAL_POSITION])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_moving_speed(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[MOVING_SPEED])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_torque_limit(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[TORQUE_LIMIT])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_present_position(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[PRESENT_POSITION])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_present_speed(self, ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[PRESENT_SPEED])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_present_load(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[PRESENT_LOAD])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_present_voltage(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[PRESENT_VOLTAGE])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_moving(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[MOVING])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_lock(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[LOCK])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

	def read_punch(self,ID, rxbuf=15):
		resp=sendPacket(bytearray(makePacket(ID,READ,[PUNCH])), self.uart, self.dir_com, self.rtime,rxbuf)
		return resp

#=================================================================
#RESET METHODS
	def reset(self,ID,rxbuf=15):
		sendPacket(bytearray(makePacket(ID,RESET), self.uart, self.dir_com, self.rtime,rxbuf))

	def sendPacket(self, packet, uart=self.uart, dir_com=self.dir_com, rtime=self.rtime, rxbuf=15):
		dir_com.value(1) #turn on so packet is sent
		uart.write(packet)
		
		#time is traced in order to know when to listen
		tinit=utime.ticks_us()
		while (utime.ticks_us()-tinit)<rtime:
			pass

		dir_com.value(0) #off to receive packet

		tinit=utime.ticks_us()
		while (utime.ticks_us()-tinit)<1600: #timeout of 1600us
			resp=uart.read(rxbuf)
			if resp is not None:
				return list(resp)
		return None

#function to send instruction
def sendPacket(packet, uart, dir_com, rtime, rxbuf):
	dir_com.value(1) #turn on so packet is sent
	uart.write(packet)
	
	#time is traced in order to know when to listen
	tinit=utime.ticks_us()
	while (utime.ticks_us()-tinit)<rtime:
		pass

	dir_com.value(0) #off to receive packet

	tinit=utime.ticks_us()
	while (utime.ticks_us()-tinit)<1600: #timeout of 1600us
		resp=uart.read(rxbuf)
		if resp is not None:
			return list(resp)
	return None



#function to construct a packet easily
def makePacket(ID, instr, params=None):

	pkt = HEADER+[ID]
	if params:
		pkt += [len(params)+2]+[instr]+params
	else:
		pkt += [2]+[instr]
	pkt += [checksum(pkt[2:])]
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