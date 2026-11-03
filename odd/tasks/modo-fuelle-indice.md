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

- [ ] Añadir profundidad máxima configurable al estado del acordeón.
- [ ] Filtrar el índice por profundidad, ocultando niveles más allá del máximo.
- [ ] Mostrar la ruta completa (todos los niveles) del campo actual.
- [ ] Control de profundidad en la tercera columna.
- [ ] Verificación (build frontend) y cierre.

## Criterios de aceptación

- Con profundidad por defecto (1) la tercera columna muestra `# Cabecera`,
  `# Requerimiento`, `# Análisis`, ... y oculta subapartados y más.
- Al estar en un campo concreto de la columna principal, la tercera columna
  muestra toda la profundidad de apartados y subapartados hasta ese campo.
- El control de profundidad permite variar el número de niveles mostrados.
- No se exponen credenciales ni secrets en el flujo.

## Estado

- [ ] Implementado
- [ ] Verificado
