# AX12_uPy
Library to control AX12 Dynamixel motors with MicroPython.

This library has been  by consulting the following link: https://github.com/jeremiedecock/pyax12

## Hardware
Since ESPXXXX MicroControllers support a UART communication, while Dynamixel Servo Motors use OneWire, an specific hardware that allows this communication between these two protocols is needed. For that, a driver board is being developed in the following repo: [OpenFPy](https://github.com/FunPythonEC/OpenFpy)

Unfortunately, while developing this library I noticed that the MicroPython firmware for the ESP8266 doesn't support the parameter `txbuf` in the UART definition, meaning in the end this library can so far only be used with the ESP32 and maybe some other boards that can work maybe with this kind of generic form of MicroPython.

## Comunication
As mentioned before, UART is used in order to send data to the servo. A circuit can also be made in order to interface the microcontroller with the servo, which an be found in the following link: [Circuit interface ESP-Dynamixel](https://electronics.stackexchange.com/questions/243740/understanding-how-a-tristate-buffer-works-74ls241) Here a pin for direction is needed apart from the TX and RX used from the ESP32 for UART. As default the following pins are needed:
* TX pin: in everyboard the position of the pin can differ, however any can be used and it is specified with the `serialid` parameter in the constructor of the `ax12` object.
* RX pin: same condition as TX pin.
* Ground pin
* 5V pin: used to power the integrated circuit but would work with external power.
* Direction pin: specified as `dir_com`, it can be any gpio from the microcontroller.

In the case of the ESP32, it has available 3 TX and RX pins, meaning 3 UART interfaces can be established. In order to specify which one is wanted to control the servo, the parameter `serialid` needs to be defined when creating the `ax12` objects, if it is 0, TX0 and RX0 ares used, and so on. For more information about UART: [UART MicroPython](https://docs.micropython.org/en/latest/library/machine.UART.html)

## `ax12.py`
 This is the core script that allows the use of Dynamixel Servos with MicroPython. In it a class called `ax12` has been defined with its respective constructor and methods. How to use it is specified below.

### Constructor

~~~~ python
from ax12 import ax12
ax12(dir_com, baudrate=1000000, serialid=2, rtime=500)
~~~~

* `dir_com`: corresponds to the number of the gpio that is going to be used in order to control the transfer of packets between the servo and the microcontroller. It is the only parameter which doesn't have a value as default.
* `baudrate`: defines the baudrate of the communication, by default it is 1Mbps, however it could be changed depending of the used by the servo.
* `serialid`: defines which TX and RX are used, by default the value is for `UART(2)`.
* `rtime`: corresponds to the Return delay time. It is the time that the servo awaits in order to respond after it receives a package. For every servo line this could be different. By default it is 500us.

#### Examples of use

~~~~ python
from ax12 import *
dxl=ax12(dir_com=22) #GPIO22 would be the one used
					#in order to control the servo
~~~~

In case `baudrate`, `serialid` and `rtime` are different:
~~~~ python
from ax12 import *
dxl=ax12(dir_com=22,baudrate=115200,serialid=1,rtime=300)
~~~~

### Functions and methods for `ax12.py`
A series of functions and methods have been implemented in the script. There are some generic functions that can be used in order to control the servo since the package creation and the methods from the class to do more specific actions. This is detailed below:

#### Generic methods
##### `makePacket(ID, instr, params=None)`
This method can be used and is used to construct the packet to send to the servo. `ID` corresponds to the ID of the servo, `instr` is the instruction that want to be sent and `params` a list of the parameters that may include the item address and values needed like speed or position.
##### `sendPacket(packet,uart,dir_com,rtime,rxbuf)`
This methos is used to send the packet returned by `makePacket`, which correspond to the parameter packet, also `uart`corresponds to the UART object used, `dir_com` the object `Pin` already specified, `rtime` explained before and `rxbuf` which is the length or maximum amount of bytes that want to be received once the servo responds.
##### `word(l, h)`
Used in order to get an intl from a Low-High byte number. `l`is the low byte and `h` high byte. Returns an int number.
##### `le(h)`
Returns Low-High byte number in a list. `h` is the int number.
###### Example
~~~~ python
from ax12 import *
dxl=ax12(dir_com=22)
#change of ID from 1 to 2
pkt=makePacket(1,WRITE,SET_ID,[2]) #packet made
dxl.sendPacket(pkt) #packet sent
~~~~
In the above example a kinda raw change of ID is made. In this case the parameter for the ID can be specified in only one byte. If the parameter can't be defined this way, the method `le` must be used which already return a list.

#### Specific write Methods

For all methods, the ID of the servo is always needed, so be sure to always define it. Also all of them have a parameter called `rxbuf`that can be specified if wanted (not showed in the table).

##### EEPROM


|Method|Purpose|Parameter description|
|-----------|-----------|--------------------------------------|
|`set_id(ID,NID)`|Change of ID of the servo.|`newID` : is the new ID wanted to be set.|
|`set_baud_rate(ID,baudrate)`|Change of baud rate.|`baudrate`: the value by default is 1. The other values are specified in the doc found in the repo.|
| `set_return_delay_time(ID,delay)` | Change of the return delay time. | `delay`: it is the 2*time that passes until the servo responds. |
|`set_cw_angle_limit(ID,angle)`|Set of limit angle for cw direction.|`angle`: value between 0 and 1023, 0 correspond to 0 degrees and 1023 to 300 degrees.|
|`set_ccw_angle_limit(ID, angle)`|Set of limit angle for ccw direction.|`angle`: value between 0 and 1023, 0 correspond to 0 degrees and 1023 to 300 degrees.|
|`set_temperature_limit(ID,temp)`|Set limit hight temperature the servo would permit to operate.|`temp`: the temperature in Degrees Celsius, can be from 0 to 255.|
|`set_lowest_voltage(ID,volt)`|Set lowest voltage of operation.|`volt`: minimum voltage so that the servo would operate.|
|`set_highest_voltage(ID,volt)`|Set highest voltage of operation.|`volt`: minimum voltage so that the servo would operate.|
|`set_max_torque(ID,torque)`|Set max torque the servo would give.|`torque`: value from 0 to 1023.|
|`set_status_return_level(ID,status)`|Change of the status return level.|`status`: value from 0 to 2.|
|`set_alarm_led(ID,alarm)`|Set led alarm.|`alarm`: corresponds to 0 for off and 1 for on.|
|`set_alarm_shutdown(ID,alarm)`|Set shutdown alarm.|`alarm`: value of 0 if off and 1 for on.|

##### RAM

|Method| Purpose                                                      | Parameter description                                        |
|:-----------|------------|---------------------------------------|
|`set_torque_enable(ID,enable)`|Enables or disables the torque.|`enable`: 1 if it is enabled and 0 if it is not.|
|`set_led(ID,led)`|Turns led on or off.|`led`: value of 1 for on and 0 for off.|
|`set_cw_compliance_margin(ID,margin)`| Set the margin of error the servo can have when asked to be in certain position, for clockwise. | `margin`: the value can be between 0 and 255.                |
| `set_ccw_compliance_margin(ID,margin)` |Set the margin of error the servo can have when asked to be in certain position, for counter clockwise.|`margin`: the value can be between 0 and 255.|
| `set_cw_compliance_slope(ID,margin)`   |Set the slope that the servo has when turning clockwise.|`slope`: the value can be between 0 and 255.|
| `goal_position(ID,angle)`              |Turn the servo to a defined angle.|`angle`: can be between 0 and 300 since in this case the conversion to degrees is always done.|
| `goal_speed(ID,speed)`                 |Set the speed in which the servo turns. If it is in endless turn mode, which is when cw and ccw angle limits are 0, then the servo would work like a wheel or dc motor.|`speed`: Value can be between 0 and 1023. If it is in endless turn, then for 0-1023 range is for cw direction, and 1024-2046 for ccw direction.|
| `set_torque_limit(ID,torque)`          |Set the limit torque of the servo.|`torque`: it is a value between 0-1023. If the power is turned on, the value of Max Torque is used as the initial value.|
| `set_lock(ID,status)`                  |Define if the EEPROM can be modified.|`status`: a value of 0 if the EEPROM is modified, and 1 if it doesn't want to be modified.|
| `set_punch(ID, punch)`                 |Defines minimum current with which the servo would work.|`punch`:  The initial value is set to 0x20 and its maximum value is 0x3ff.|

#### Specific read methods

Here could be more important to include the parameter `rxbuf` so that you get just what you want from the servo. However, it already has a value and every of the reading methods returns the packet received in `list` form.

##### EEPROM

| Methods                  | Returned info                                                |
| ------------------------ | ------------------------------------------------------------ |
| `read_model_number(ID)`  | Model number of the servo.                                   |
| `read_firmware(ID)`      | Firmware embedded in the servo.                              |
| `read_id(ID)` | ID of the connected servo. |
| `read_baud_rate(ID)`     | Current baud rate with which the servo communicates. |
| `read_return_delay_time(ID)` | The time the servo takes in order to respond after receiving its packet. |
| `read_cw_angle_limit(ID)` | Limit angle in which the servo can turn with cw direction. |
| `read_ccw_angle_limit(ID)` | Limit angle in which the servo can turn with ccw direction. |
| `read_temperature_limit(ID)` | Limit high temperature with which the servo would work. |
| `read_lowest_voltage(ID)` | Lowest voltage with which the servo would work. |
| `read_highest_voltage(ID)` | Highest voltage with which the servo would work. |
| `read_max_torque(ID)` | Max torque the servo would give. |
| `read_status_return_level(ID)` | Number of the status return level. |
| `read_alarm_led(ID)` | The alarm led value. |
| `read_alarm_shutdown(ID)` | The alarm shutdown value. |
| `read_down_calibration(ID) ` | The down calibration value. |
| `read_up_calibration(ID)` | The up calibration value. |

##### RAM
| Methods                          | Returned info                                                |
| -------------------------------- | ------------------------------------------------------------ |
| `read_torque_enable(ID)`         | Returns if torque is enabled or not.                         |
| `read_led(ID)`                   | Returns if the led is on or off.                             |
| `read_cw_compliance_margin(ID)`  | Returns the compliance margin for cw direction.              |
| `read_ccw_compliance_margin(ID)` | Returns the compliance margin for ccw direction.             |
| `read_cw_compliance_slope(ID)`   | Returns the compliance slope for cw direction.               |
| `read_ccw_compliance_slope(ID)`  | Returns the compliance slope for ccw direction.              |
| `read_goal_position(ID)`         | Returns the last asked angle.                                |
| `read_moving_speed(ID)`          | Returns the last requested speed.                            |
| `read_torque_limit(ID)`          | Returns the torque limit.                                    |
| `read_present_position(ID)`      | Returns the angle present position.                          |
| `read_present_speed( ID)`        | Returns the current speed in which the servo is moving.      |
| `read_present_load(ID)`          | Returns the current applied load.                            |
| `read_present_voltage(ID)`       | Returns the current voltage received by the servo.           |
| `read_moving(ID)`                | Returns a value that expresses if the servo is moving or not. |
| `read_lock(ID)`                  | Returns if the EEPROM can be modified or not.                |
| `read_punch(ID)`                 | Returns the current that the servo needs to work.            |





## Referencias
* [Dynamixel Protocol 1.0](http://emanual.robotis.com/docs/en/dxl/protocol1/)
* [Main info Dynamixel AX12](http://support.robotis.com/en/product/actuator/dynamixel/ax_series/dxl_ax_actuator.htm#Actuator_Address_28)
