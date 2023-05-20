# Garnotes - Aplicación web para la administración de notas
## Descripción
Proyecto realizado para la asignatura Administración de Sistemas. Es una aplicación web basada en Flask, que utiliza 3 servicios distintos: una imagen personalizada que funciona como aplicación web, una imagen de LDAP para la autenticación de usuarios y una imagen de CrateDB para el almacenamiento de notas.
## Requisitos
Docker Compose
## Ejecución
- Clonar el repositorio en el equipo: ```$ git clone \<URL del repositorio> ```
- Moverse dentro de la carpeta clonada: ```$ cd \<nombre del repositorio>```
- Ejecutar el script cambioMemoria.sh para incrementar la memoria virtual: ```$ ./cambioMemoria.sh```
- Hacer docker compose up: ```$ docker compose up```
