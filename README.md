# AX12_uPy
Library to control AX12 Dynamixel motors with MicroPython.

This library has been  by consulting the following link: https://github.com/jeremiedecock/pyax12

## Hardware
Since ESPXXXX MicroControllers support a UART communication, while Dynamixel Servo Motors use OneWire, an specific hardware that allows this communication between these two protocols is needed. For that, a driver board is being developed in the following repo: [OpenFPy](https://github.com/FunPythonEC/OpenFpy)

## Comunicación con el motor

Para la comunicación se utiliza UART. A pesar de que los motores dynamixel para la comunicación utilizan un pin DATA, este puede ser manejado utilizando la siguiente configuración electrónica: [UART to 1-WIRE interface](https://hackaday.com/2015/01/29/easier-uart-to-1-wire-interface/)

Para su uso en la parte de programación, se ha especificado en el constructor de `ax12()`, el id de UART a usar que es especificado como serialid, ya que ciertas placas carecen de cierta cantidad de objetos UART para crear. Correspondiendo entonces serialid al numero de UART usado en el microcontrolador.  Para más información de UART con uPy: [UART MicroPython](https://docs.micropython.org/en/latest/library/machine.UART.html)

### Nota

A pesar de que para controlar el motor se puede utilizar la configuracion de [UART to 1-WIRE interface](https://hackaday.com/2015/01/29/easier-uart-to-1-wire-interface/), para tener un sistema más robusto se ha utilizado lo siguiente [Robotis TTL Communication](http://emanual.robotis.com/docs/en/dxl/x/xl320/#ttl-communication). Para esta es necesario especificar la dirección en que se envian datos. Para lo cual en la clase `xl320()`se especifica un pin de dirección con el cual poder manejar si se envia o se recibe datos al ESP, lo cual es sumamente necesario para la lectura.

## Video


## `AX12.PY`
 This is the core script that allows the use of Dynamixel Servos with MicroPython. In it a class called `ax12` has been defined with its respective constructor and methods. How to use it is specified below.


### UART-To-1Wire

![UART to 1-Wire](https://hackaday.com/wp-content/uploads/2015/01/onewire.png?w=800)

### Constructor

~~~~ python
ax12(self, dir_com, baudrate=1000000, serialid=2)
~~~~

* dir_com: debido a la interface de UART-1Wire, para prevenir el fallo de lectura se utiliza un pin que especifica en que dirección se transmiten los datos, que es especificado con esta variable, que basicamente representa el pin con el que se manejara la dirección.
* baudrate: define los baudios con el cual se utilizará el motor
* serialid: define que pines tx, rx del ESP se usaran, por default UART(2)
Tener en cuenta que hay valores especificados como default en el constructor de la clase, por lo que si se quiere unos distintos, este debe ser especficado. Además se permite la creación de distintos objetos para el uso de motores, en el caso del ESP32 se permite hasta 3 lineas de motores. Para el ESP8266 tan solo 2. Con linea de motores, se refiere a motores conectados en serie en distintos buses.

#### Ejemplo de inicialización de objeto

~~~~ python
from ax12 import *
dxl=ax12(dir_com=22) #dir_com=22 es la
~~~~

Si se desea especificar el baudrate o el serial uart a usar:
~~~~ python
from ax12 import *
dxl=ax12(dir_com=22,baudrate=15200,serialid=1)
~~~~

### Métodos
Para la clase se han creado una serie de metodos especificos para su uso. En los cuales se usan funciones encontradas en el mismo script. Como le() y makePacket().

Los metodos especificos, son para el control sobre el ID, baudrate, goal speed, present speed, etc. Pero también se agrego un metodo llamado sendPacket() el cual es un método genérico, este es más detallado en la próxima sección.
#### Genéricos
##### sendPacket()
Este metodo del objeto, esta principalmente para poder enviar por UART, un paquete propio creado.
Para la creación de un paquete se puede usar el metodo de `makePacket(ID, instr, reg=None, params=None)`, el cual regresa un array con los valores a enviar por serial.
###### Ejemplo
~~~~ python
from ax12 import *
dxl=ax12(dir_com=22)
#cambio de id, de 1 a 2
pkt=makePacket(1,WRITE,XL320_ID,[2])
~~~~
Tener en cuenta que en el ejemplo anterior, se hace un cambio de id, el cual es un registro al cual le corresponde 1 byte, por lo que en el metodo basta con poner como parametro [2], mientras que si este fuera de 2 bytes, se tendria que usar el metodo le() que se encuentra en el mismo script. Basicamente el metodo le() se encarga de representar un numero mayor a 255 en dos bytes.
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

