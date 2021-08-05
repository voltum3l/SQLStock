# SQLStock
Pequeño programa de manejo básico de STOCK por SQL

------------------------------------------------------------
Es mi segunda aplicación de python, que empecé a estudiar hace menos de un mes.
La idea es generar un programa con interfase gráfica, que permita el manejo de un stock a través de una BDD.

El programa realiza una gestión básica de stock (agregar elementos de forma manual, por archivo, modificación/eliminación de elementos).
Log de eventos con posibilidad de volcarlo a un archivo .txt.


IMPORTANTE:
El archivo que genera el log es >>> log.txt y se guarda en el directorio donde esté el programa.
El archivo que es necesario para subir inventario tiene que llamarse productos.txt y tiene que tener la siguiente sintaxis:
<var1>,<var2>,<var3>,<var4>,
  var1 -> Marca del elemento (máximo 40 caracteres)
  var2 -> Precio del elemento
  var3 -> Talle del elemento (máximo 3 caracteres)
  var4 -> Cantidad del elemento
  
var1 y var2 son strings.
var3 y var4 son integers.
Es imprescindible poner luego de cada variable y hacer un salto de linea al terminar el ingreso del elemento.
  Ejemplo:
    Adidas,30,S,150,
    Nike,40,L,200,
  
  Esto significaría que se añade el elemento Marca-> Adidas, Precio->30, Talle->S, Cantidad-> 150 y Marca-> Nike, Precio->40, Talle->L, Cantidad->200. 
    



05/08/2021

Version 0.2

* Agregada barra superior indicadora de creación/conexión de BDD (Base de Datos)
* Agregado volcado de log en archivo .txt.
* Agregada función para borrar la base de datos (con confirmación).
  
