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

- [ ] Añadir endpoints de sistema: listar bases, exportar (descargar) y
      restaurar/importar (subida de archivo).
- [ ] Crear la vista de configuración con el apartado de base de datos.
- [ ] Añadir icono de configuración en la zona inferior izquierda, junto al
      icono de cambio de modo.
- [ ] Verificación (build frontend y tests backend) y cierre.

## Criterios de aceptación

- La página de configuración existe y solo muestra el apartado de base de datos
  por ahora.
- Se puede exportar (descargar) cada una de las bases existentes.
- Se puede restaurar/importar una base desde un archivo subido.
- El icono de configuración está junto al icono de tema en la zona inferior
  izquierda.
- Build frontend (`npm run build`) y tests backend pasan.

## Estado

- [ ] Implementado
- [ ] Verificado

## Evidencia de cierre

- Pendiente.
