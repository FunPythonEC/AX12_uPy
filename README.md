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
#cambio de id, de 1 a 2
pkt=makePacket(1,WRITE,SET_ID,[2]) #packet made
dxl.sendPacket(pkt)
~~~~
In the above example a kinda raw change of ID is made. In this case the parameter for the ID can be specified in only one byte. If the parameter can't be defined this way, the method `le` must be used which already return a list.

#### Especificos de escritura
##### EEPROM
Tener en cuenta que para que el EEPROM sea modificable, es necesario que TORQUE_ENABLE tenga 0 como valor, si es cambiado a 1, EEPROM no puede ser modificado.

|Metodo|¿Qué hace?|Descripcion de parametros|
|-----------|-----------|--------------------------------------|
|||**|
|set_id(ID,newID)|Ayuda a cambiar o setear un id nuevo a uno de los motores.|**ID**: es el id del motor al que se le cambiara. **newID**: es el nuevo ID que se sobreescribira|
|set_baudrate(ID,baudrate)|Seteo de baud rate a uno de los motores.|**baudrate**:los valores van desde 0 a 3. Cada uno especificando un valor de baudios tal y como se muestra en la documentación del motor, que puede ser desde 9600 hasta 1000000.|
|set_cw_angle_limit(ID,angle)|Seteo de ángulo límite para el movimiento del motor en sentido horario.|**angle**: en este caso, por las capacidades del motor xl320, el valor de angulos para el cual permite el giro funcionando como un servo motor (JOINT mode) es desde 0 hasta 300 grados.|
|set_ccw_angle_limit(ID, angle)|Seteo de ángulo límite para el movimiento del motor en sentido antihorario.|**angle**: en este caso, por las capacidades del motor xl320, el valor de angulos para el cual permite el giro funcionando como un servo motor (JOINT mode) es desde 0 hasta 300 grados.|
|set_max_torque(ID,torque)|Seteo de torque máximo que puede ejercer el motor.|**torque**: el valor puede variar de 0 a 1023, siendo 1023 el máximo de torque que es capaz de ejercer el motor.|

##### RAM

|Metodo|¿Qué hace?|Descripción de parámetros|
|:-----------|------------|---------------------------------------|
|torque_enable(ID,status)|Deshabilita o habilita el torque.|**status**: el valor puede ser 1 (wheel mode) o 2 (joint mode).|
|goal_speed(ID,speed)|Pone una velocidad definida a la que se mueva el motor, funciona diferente dependiendo del modo de control en el que se encuentre.|**speed**: (JOINT) para este caso speed se refiere a la velocidad a la que girará el motor cuando se le especifique un ángulo, su valor puede ser entre 0-1023. (WHEEL) en este caso, se refiere a la velocidad a la que se quiere que se mueva el motor actualmente, su valor puede ser entre 0-2047. 0-1023 para que gire en un sentido. 1024-2047 para el otro.|
|goal_position(ID,position)|Coloca al motor en una posición definida que se da por el ángulo como posición.|**position**: corresponde al ángulo en que se quiere que se ponga el motor.|
|goal_torque(ID, torque)|Setea el torque en un valor definido.|**torque**: su valor es entre 0-1023, siendo 1023 el valor máximo.|

#### Especificos de lectura

Todos los metodos de lectura tiene como parámetro nada más que el ID, por lo que no se explica a continucación, solo que hace cada metodo.

Tener en cuenta que todos los metodos de lectura, al usarlos, por ahora imprimen todo lo que le llega al microcontrolador. Se tiene que entonces identificar que generalmente el unico print que se mostraría es lo que envia como respuesta el motor. Lo cual correspondera a un paquete del cual se tendrá que identificar los valores regresados.

##### EEPROM

| Metodos                  | ¿Qué hace?                                                   |
| ------------------------ | ------------------------------------------------------------ |
| read_model_number(ID)    | Lectura el numero de modelo del motor.                       |
| read_firmware(ID)        | Lectura el firmware que tiene el motor.                      |
| read_baudrate(ID)        | Lectura el valor de baud rate con el que esta trabajando el motor para la comunicación. |
| read_delay_time(ID)      | Lectura el tiempo de delay entre escritura y respuesta. **Todavia no esta implementado el metodo para el cambio de delay time** |
| read_cw_angle_limit(ID)  | Lectura de angulo limite para el giro horario.               |
| read_ccw_angle_limit(ID) | Lectura de angulo limite para el giro anti-horario.          |
| read_control_mode(ID)    | Lectura de modo de control actual.                           |
| read_max_torque(ID)      | Lectura de torque máximo al cual ha sido seteado el motor.   |
| read_return_level(ID)    | Lectura de nivel de retorno en el motor.                     |

##### RAM
| Metodos                      | ¿Qué hace?                                                   |
| ---------------------------- | ------------------------------------------------------------ |
| read_torque_enable(ID)       | Lectura del estado de torque, si esta activado o no.         |
| read_goal_torque(ID)         | Lectura de el valor de torque al que se haya seteado el motor. |
| read_goal_speed(ID)          | Lectura del valor de goal speed puesto.                      |
| read_present_position(ID)    | Lectura de la posición actual del motor.                     |
| read_present_speed(ID)       | Lectura de la velocidad actual del motor.                    |
| read_present_load(ID)        | Lectura del peso o fuerza ejercida por el motor.             |
| read_present_voltage(ID)     | Lectura del voltage presente suministrado al motor.          |
| read_present_temperature(ID) | Lectura de temperatura actual del motor.                     |
| read_moving(ID)              | Lectura de estado del motor, para saber si esta o no en movimiento. |
| read_hw_error_status(ID)     | Lectura de estado de error de hardware.                      |
| read_goal_position(ID)       | Lectura de valor de goal position indicado.                  |
| read_punch(ID)               | Lectura de minima corriente suministrada al motor.           |





## Referencias

