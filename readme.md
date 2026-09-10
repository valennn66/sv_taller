# Tasks API

 **Métodos**:

- GET: Sirve para consultar la lista completa de tareas /tasks o una puntual mediante una id /tasks/id

- POST: Permite añadir una nueva tarea recibiendo los datos en el cuerpo de esta, le asigna una id única con next_id y la guarda en la lista

- PATCH: Permite modificar parcialmente una tarea ya existente

- DELETE: Permite borrar una tarea de la lista correspondiente al ID solicitado 

## Por qué POST no es idempotente?
Que un método sea idempotente significa que ejecutarlo sin importar la cantidad de veces dara el mismo resultado, POST no puede ser idempotente porque aunque el cuerpo sea el mismo se creara una entrada nueva con la siguente ID