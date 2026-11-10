// Esquema declarativo de las secciones de cada tipo de documento.
// Refleja la estructura de las plantillas markdown de la carpeta docs.

export const ESTADOS_DOC = [
  'Borrador',
  'En análisis',
  'En desarrollo',
  'En pruebas',
  'Listo para desplegar',
  'Cerrado'
]
export const PRIORIDADES = ['Baja', 'Media', 'Alta']
export const SEVERIDADES = ['Crítica', 'Alta', 'Media', 'Baja']
export const ENTORNOS = ['DEV', 'QA', 'TEST', 'PROD']
export const ESTADOS_TAREA = [
  'Pendiente',
  'En curso',
  'Bloqueada',
  'En revisión',
  'Completada',
  'Cancelada'
]
export const RESULTADOS_PRUEBA = ['OK', 'NOK', 'BLOQUEADA', 'NO EJECUTADA']
export const COBERTURAS = ['Pendiente', 'Parcial', 'Validada', 'No aplica', 'Bloqueada']
export const TIPOS_RECURSO = ['base_datos', 'servicio']

// Colores por id de sección: secciones homónimas comparten color en evolutivos e incidencias.
export const COLORES_SECCION = {
  cabecera: { fondo: '#f6f8fa', borde: '#afb8c1' },
  requerimiento: { fondo: '#ddf4ff', borde: '#54aeff' },
  problema: { fondo: '#ffebe9', borde: '#ff8182' },
  analisis: { fondo: '#fbefff', borde: '#c297ff' },
  desarrollo: { fondo: '#dafbe1', borde: '#4ac26b' },
  pruebas: { fondo: '#fff1e5', borde: '#fb8f44' },
  dod: { fondo: '#fff8c5', borde: '#d4a72c' },
  despliegue: { fondo: '#d8f5f3', borde: '#3fb8af' },
  reuniones: { fondo: '#ffeff7', borde: '#ff80c8' },
  seguimiento: { fondo: '#eef0ff', borde: '#8c95ff' }
}

const texto = (id, titulo, campo, ayuda = '') => ({ tipo: 'texto', id, titulo, campo, ayuda })

export const etiquetaOrigen = (e) => [e.codigo, e.nombre].filter(Boolean).join(' — ')

// Título de una entidad enlazada a otra del documento a través de `campo` (p. ej. tarea_id).
function tituloOrigen(item, campo, origenes = [], porDefecto = '') {
  const origen = origenes.find((candidato) => candidato.id === item[campo])
  return origen ? etiquetaOrigen(origen) || `#${origen.id}` : porDefecto
}

const casosPlan = {
  tipo: 'entidades',
  id: 'casos-plan',
  titulo: 'Plan de pruebas',
  recurso: 'casos-plan',
  etiqueta: 'caso',
  clave: (c) => etiquetaOrigen(c) || 'Caso',
  campos: [
    { campo: 'codigo', etiqueta: 'Id', ancho: 'codigo' },
    { campo: 'nombre', etiqueta: 'Nombre' },
    { campo: 'criterio_codigo', etiqueta: 'Criterio de aceptación' }
  ],
  textos: [
    { campo: 'precondiciones', titulo: 'Precondiciones' },
    { campo: 'pasos', titulo: 'Pasos' },
    { campo: 'resultado_esperado', titulo: 'Resultado esperado' }
  ],
  hijos: []
}

const origenCasoPlan = {
  campo: 'caso_plan_id',
  recurso: 'casos-plan',
  mensaje: 'Para añadir un caso de prueba, da de alta antes un caso en Análisis › Plan de pruebas'
}
const campoCasoPlan = { campo: 'caso_plan_id', etiqueta: 'Caso del plan', control: 'select-origen' }

const ejecuciones = {
  tipo: 'tabla',
  id: 'ejecuciones',
  titulo: 'Ejecuciones',
  recurso: 'ejecuciones',
  rutaPadre: 'casos-prueba',
  columnas: [
    { campo: 'fecha', etiqueta: 'Fecha' },
    { campo: 'version', etiqueta: 'Versión' },
    { campo: 'entorno', etiqueta: 'Entorno', control: 'select', opciones: ENTORNOS },
    { campo: 'responsable', etiqueta: 'Responsable' },
    { campo: 'resultado', etiqueta: 'Resultado', control: 'select', opciones: RESULTADOS_PRUEBA },
    { campo: 'incidencia', etiqueta: 'Incidencia' },
    { campo: 'evidencias', etiqueta: 'Evidencias', control: 'area' }
  ]
}

