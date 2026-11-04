# Configuración y gestión de bases de datos

## Objetivo

Añadir una página de configuración con el apartado de base de datos para poder
exportar, importar y hacer copia de seguridad/restaurar las bases de datos del
backend. Por ahora la página solo expone el apartado de base de datos.

## Contexto

- Backend FastAPI con SQLite en `onepage-be/src/onepage_be/config.py`
  (`DATA_DIR`, `evolutivos.sqlite3`, `incidencias.sqlite3`).
- Los routers se registran en `main.py` bajo `/api/<recurso>`.
- Frontend Vue sin router: las vistas se seleccionan por el tipo en `App.vue`
  (proyecto, busqueda, evolutivos, incidencias, diario, configuracion futuro).
- El icono de cambio de tema (claro/oscuro) vive en el footer del panel izquierdo
  (`ArbolProyectos.vue`, `.pie-arbol`).

## Alcance

- [x] Añadir endpoints de sistema: listar bases, exportar (descargar) y
      restaurar/importar (subida de archivo).
- [x] Crear la vista de configuración con el apartado de base de datos.
- [x] Añadir icono de configuración en la zona inferior izquierda, junto al
      icono de cambio de modo.
- [x] Verificación (build frontend y tests backend) y cierre.

## Criterios de aceptación

- La página de configuración existe y solo muestra el apartado de base de datos
  por ahora.
- Se puede exportar (descargar) cada una de las bases existentes.
- Se puede restaurar/importar una base desde un archivo subido.
- El icono de configuración está junto al icono de tema en la zona inferior
  izquierda.
- Build frontend (`npm run build`) y tests backend pasan.

## Estado

- [x] Implementado
- [x] Verificado

## Evidencia de cierre

- Commit de configuración y gestión de bases: `2097576`.
- `npm run build` en `onepage-fe`: correcto (exit code 0).
- Tests backend (`python -m unittest discover -s tests`): OK (7 tests, exit 0).
- La app de FastAPI carga con el nuevo router `/api/sistema` (incluido).
- Se añadió la dependencia `python-multipart` para los endpoints de importación.

## Contexto de implementación

- Nuevo router `onepage-be/src/onepage_be/routers/sistema.py` con
  `GET /api/sistema/bases`, `GET /api/sistema/bases/{nombre}/descargar` y
  `POST /api/sistema/bases/{nombre}/importar`.
- Nueva vista `onepage-fe/src/components/ConfiguracionVista.vue` con el apartado
  de base de datos (exportar todas + restaurar/importar con selector).
- Icono `⚙️` en el footer del panel izquierdo (`ArbolProyectos.vue`), junto al
  toggle de tema (`🌙`/`☀️`).
- `App.vue` gestiona la vista de configuración mediante el tipo
  `configuracion` de la selección.

## Corrección de seguimiento

- Al abrir la vista de configuración, la rama condicional de búsqueda seguía con
  `v-if` y la de documento con `v-else-if`, montando de más la vista de documento
  (`GET /configuracion/undefined/full -> 404`). Se unificó la cadena con
  `v-else-if` en busqueda. Commit: `413d89b`.
