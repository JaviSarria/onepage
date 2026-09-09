# {Título}

***

| **Estado**         | {`Borrador`; `En análisis`; `En desarrollo`; `En pruebas`; `Listo para desplegar`; `Cerrado`} |
| ------------------ | --------------------------------------------------------------------------------------------- |
| **Responsable**    | {Nombre}                                                                                      |
| **Prioridad**      | {`Baja`; `Media`; `Alta`}                                                                     |
| **Versión**        | {#.#}                                                                                         |
| **Fecha objetivo** | {dd/MM/yyyy}                                                                                  |
| **Commits**        | {id-bitbucket-01, ...}                                                                        |
| **Despliegues**    | {id-bamboo-01, ...}                                                                           |
| **Incidencias**    | {id-jira-01, ...}                                                                             |

***

# SM300

***

## Resumen

## Descripción del requerimiento

> Descripción resumida del documento

## Objetivo

> Objetivo que persigue el desarrollo del evolutivo

## Alcance

> Qué funcionalidad cubre este evolutivo

## Fuera de alcance

> Qué funcionalidad no va a cubrir

## Supuestos y restricciones

## Dependencias

> Dependencias con el resto del sistema

## Riesgos y mitigación

> Cuales son los riesgos en el desarrollo, ¿algo no está bien planteado?

## Decisiones pendientes

> Temas abiertos pendientes de tratar

## Requisitos

> Indicar los puntos del SM300 en el que se basan los requisitos

### Grupo de requisito A

| **Id**   | **Requisito** |
| -------- | ------------- |
| {REQ-01} | {detalle}     |

## Criterios de aceptación

| **Id**  | Requisito | Criterio                          |
| ------- | --------- | --------------------------------- |
| {CA-XX} | {REQ-YY}  | {Dado..., cuando..., entonces...} |

## Tareas planificadas (si se manda excel)

> La lista de tareas planificadas que acompaña al documento, normalmente una excel.

***

# Análisis

***

## Descripción de la solución

> Puntos que describen el evolutivo

## Repositorios

| Nombre             |
| ------------------ |
| {Nombre_real_repo} |

## Tareas

> Tareas de Backend

### Tarea XX

{Descripción}

| **Id**           | {TAR-XX}       |
| ---------------- | -------------- |
| **Requisito**    | {id-requisito} |
| **Dependencias** | {TAR-XX, ...}  |

#### Diseño

> Diagramas y puntos que describen la tarea hasta completar el requerimiento

#### Recursos dependientes

##### Base de datos

> Si usa tablas de base de datos

##### Servicio XX

> Listado de servicios (externos) usados para completar la tarea

#### Problemas

> Si se ha encontrado un problema y sea necesario recordarlo

## Plan de Pruebas

### Casos

#### Caso XX

| **Id**                     | {PRU-XX}      |
| -------------------------- | ------------- |
| **Requisito**              | {REQ-XX}      |
| **Criterio de aceptación** | {CA-XX}       |
| **Nombre**                 | {Nombre_caso} |

##### PRECONDICIONES

> listado de condiciones previas a la prueba

##### Datos de la prueba

##### Pasos

> listado de pasos a dar

##### Resultado esperado

> Valor esperado de la prueba según los datos aportados

***

# Desarrollo

***

## Tareas desarrolladas

### Tarea XX

**ID**: {id-tarea-analisis}
**REQUISITO**: {id}

- [ ] Actividad 1 

#### Cambios

##### Objeto XX

| **Nombre**      | {Nombre_objeto(clase/archivo/...)} |
| --------------- | ---------------------------------- |
| **Ubicación**   | {Ruta_lógica_Paquete}              |
| **Descripción** | {Descripción del cambio}           |
| **Commit**      | {id_bitbucket}                     |

***

# Pruebas

***

## Datos para las pruebas

> En caso de que se cuente con una bolsa de datos o datos relacionados, que puedan ser útiles para las pruebas.

## Casos

### Caso XX

| **Id**          | {PRU-XX}                                   |
| --------------- | ------------------------------------------ |
| **Requisito**   | {REQ-XX}                                   |
| **Estado**      | {`OK`; `NOK`; `BLOQUEADA`; `NO EJECUTADA`} |
| **Responsable** | {nombre}                                   |
| **Incidencias** | {Id-jira}                                  |

#### Ejecuciones

| **Fecha**    | **Versión** | **Entorno**             | **Responsable** | **Resultado**                      | **Incidencia** | **Evidencias**              |
| ------------ | ----------- | ----------------------- | --------------- | ---------------------------------- | -------------- | --------------------------- |
| {dd/MM/yyyy} | {#.##}      | {`DEV`; `TEST`; `PROD`} | {nombre}        | {OK; NOK; BLOQUEADA; NO EJECUTADA} | {Id-jira       | {`C:\evidencias\ev_01.jpg`} |

> El estado del caso corresponde a su última ejecución aplicable.

***

# Definition of Done

***

- [ ] Revisión de código realizada
- [ ] Pruebas requeridas ejecutadas con resultado satisfactorio
- [ ] Documentación actualizada
- [ ] Sin defectos bloqueantes abiertos
- [ ] Despliegue validado o marcado como no aplicable
- [ ] Aprobación funcional registrada

***

# Despliegue

***

| Parámetro                         | Valor                  |
| --------------------------------- | ---------------------- |
| **Versión**                       | {version}              |
| **Entorno**                       | {`DEV`; `QA`; `PROD`}  |
| **Fecha-hora**                    | {dd/MM/yyyy HH:mm}     |
| **Responsable**                   | {nombre}               |
| **Commits**                       | {Id_bitbucket-01, ...} |
| **URL Pipeline Bamboo**           | {pipeline_despliegue}  |
| **Validación post-despliegue**    | {acciones}             |
| **Resultado**                     | {texto}                |
| **Plan de reversión / No aplica** | {plan}                 |

## MODULOS AFECTADOS

> servidores, bases de datos, apps, etc...

### Repositorios

| Nombre             | Subaccount         | Space     |
| ------------------ | ------------------ | --------- |
| {Nombre_real_repo} | {Nombre_subcuenta} | {Espacio} |

### Bases de datos

| Repositorio | Nombre      | Tabla          | Campos         |
| ----------- | ----------- | -------------- | -------------- |
| IPOPENPO071 | {Nombre_DB} | {Nombre_Tabla} | {Nombre_campo} |

## MIGRACIÓN DE DATOS

> En caso de ser necesario

***

# Reuniones

***

## dd/MM/YYYY

**Participantes**: {`Participante-1`, ...}
**Objetivo**: `Objetivo de la reunión`

### Decisiones

> Listado de las decisiones que se toman

### Acciones

> Acciones o tareas habladas que hay que realizar. Indicar el responsable y fecha objetivo
> | **Acciones** | **Responsable** | **Fecha Objetivo** |
> |---|---|---|
> | {descripción} | {nombre} | {dd/MM/yyyy} |

***

# Seguimiento

***

## Convención de estados

- El evolutivo pasa a `En análisis` cuando se ha iniciado el diseño de al menos una tarea.
- El evolutivo pasa a `En desarrollo` cuando hay al menos una tarea `En curso`.
- El evolutivo pasa a `En pruebas` cuando las tareas necesarias están `Completadas` o `En revisión`.
- El evolutivo pasa a `Listo para desplegar` cuando los casos de prueba obligatorios tienen resultado `OK`, la cobertura de la matriz está `Validada` o `No aplica` y no existen incidencias bloqueantes.
- El evolutivo pasa a `Cerrado` cuando se completa la Definition of Done y queda registrado el despliegue, si aplica.
- Una tarea `Bloqueada`, un caso de prueba `BLOQUEADA` o una cobertura `Bloqueada` impide avanzar al siguiente estado hasta que se resuelva o se apruebe la excepción.

## Planificación

| **Requisito** | **Tarea** | **Responsable** | **Estado**                                                                       | **Estimado** | **Real** | **Inicio**   | **Fin**      | **Bloqueos** |
| ------------- | --------- | --------------- | -------------------------------------------------------------------------------- | ------------ | -------- | ------------ | ------------ | ------------ |
| {REQ-XX}      | {TAR-XX}  | {Nombre}        | {`Pendiente`; `En curso`; `Bloqueada`; `En revisión`; `Completada`; `Cancelada`} | {horas}      | {horas}  | {dd/MM/YYYY} | {dd/MM/YYYY} |              |

## Matriz de trazabilidad

| **Requisito** | **Criterio aceptación** | **Tarea** | **Prueba** | **Cambios**       | **Estado de cobertura**                                       |
| ------------- | ----------------------- | --------- | ---------- | ----------------- | ------------------------------------------------------------- |
| {REQ-XX}      | {CA-XX}                 | {TAR-XX}  | {PRU-XX}   | {nombre_objeto}   | {`Pendiente`; `Parcial`;`Validada`; `No aplica`; `Bloqueada`} |
| Ejemplo:      |                         |           |            |                   |                                                               |
| **Requisito** | **Criterio aceptación** | **Tarea** | **Prueba** | **Cambios**       | **Estado de cobertura**                                       |
| ---           | ---                     | ---       | ---        | ---               | ---                                                           |
| REQ-01        | CA-01                   | TAR-01    | PRU-01     | Servicio.class    | `Pendiente`                                                   |
| REQ-01        | CA-02                   | TAR-01    | PRU-01     | Servicio.class    | `Validada`                                                    |
| REQ-01        | CA-01                   | TAR-02    | PRU-02     | Controlador.class | `Pendiente`                                                   |
| REQ-01        | CA-02                   | TAR-02    | PRU-02     | Controlador.class | `Pendiente`                                                   |

## dd/MM/YYYY

**TIEMPO**: {horas}

### Tareas

#### Tarea XX

| **ID** | {ID-Tarea-Asociada} |
| ------ | ------------------- |

##### Actividades

- [ ] Actividad XX
- [ ] Actividad YY

### Notas

> si fuera necesario