const accionesReunion = {
  tipo: 'tabla',
  id: 'acciones',
  titulo: 'Acciones',
  recurso: 'acciones',
  rutaPadre: 'reuniones',
  columnas: [
    { campo: 'descripcion', etiqueta: 'Acción' },
    { campo: 'responsable', etiqueta: 'Responsable' },
    { campo: 'fecha_objetivo', etiqueta: 'Fecha objetivo' }
  ]
}

const tareasSeguimiento = {
  tipo: 'entidades',
  id: 'tareas-seguimiento',
  titulo: 'Tareas del día',
  recurso: 'tareas-seguimiento',
  rutaPadre: 'seguimientos',
  etiqueta: 'tarea',
  clave: (t) => t.nombre || t.tarea_codigo || 'Tarea',
  campos: [{ campo: 'nombre', etiqueta: 'Nombre' }],
  textos: [{ campo: 'descripcion', titulo: 'Descripción' }],
  camposFinales: [{ campo: 'completada', etiqueta: 'Terminado', control: 'check' }],
  hijos: []
}

const seguimientos = {
  tipo: 'entidades',
  id: 'seguimientos',
  titulo: 'Partes de seguimiento',
  recurso: 'seguimientos',
  etiqueta: 'parte',
  clave: (s) => s.fecha || 'Parte',
  campos: [
    { campo: 'fecha', etiqueta: 'Fecha' },
    { campo: 'tiempo', etiqueta: 'Tiempo (h)', control: 'numero' }
  ],
  textos: [],
  hijos: [
    tareasSeguimiento,
    { tipo: 'texto', id: 'notas', titulo: 'Notas', campo: 'notas', recurso: 'seguimientos' }
  ]
}

const reuniones = {
  tipo: 'entidades',
  id: 'reuniones',
  titulo: 'Reuniones',
  recurso: 'reuniones',
  etiqueta: 'reunión',
  clave: (r) => r.fecha || 'Reunión',
  campos: [
    { campo: 'fecha', etiqueta: 'Fecha' },
    { campo: 'participantes', etiqueta: 'Participantes' },
    { campo: 'objetivo', etiqueta: 'Objetivo' }
  ],
  textos: [
    { campo: 'decisiones', titulo: 'Decisiones' },
    { campo: 'notas', titulo: 'Notas' }
  ],
  hijos: [accionesReunion]
}

const cambiosDesarrollo = {
  tipo: 'entidades',
  id: 'cambios-desarrollo',
  titulo: 'Cambios',
  recurso: 'cambios-desarrollo',
  rutaPadre: 'tareas-desarrollo',
  etiqueta: 'cambio',
  clave: (c) => c.nombre || 'Cambio',
  campos: [
    { campo: 'nombre', etiqueta: 'Objeto' },
    { campo: 'ubicacion', etiqueta: 'Ubicación' },
    { campo: 'repositorio', etiqueta: 'Repositorio' },
    { campo: 'rama', etiqueta: 'Rama' },
    { campo: 'commit', etiqueta: 'Commit' }
  ],
  textos: [{ campo: 'descripcion', titulo: 'Descripción' }],
  hijos: []
}

const desarrollo = {
  id: 'desarrollo',
  titulo: 'Desarrollo',
  hijos: [
    {
      tipo: 'entidades',
      id: 'tareas-desarrollo',
      titulo: 'Tareas desarrolladas',
      recurso: 'tareas-desarrollo',
      etiqueta: 'tarea desarrollada',
      clave: (t, doc) => tituloOrigen(t, 'tarea_id', doc?.tareas, 'Tarea desarrollada'),
      origen: {
        campo: 'tarea_id',
        recurso: 'tareas',
        mensaje: 'Para añadir una tarea desarrollada, da de alta antes una tarea en Análisis'
      },
      campos: [
        { campo: 'tarea_id', etiqueta: 'Id tarea de Análisis', control: 'select-origen' },
        { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_TAREA }
      ],
      textos: [],
      hijos: [
        {
          tipo: 'checklist',
          id: 'actividades-desarrollo',
          titulo: 'Actividades',
          recurso: 'actividades-desarrollo',
          rutaPadre: 'tareas-desarrollo',
          campo: 'descripcion',
          check: 'completada'
        },
        cambiosDesarrollo
      ]
    }
  ]
}

