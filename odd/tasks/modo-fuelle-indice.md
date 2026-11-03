# Modo fuelle en la tercera columna (índice de profundidad)

## Objetivo

En las páginas de evolutivos e incidencias, la tercera columna (índice
«En esta página») debe ofrecer un modo de profundidad tipo fuelle: mostrar los
niveles superiores (`# Cabecera`, `# Requerimiento`, `# Análisis`, ...) y ocultar
lo de más. Además, cuando la columna principal está en un campo concreto, la
tercera columna debe mostrar toda la profundidad de apartados y subapartados
donde se encuentra ese campo.

## Contexto

- Disposición de pantalla: izquierda (árbol de proyectos), centro (documento,
  columna principal) y derecha (índice de la página actual).
- La tercera columna renderiza `ArbolContenido.vue` a partir de `indice` construido
  por `toc.js` (`construirIndice`).
- El estado de apertura vive en `store/acordeon.js` (claves tipo
  `doc/requerimiento/resumen`, `doc/analisis/tareas/3`).

## Alcance

- [x] Añadir profundidad máxima configurable al estado del acordeón.
- [x] Filtrar el índice por profundidad, ocultando niveles más allá del máximo.
- [x] Mostrar la ruta completa (todos los niveles) del campo actualmente enfocado.
- [x] Control de profundidad en la tercera columna.
- [x] Verificación (build frontend): `npm run build` en `onepage-fe` finalizó correctamente.

## Criterios de aceptación

- Con profundidad por defecto (1) la tercera columna muestra `# Cabecera`,
  `# Requerimiento`, `# Análisis`, ... y oculta subapartados y más.
- Al enfocar un campo concreto de la columna principal, la tercera columna
  muestra toda la ruta de apartados y subapartados que lo contiene.
- El control de profundidad permite variar el número de niveles mostrados.
- No se exponen credenciales ni secrets en el flujo.

## Estado

- [x] Implementado
- [x] Verificado

## Corrección de seguimiento

La primera implementación intentaba deducir el campo actual mediante el acordeón
más profundo abierto, lo que no era fiable porque al cargar se abren varias
secciones con contenido. Ahora la columna principal registra el foco y el índice
mantiene la ruta de ancestros del acordeón que contiene el control enfocado.
También se confirmó que Vite sirve los cambios actuales desde `127.0.0.1:5173`.

Commit de la corrección: `8ba547b`.
