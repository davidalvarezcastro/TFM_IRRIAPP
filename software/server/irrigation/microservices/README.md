# Microservicios

En este directorio se encuentran los microservicios principales que gestiona la aplicación de gestión de controladores.

- Servicio de recogida de estado de los sensores de los diferentes controladores y almacenamiento en el histórico de datos.
- Servicio de monitorización para llevar a cabo la acción de los diferentes actuadores teniendo en cuenta el tipo de zona. Por ejemplo, en las zonas que sean de tipo `regar` (principal ámbito de aplicación del prototipo), este servicio monitorizará el estado del cultivo a partir de los datos de los sensores para activar o desactivar el relé de riego (de ahí el nombre del proyecto).