const recursosTarea = {
  tipo: 'tabla',
  id: 'recursos',
  titulo: 'Recursos dependientes',
  recurso: 'recursos',
  rutaPadre: 'tareas',
  columnas: [
    { campo: 'tipo', etiqueta: 'Tipo', control: 'select', opciones: TIPOS_RECURSO },
    { campo: 'nombre', etiqueta: 'Nombre' },
    { campo: 'detalle', etiqueta: 'Detalle' }
  ]
}

const actividadesTarea = {
  tipo: 'checklist',
  id: 'actividades',
  titulo: 'Actividades',
  recurso: 'actividades',
  rutaPadre: 'tareas',
  campo: 'descripcion',
  check: 'completada'
}

const repositorios = {
  tipo: 'tabla',
  id: 'repositorios',
  titulo: 'Repositorios',
  recurso: 'repositorios',
  columnas: [
    { campo: 'nombre', etiqueta: 'Nombre' },
    { campo: 'subaccount', etiqueta: 'Subaccount' },
    { campo: 'space', etiqueta: 'Space' }
  ]
}

const despliegue = (extra = []) => ({
  id: 'despliegue',
  titulo: 'Despliegue',
  hijos: [
    {
      tipo: 'tabla',
      id: 'registros-despliegue',
      titulo: 'Registros de despliegue',
      recurso: 'registros-despliegue',
      columnas: [
        { campo: 'version', etiqueta: 'Versión' },
        { campo: 'entorno', etiqueta: 'Entorno', control: 'select', opciones: ENTORNOS },
        { campo: 'fecha_hora', etiqueta: 'Fecha-hora' },
        { campo: 'responsable', etiqueta: 'Responsable' },
        { campo: 'commits', etiqueta: 'Commits' },
        { campo: 'url_pipeline', etiqueta: 'URL Pipeline' },
        { campo: 'validacion_post', etiqueta: 'Validación post-despliegue' },
        { campo: 'resultado', etiqueta: 'Resultado' },
        { campo: 'plan_reversion', etiqueta: 'Plan de reversión' }
      ]
    },
    texto('modulos_afectados', 'Módulos afectados', 'modulos_afectados'),
    ...extra,
    {
      tipo: 'tabla',
      id: 'bases-datos',
      titulo: 'Bases de datos',
      recurso: 'bases-datos',
      columnas: [
        { campo: 'repositorio', etiqueta: 'Repositorio' },
        { campo: 'nombre', etiqueta: 'Nombre' },
        { campo: 'tabla', etiqueta: 'Tabla' },
        { campo: 'campos', etiqueta: 'Campos' }
      ]
    },
    texto('migracion_datos', 'Migración de datos', 'migracion_datos')
  ]
})

const dod = {
  id: 'dod',
  titulo: 'Definition of Done',
  hijos: [
    {
      tipo: 'checklist',
      id: 'definition-of-done',
      titulo: 'Checklist',
      recurso: 'definition-of-done',
      campo: 'descripcion',
      check: 'completado'
    }
  ]
}

