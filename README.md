# Elenas test
### Los commits recientes son agregados por la rama master
### Para hacer el despliegue se necesita que la maquina anfitrión tenga instalado y configurado docker y docker-compose
## Clonar repositorio
- git clone https://github.com/softkra/elenas.git
#### *No deberia presentar problemas al momento de clonarlo ya que el repositorio es publico*
## Iniciar despliegue del proyecto mediante docker
- Una vez clonado el repositorio, se ingresa al directorio  'elenas'
- Con `docker-compose up --build -d` se iniciará la construccion de los contenedores docker que estan configurados para trabajar con la version de Python 3.9 y la ultima de Django soportada por la version de python
- Una vez se creen los contenedores se puede hacer seguimiento a los logs con el comando `docker-compose logs -f` y en este apartado nos debe mostrar lo siguiente:
```
django_1  | Watching for file changes with StatReloader
django_1  | Performing system checks...
django_1  | 
django_1  | System check identified no issues (0 silenced).
django_1  | August 25, 2021 - 05:12:35
django_1  | Django version 3.2.6, using settings 'elenas.settings'
django_1  | Starting development server at http://0.0.0.0:8080/
django_1  | Quit the server with CONTROL-C.
```
## Documentación
### Se ha habilitado un módulo de documentación automática de swagger el cual lo pueden encontrar en el endpoint: http://localhost:8080/api/docs/
##### _El código almacenado en este GitHub fue desarrollado por Christian David Porres_
