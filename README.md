# Garnotes - Aplicación web para la administración de notas
## Descripción
Proyecto realizado para la asignatura Administración de Sistemas. Es una aplicación web basada en Flask, que utiliza 3 servicios distintos: una imagen personalizada que funciona como aplicación web, una imagen de LDAP para la autenticación de usuarios y una imagen de CrateDB para el almacenamiento de notas.
## Requisitos
Docker Compose
## Ejecución
- Clonar el repositorio en el equipo: ```$ git clone <URL del repositorio> ```
- Moverse dentro de la carpeta clonada: ```$ cd <nombre del repositorio>```
- Ejecutar el script cambioMemoria.sh para incrementar la memoria virtual necesaria para ejecutar CrateDB: ```$ ./cambioMemoria.sh```
- Hacer docker compose up: ```$ docker compose up```
## Funcionamiento
La aplicación está desarrollada en el Framework Flask y tiene un Login y un Registro accesible para cualquier usuario, en el que al iniciar sesión o registrarse la aplicación se conecta con el servidor LDAP creado e inserta o consulta, en función de lo elegido por el usuario, en la unidad organizativa "usuarios" (ou=usuarios) de "garnotes.com" (dc=garnotes, dc=com).

Una vez ha iniciado sesión el usuario, la aplicación guarda el nombre de usuario en una variable de sesión de Flask y envía a este al apartado de notas, donde esta se conecta con CrateDB y selecciona las notas del usuario en función de un identificador basado en el nombre de usuario LDAP. En caso de no coincidir el nombre de usuario y contraseña con un usuario existente aparece un mensaje de error.

Además de ver las notas listadas en orden de nota más antigua a más reciente, el usuario puede añadir sus notas, insertando en CrateDB el texto de esta, junto con el identificador del usuario y la fecha de inserción.

Por último, si el usuario decide cerrar sesión se borra la variable de sesión de Flask y el usuario tendrá que volver a iniciar sesión para poder acceder al apartado de notas, ya que en caso de intentar acceder a notas, la aplicación le reenvía al login.

Cabe destacar, que al lanzar el servidor LDAP, se crea un usuario administrador con nombre de usuario "administrador" y contraseña "admin1234" que puede ver las notas de todos los usuarios, pero no puede insertar ninguna. Este usuario también se encuentra en la unidad organizativa "usuarios" (ou=usuarios) de LDAP.