export const ESQUEMA_EVOLUTIVO = {
  tipo: 'evolutivos',
  etiqueta: 'Evolutivo',
  cabecera: [
    { campo: 'codigo', etiqueta: 'Código' },
    { campo: 'titulo', etiqueta: 'Título' },
    { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_DOC },
    { campo: 'responsable', etiqueta: 'Responsable' },
    { campo: 'prioridad', etiqueta: 'Prioridad', control: 'select', opciones: PRIORIDADES },
    { campo: 'version', etiqueta: 'Versión' },
    { campo: 'fecha_objetivo', etiqueta: 'Fecha objetivo' },
    { campo: 'referencia_normativa', etiqueta: 'Referencia (SM300)' },
    { campo: 'commits', etiqueta: 'Commits' },
    { campo: 'despliegues', etiqueta: 'Despliegues' },
    { campo: 'incidencias', etiqueta: 'Incidencias' }
  ],
  secciones: [
    {
      id: 'requerimiento',
      titulo: 'Requerimiento',
      hijos: [
        texto('resumen', 'Resumen', 'resumen'),
        texto(
          'descripcion_requerimiento',
          'Descripción del requerimiento',
          'descripcion_requerimiento'
        ),
        texto('objetivo', 'Objetivo', 'objetivo'),
        texto('alcance', 'Alcance', 'alcance'),
        texto('fuera_alcance', 'Fuera de alcance', 'fuera_alcance'),
        texto('supuestos_restricciones', 'Supuestos y restricciones', 'supuestos_restricciones'),
        texto('dependencias', 'Dependencias', 'dependencias'),
        texto('riesgos_mitigacion', 'Riesgos y mitigación', 'riesgos_mitigacion'),
        texto('decisiones_pendientes', 'Decisiones pendientes', 'decisiones_pendientes'),
        {
          tipo: 'tabla',
          id: 'grupos-requisito',
          titulo: 'Grupos de requisito',
          recurso: 'grupos-requisito',
          columnas: [{ campo: 'nombre', etiqueta: 'Grupo' }]
        },
        {
          tipo: 'tabla',
          id: 'requisitos',
          titulo: 'Requisitos',
          recurso: 'requisitos',
          columnas: [
            { campo: 'grupo_id', etiqueta: 'Grupo', control: 'select-dinamico' },
            { campo: 'codigo', etiqueta: 'Id', ancho: 'codigo' },
            { campo: 'detalle', etiqueta: 'Requisito', control: 'area' }
          ]
        },
        {
          tipo: 'tabla',
          id: 'criterios',
          titulo: 'Criterios de aceptación',
          recurso: 'criterios',
          columnas: [
            { campo: 'codigo', etiqueta: 'Id', ancho: 'codigo' },
            { campo: 'requisito_codigo', etiqueta: 'Requisito', ancho: 'codigo' },
            { campo: 'criterio', etiqueta: 'Criterio', control: 'area' }
          ]
        },
        texto('tareas_planificadas', 'Tareas planificadas', 'tareas_planificadas')
      ]
    },
    {
      id: 'analisis',
      titulo: 'Análisis',
      hijos: [
        texto('investigacion_previa', 'Investigación previa', 'investigacion_previa'),
        texto('descripcion_solucion', 'Descripción de la solución', 'descripcion_solucion'),
        repositorios,
        {
          tipo: 'entidades',
          id: 'tareas',
          titulo: 'Tareas',
          recurso: 'tareas',
          etiqueta: 'tarea',
          clave: (t) => [t.codigo, t.nombre].filter(Boolean).join(' — ') || 'Tarea',
          campos: [
            { campo: 'codigo', etiqueta: 'Id' },
            { campo: 'nombre', etiqueta: 'Nombre' },
            { campo: 'requisito_codigo', etiqueta: 'Requisito' },
            { campo: 'dependencias', etiqueta: 'Dependencias' },
            { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_TAREA }
          ],
          textos: [
            { campo: 'descripcion', titulo: 'Descripción' },
            { campo: 'diseno', titulo: 'Diseño' },
            { campo: 'problemas', titulo: 'Problemas' }
          ],
          hijos: [recursosTarea, actividadesTarea]
        },
        casosPlan
      ]
    },
    desarrollo,
    {
      id: 'pruebas',
      titulo: 'Pruebas',
      hijos: [
        texto('datos_pruebas', 'Datos para las pruebas', 'datos_pruebas'),
        {
          tipo: 'entidades',
          id: 'casos-prueba',
          titulo: 'Casos de prueba',
          recurso: 'casos-prueba',
          etiqueta: 'caso',
          clave: (c, doc) => tituloOrigen(c, 'caso_plan_id', doc?.['casos-plan'], 'Caso'),
          origen: origenCasoPlan,
          campos: [
            campoCasoPlan,
            { campo: 'requisito_codigo', etiqueta: 'Requisito', ancho: 'codigo' },
            {
              campo: 'estado',
              etiqueta: 'Estado',
              control: 'select',
              opciones: RESULTADOS_PRUEBA
            },
            { campo: 'responsable', etiqueta: 'Responsable' },
            { campo: 'incidencias', etiqueta: 'Incidencias' },
            { campo: 'es_regresion', etiqueta: 'Regresión', control: 'check' }
          ],
          textos: [{ campo: 'datos', titulo: 'Datos de la prueba' }],
          hijos: [ejecuciones]
        }
      ]
    },
    dod,
    despliegue(),
    { id: 'reuniones', titulo: 'Reuniones', hijos: [reuniones] },
    {
      id: 'seguimiento',
      titulo: 'Seguimiento',
      hijos: [
        {
          tipo: 'tabla',
          id: 'planificacion',
          titulo: 'Planificación',
          recurso: 'planificacion',
          columnas: [
            { campo: 'requisito_codigo', etiqueta: 'Requisito' },
            { campo: 'tarea_codigo', etiqueta: 'Tarea' },
            { campo: 'responsable', etiqueta: 'Responsable' },
            { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_TAREA },
            { campo: 'estimado', etiqueta: 'Estimado', control: 'numero' },
            { campo: 'real', etiqueta: 'Real', control: 'numero' },
            { campo: 'inicio', etiqueta: 'Inicio' },
            { campo: 'fin', etiqueta: 'Fin' },
            { campo: 'bloqueos', etiqueta: 'Bloqueos', control: 'area' }
          ]
        },
        {
          tipo: 'tabla',
          id: 'trazabilidad',
          titulo: 'Matriz de trazabilidad',
          recurso: 'trazabilidad',
          columnas: [
            { campo: 'requisito_codigo', etiqueta: 'Requisito' },
            { campo: 'criterio_codigo', etiqueta: 'Criterio' },
            { campo: 'tarea_codigo', etiqueta: 'Tarea' },
            { campo: 'prueba_codigo', etiqueta: 'Prueba' },
            { campo: 'cambios', etiqueta: 'Cambios' },
            {
              campo: 'estado_cobertura',
              etiqueta: 'Cobertura',
              control: 'select',
              opciones: COBERTURAS
            }
          ]
        },
        seguimientos
      ]
    }
  ]
}

