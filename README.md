# RobotAjedrecista

# Requerimientos 
Previo a comenzar con la instalación, se deberían cumplir los siguientes requerimientos:
 * Tener Python 3.8 y PIP instalados.
 * Una cámara web que se pueda conectar a la computadora.
 * Cobot UR5e.
# Pasos
Una vez cumplidos los requerimientos, se puede continuar con la instalación:
## Instalación 
 1. Clonar el repositorio.
 2. __Instalar dependencias__: en consola, utilizar el siguiente comando `pip install -r requirments.txt` para instalar las dependencias
 3. __Corrección de dependencia del gripper__: hay un error en la dependencia que impide el funcionamiento correcto del programa. Para corregirla:
  * Entrar al archivo robotiq_two_finger_gripper.py
  * Dentro del método _get_new_urscript(self) eliminar siguiente línea: `urscript._set_robot_activate()`
## Configuración del robot
 1. Prender el robot, activar el gripper y dejarlo en modo remoto. 
 2. Revisar que el robot esté conectado al router.
 3. Conectar la computadora al router mediante un cable ethernet.
## Set up del ambiente
 1. Ubicar tablero de ajedrez cerca del robot
 2. Colocar la camera encima del tablero, lo mas centrado posible. Asegurarse que se pueda ver todo el tablero en la camara
 3. Colocar todas las piezas en sus lugares correspondientes
## Ejecución
Una vez que esté todo preparado, se pueden correr los siguientes archivos:
 - __calibracion.py__ : Calibrar la camara
 - __main.py__ : Ejecutar 
 