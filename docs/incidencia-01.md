***

# {Título}

***

| **Estado**            | {`Borrador`; `En análisis`; `En desarrollo`; `En pruebas`; `Listo para desplegar`; `Cerrado`} |
| --------------------- | --------------------------------------------------------------------------------------------- |
| **Responsable**       | {Nombre}                                                                                      |
| **Severidad**         | {`Crítica`; `Alta`; `Media`; `Baja`}                                                          |
| **Prioridad**         | {`Baja`; `Media`; `Alta`}                                                                     |
| **Versión afectada**  | {#.#}                                                                                         |
| **Entorno detección** | {`DEV`; `QA`; `PROD`}                                                                         |
| **Fecha detección**   | {dd/MM/yyyy}                                                                                  |
| **Fecha objetivo**    | {dd/MM/yyyy}                                                                                  |
| **Commits**           | {id-bitbucket-01, ...}                                                                        |
| **Despliegues**       | {id-bamboo-01, ...}                                                                           |
| **Incidencia Jira**   | {id-jira-01}                                                                                  |

## Resumen



## Descripción del problema

> Descripción resumida del comportamiento incorrecto observado

## Impacto

> A quién/qué afecta, alcance del impacto (usuarios, procesos, datos)

## Pasos para reproducir

> Secuencia de pasos que permiten reproducir el problema

## Comportamiento actual

> Qué está ocurriendo

## Comportamiento esperado

> Qué debería ocurrir

## Alcance de la corrección

> Qué se va a corregir con este trabajo

## Fuera de alcance

> Qué no se va a corregir en esta incidencia

## Supuestos y restricciones



## Dependencias

> Dependencias con el resto del sistema

## Riesgos y mitigación

> Cuales son los riesgos al aplicar la corrección, ¿puede afectar a otras funcionalidades?

## Decisiones pendientes

> Temas abiertos pendientes de tratar

## Evidencias iniciales

> Logs, capturas, trazas u otra evidencia que documente el problema

## Criterios de aceptación

| **Id**  | Criterio                          |
| ------- | --------------------------------- |
| {CA-XX} | {Dado..., cuando..., entonces...} |

***

# Análisis

***

## Causa raíz

> Descripción del origen real del problema (root cause analysis)

## Descripción de la solución

> Puntos que describen el análisis realizado

## Tareas

### Tarea XX

| **Id**                     | {TAR-XX}      |
| -------------------------- | ------------- |
| **Criterio de aceptación** | {id-criterio} |
| **Dependencias**           | {TAR-XX, ...} |

#### Diseño de la corrección

> Diagramas y puntos que describen la solución hasta completar la corrección

#### Recursos

##### Repositorio XX

| **Nombre**     | {Nombre_real_repo} |
| -------------- | ------------------ |
| **Subaccount** | {Nombre_subcuenta} |
| **Space**      | {Espacio}          |

##### Servicio XX

#### Problemas

> Si se ha encontrado un problema adicional y sea necesario recordarlo

## Plan de Pruebas

### Casos

#### Caso XX

| **Id**                     | {PRU-XX}      |
| -------------------------- | ------------- |
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
**CAUSA RAÍZ**: {referencia a la causa raíz} (en caso que fuera necesario)

#### Actividades

> pasos para completar la tarea

- [ ] Actividad 1

#### Cambios

##### Objeto XX

| **Nombre**      | {Nombre_objeto(clase/archivo/...)}    |
| --------------- | ------------------------------------- |
| **Ubicación**   | {Ruta_lógica_Paquete}                 |
| **Descripción** | {Descripción del cambio}              |
| **Repositorio** | {Nombre del repositorio}              |
| **Rama**        | {Nombre de la rama en el repositorio} |
| **Commit**      | {id_bitbucket}                        |



***

# Pruebas

***

## Datos para las pruebas

> En caso de que se cuente con una bolsa de datos o datos relacionados, que puedan ser útiles para las pruebas.

## Casos

### Caso XX

| **Id**                       | {PRU-XX}                                   |
| ---------------------------- | ------------------------------------------ |
| **Criterio de aceptación**   | {CA-XX}                                    |
| **Estado**                   | {`OK`; `NOK`; `BLOQUEADA`; `NO EJECUTADA`} |
| **Responsable**              | {nombre}                                   |
| **Incidencias relacionadas** | {Id-jira}                                  |

#### Datos usados para el caso

> Relación de datos usados, **si se puede reseñar algún identificador de los datos de prueba antes de mostrar todos los datos, mejor**.

#### Pasos dados

> Enumeración resumida de los pasos dados para la ejecución del caso.

#### Ejecuciones

| **Fecha**    | **Versión** | **Entorno**             | **Responsable** | **Resultado**                      | **Incidencia** | **Evidencias**              |
| ------------ | ----------- | ----------------------- | --------------- | ---------------------------------- | -------------- | --------------------------- |
| {dd/MM/yyyy} | {#.##}      | {`DEV`; `TEST`; `PROD`} | {nombre}        | {OK; NOK; BLOQUEADA; NO EJECUTADA} | {Id-jira}      | {`C:\evidencias\ev_01.jpg`} |

> El estado del caso corresponde a su última ejecución aplicable.

## Verificación de no regresión

> Casos existentes que se han vuelto a validar para asegurar que la corrección no introduce nuevos problemas



### Caso de regresión XX

| **Id**                       | {PRU-R-XX}                                 |
| ---------------------------- | ------------------------------------------ |
| **Criterio de aceptación**   | {CA-XX}                                    |
| **Estado**                   | {`OK`; `NOK`; `BLOQUEADA`; `NO EJECUTADA`} |
| **Responsable**              | {nombre}                                   |
| **Incidencias relacionadas** | {Id-jira}                                  |

#### Datos usados para el caso

> Relación de datos usados, **si se puede reseñar algún identificador de los datos de prueba antes de mostrar todos los datos, mejor**.

#### Pasos dados

> Enumeración resumida de los pasos dados para la ejecución del caso.

#### Ejecuciones

| **Fecha**    | **Versión** | **Entorno**             | **Responsable** | **Resultado**                      | **Incidencia** | **Evidencias**              |
| ------------ | ----------- | ----------------------- | --------------- | ---------------------------------- | -------------- | --------------------------- |
| {dd/MM/yyyy} | {#.##}      | {`DEV`; `TEST`; `PROD`} | {nombre}        | {OK; NOK; BLOQUEADA; NO EJECUTADA} | {Id-jira}      | {`C:\evidencias\ev_01.jpg`} |

> El estado del caso corresponde a su última ejecución aplicable.



***

# Definition of Done

***

- [ ] Causa raíz identificada y documentada
- [ ] Revisión de código realizada
- [ ] Pruebas requeridas ejecutadas con resultado satisfactorio
- [ ] Pruebas de no regresión ejecutadas
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

- La incidencia pasa a `En análisis` cuando se ha iniciado la investigación de la causa raíz.
- La incidencia pasa a `En desarrollo` cuando hay al menos una tarea `En curso`.
- La incidencia pasa a `En pruebas` cuando las tareas necesarias están `Completadas` o `En revisión`.
- La incidencia pasa a `Listo para desplegar` cuando los casos de prueba obligatorios (incluida la no regresión) tienen resultado `OK`, la cobertura de la matriz está `Validada` o `No aplica` y no existen incidencias derivadas bloqueantes.
- La incidencia pasa a `Cerrado` cuando se completa la Definition of Done y queda registrado el despliegue, si aplica.
- Una tarea `Bloqueada`, un caso de prueba `BLOQUEADA` o una cobertura `Bloqueada` impide avanzar al siguiente estado hasta que se resuelva o se apruebe la excepción.

## Planificación

| **Criterio de aceptación** | **Tarea** | **Responsable** | **Estado**                                                                       | **Estimado** | **Real** | **Inicio**   | **Fin**      | **Bloqueos** |
| -------------------------- | --------- | --------------- | -------------------------------------------------------------------------------- | ------------ | -------- | ------------ | ------------ | ------------ |
| {CA-XX}                    | {TAR-XX}  | {Nombre}        | {`Pendiente`; `En curso`; `Bloqueada`; `En revisión`; `Completada`; `Cancelada`} | {horas}      | {horas}  | {dd/MM/YYYY} | {dd/MM/YYYY} |              |

## Matriz de trazabilidad

| **Criterio aceptación** | **Tarea** | **Prueba** | **Cambios**       | **Estado de cobertura**                                       |
| ----------------------- | --------- | ---------- | ----------------- | ------------------------------------------------------------- |
| {CA-XX}                 | {TAR-XX}  | {PRU-XX}   | {nombre_objeto}   | {`Pendiente`; `Parcial`;`Validada`; `No aplica`; `Bloqueada`} |
| Ejemplo:                |           |            |                   |                                                               |
| **Criterio aceptación** | **Tarea** | **Prueba** | **Cambios**       | **Estado de cobertura**                                       |
| ---                     | ---       | ---        | ---               | ---                                                           |
| CA-01                   | TAR-01    | PRU-01     | Servicio.class    | `Pendiente`                                                   |
| CA-02                   | TAR-01    | PRU-01     | Servicio.class    | `Validada`                                                    |
| CA-01                   | TAR-02    | PRU-02     | Controlador.class | `Pendiente`                                                   |
| CA-02                   | TAR-02    | PRU-02     | Controlador.class | `Pendiente`                                                   |

## dd/MM/YYYY

**TIEMPO**: {horas}

### Tareas

#### Tarea XX

| **ID** | {ID-TAREA-ASOCIADA} |
| ------ | ------------------- |

##### Actividades

- [ ] Actividad XX
- [ ] Actividad YY

### Notas

> si fuera necesario


