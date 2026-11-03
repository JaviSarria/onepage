# Navegación jerárquica en el índice de la tercera columna

## Objetivo

En las páginas de evolutivos e incidencias, el índice «En esta página» muestra
inicialmente solo las secciones de nivel superior. Los nodos con hijos ofrecen
un control accesible para expandirlos o contraerlos, separado del título, que
sigue navegando a la ubicación. Al enfocar un campo en el documento, el índice
revela la ruta jerárquica de sus ancestros.

## Contexto

- Disposición de pantalla: izquierda (árbol de proyectos), centro (documento,
  columna principal) y derecha (índice de la página actual).
- La tercera columna renderiza `ArbolContenido.vue` a partir de `indice` construido
  por `toc.js` (`construirIndice`).
- El estado de apertura vive en `store/acordeon.js` (claves tipo
  `doc/requerimiento/resumen`, `doc/analisis/tareas/3`).

## Alcance

- [x] Mostrar inicialmente solo los nodos raíz y expandir o contraer nodos con hijos.
- [x] Mantener separado el control de expansión de la navegación del título.
- [x] Expandir los ancestros del campo actualmente enfocado, incluidos nodos anidados.
- [x] Reiniciar las expansiones manuales al seleccionar otro documento.
- [x] Limpiar la clave de foco al cambiar de documento y conservar la ruta indicada por un resultado de búsqueda.
- [x] Verificación (build frontend): `npm run build` en `onepage-fe` finalizó correctamente.

## Criterios de aceptación

- La tercera columna muestra inicialmente las secciones raíz y oculta sus hijos.
- Los nodos con hijos muestran `+`; al activarlo, muestran `−` y revelan sus hijos.
- Los nodos hoja no tienen control de expansión; el título navega a su ubicación.
- Al enfocar un campo concreto de la columna principal, la tercera columna
  muestra toda la ruta de apartados y subapartados que lo contiene.
- Al seleccionar otro documento, el índice vuelve a mostrar solo los nodos raíz.
- Al abrir un resultado de búsqueda, el índice conserva la ruta de `saltarA` del resultado.
- No se exponen credenciales ni secrets en el flujo.

## Estado

- [x] Implementado
- [x] Verificado

## Corrección de seguimiento

La expansión requerida por el foco se determina por la clave registrada desde el
campo enfocado, no por las secciones abiertas en el documento. La expansión
manual se conserva separada de la navegación y se reinicia al cambiar la clave
del documento del árbol. La clave de foco también se limpia al cambiar de
documento, excepto cuando la selección procede de un resultado de búsqueda, que
restablece explícitamente la clave de destino.

Commit de la corrección: `8ba547b`.