export const ESQUEMA_INCIDENCIA = {
  tipo: 'incidencias',
  etiqueta: 'Incidencia',
  cabecera: [
    { campo: 'codigo', etiqueta: 'Código' },
    { campo: 'titulo', etiqueta: 'Título' },
    { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_DOC },
    { campo: 'responsable', etiqueta: 'Responsable' },
    { campo: 'severidad', etiqueta: 'Severidad', control: 'select', opciones: SEVERIDADES },
    { campo: 'prioridad', etiqueta: 'Prioridad', control: 'select', opciones: PRIORIDADES },
    { campo: 'version_afectada', etiqueta: 'Versión afectada' },
    {
      campo: 'entorno_deteccion',
      etiqueta: 'Entorno detección',
      control: 'select',
      opciones: ENTORNOS
    },
    { campo: 'fecha_deteccion', etiqueta: 'Fecha detección' },
    { campo: 'fecha_objetivo', etiqueta: 'Fecha objetivo' },
    { campo: 'commits', etiqueta: 'Commits' },
    { campo: 'despliegues', etiqueta: 'Despliegues' },
    { campo: 'incidencia_jira', etiqueta: 'Incidencia Jira' }
  ],
  secciones: [
    {
      id: 'problema',
      titulo: 'Problema',
      hijos: [
        texto('resumen', 'Resumen', 'resumen'),
        texto('descripcion_problema', 'Descripción del problema', 'descripcion_problema'),
        texto('impacto', 'Impacto', 'impacto'),
        texto('pasos_reproducir', 'Pasos para reproducir', 'pasos_reproducir'),
        texto('comportamiento_actual', 'Comportamiento actual', 'comportamiento_actual'),
        texto('comportamiento_esperado', 'Comportamiento esperado', 'comportamiento_esperado'),
        texto('alcance_correccion', 'Alcance de la corrección', 'alcance_correccion'),
        texto('fuera_alcance', 'Fuera de alcance', 'fuera_alcance'),
        texto('supuestos_restricciones', 'Supuestos y restricciones', 'supuestos_restricciones'),
        texto('dependencias', 'Dependencias', 'dependencias'),
        texto('riesgos_mitigacion', 'Riesgos y mitigación', 'riesgos_mitigacion'),
        texto('decisiones_pendientes', 'Decisiones pendientes', 'decisiones_pendientes'),
        texto('evidencias_iniciales', 'Evidencias iniciales', 'evidencias_iniciales'),
        {
          tipo: 'tabla',
          id: 'criterios',
          titulo: 'Criterios de aceptación',
          recurso: 'criterios',
          columnas: [
            { campo: 'codigo', etiqueta: 'Id' },
            { campo: 'criterio', etiqueta: 'Criterio', control: 'area' }
          ]
        }
      ]
    },
    {
      id: 'analisis',
      titulo: 'Análisis',
      hijos: [
        texto('investigacion_previa', 'Investigación previa', 'investigacion_previa'),
        texto('causa_raiz', 'Causa raíz', 'causa_raiz'),
        texto('descripcion_solucion', 'Descripción de la solución', 'descripcion_solucion'),
        repositorios,
        {
          tipo: 'entidades',
          id: 'tareas',
          titulo: 'Tareas',
          recurso: 'tareas',
          etiqueta: 'tarea',
          clave: (t) => [t.codigo, t.nombre].filter(Boolean).join(' — ') || 'Tarea',
          campos: [
            { campo: 'codigo', etiqueta: 'Id' },
            { campo: 'nombre', etiqueta: 'Nombre' },
            { campo: 'criterio_codigo', etiqueta: 'Criterio de aceptación' },
            { campo: 'dependencias', etiqueta: 'Dependencias' },
            { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_TAREA }
          ],
          textos: [
            { campo: 'descripcion', titulo: 'Descripción' },
            { campo: 'diseno', titulo: 'Diseño de la corrección' },
            { campo: 'problemas', titulo: 'Problemas' }
          ],
          hijos: [recursosTarea, actividadesTarea]
        },
        casosPlan
      ]
    },
    desarrollo,
    {
      id: 'pruebas',
      titulo: 'Pruebas',
      hijos: [
        texto('datos_pruebas', 'Datos para las pruebas', 'datos_pruebas'),
        texto(
          'verificacion_no_regresion',
          'Verificación de no regresión',
          'verificacion_no_regresion'
        ),
        {
          tipo: 'entidades',
          id: 'casos-prueba',
          titulo: 'Casos de prueba',
          recurso: 'casos-prueba',
          etiqueta: 'caso',
          clave: (c, doc) =>
            tituloOrigen(c, 'caso_plan_id', doc?.['casos-plan'], 'Caso') +
            (c.es_regresion ? ' (regresión)' : ''),
          origen: origenCasoPlan,
          campos: [
            campoCasoPlan,
            {
              campo: 'estado',
              etiqueta: 'Estado',
              control: 'select',
              opciones: RESULTADOS_PRUEBA
            },
            { campo: 'responsable', etiqueta: 'Responsable' },
            { campo: 'incidencias', etiqueta: 'Incidencias relacionadas' },
            { campo: 'es_regresion', etiqueta: 'Regresión', control: 'check' }
          ],
          textos: [
            { campo: 'datos', titulo: 'Datos de la prueba' },
            { campo: 'datos_usados', titulo: 'Datos usados para el caso' },
            { campo: 'pasos_dados', titulo: 'Pasos dados' }
          ],
          hijos: [ejecuciones]
        }
      ]
    },
    dod,
    despliegue(),
    { id: 'reuniones', titulo: 'Reuniones', hijos: [reuniones] },
    {
      id: 'seguimiento',
      titulo: 'Seguimiento',
      hijos: [
        {
          tipo: 'tabla',
          id: 'planificacion',
          titulo: 'Planificación',
          recurso: 'planificacion',
          columnas: [
            { campo: 'criterio_codigo', etiqueta: 'Criterio' },
            { campo: 'tarea_codigo', etiqueta: 'Tarea' },
            { campo: 'responsable', etiqueta: 'Responsable' },
            { campo: 'estado', etiqueta: 'Estado', control: 'select', opciones: ESTADOS_TAREA },
            { campo: 'estimado', etiqueta: 'Estimado', control: 'numero' },
            { campo: 'real', etiqueta: 'Real', control: 'numero' },
            { campo: 'inicio', etiqueta: 'Inicio' },
            { campo: 'fin', etiqueta: 'Fin' },
            { campo: 'bloqueos', etiqueta: 'Bloqueos', control: 'area' }
          ]
        },
        {
          tipo: 'tabla',
          id: 'trazabilidad',
          titulo: 'Matriz de trazabilidad',
          recurso: 'trazabilidad',
          columnas: [
            { campo: 'criterio_codigo', etiqueta: 'Criterio' },
            { campo: 'tarea_codigo', etiqueta: 'Tarea' },
            { campo: 'prueba_codigo', etiqueta: 'Prueba' },
            { campo: 'cambios', etiqueta: 'Cambios' },
            {
              campo: 'estado_cobertura',
              etiqueta: 'Cobertura',
              control: 'select',
              opciones: COBERTURAS
            }
          ]
        },
        seguimientos
      ]
    }
  ]
}

export const ESQUEMAS = {
  evolutivos: ESQUEMA_EVOLUTIVO,
  incidencias: ESQUEMA_INCIDENCIA
}
