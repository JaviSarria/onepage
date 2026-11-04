<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { api } from './api.js'
import { setClaveActual } from './store/acordeon.js'
import ArbolContenido from './components/ArbolContenido.vue'
import ArbolProyectos from './components/ArbolProyectos.vue'
import BusquedaVista from './components/BusquedaVista.vue'
import ConfiguracionVista from './components/ConfiguracionVista.vue'
import DiarioSeguimiento from './components/DiarioSeguimiento.vue'
import DocumentoVista from './components/DocumentoVista.vue'
import ProyectoVista from './components/ProyectoVista.vue'

const arbol = ref([])
const seleccion = ref(null)
const indice = ref([])
const error = ref('')

const consultaBusqueda = ref('')
const saltarA = ref('')
const terminoBusquedaActivo = ref('')
const ultimaSeleccion = ref(null)

// Anchos de las columnas laterales (el centro se ajusta con el espacio disponible).
const anchoIzquierda = ref(290)
const anchoDerecha = ref(270)

const estiloDisposicion = computed(() => ({
  gridTemplateColumns: `${anchoIzquierda.value}px 6px minmax(0, 1fr) 6px ${anchoDerecha.value}px`,
  '--ancho-izq': `${anchoIzquierda.value}px`
}))

function iniciarRedimension(parte) {
  const alMover = (evento) => {
    const total = window.innerWidth
    if (parte === 'izquierda') {
      anchoIzquierda.value = Math.min(
        Math.max(event.clientX - 3, 160),
        Math.max(0, total - 160 - anchoDerecha.value)
      )
    } else {
      anchoDerecha.value = Math.min(
        Math.max(total - event.clientX + 3, 160),
        Math.max(0, total - anchoIzquierda.value - 160)
      )
    }
  }
  const alSoltar = () => {
    window.removeEventListener('mousemove', alMover)
    window.removeEventListener('mouseup', alSoltar)
  }
  window.addEventListener('mousemove', alMover)
  window.addEventListener('mouseup', alSoltar)
}

const proyectoSeleccionado = computed(() =>
  seleccion.value?.tipo === 'proyecto'
    ? arbol.value.find((p) => p.id === seleccion.value.id)
    : null
)

function registrarCampoActual(evento) {
  const seccion = evento.target.closest('.acordeon[data-clave]')
  if (seccion) setClaveActual(seccion.dataset.clave)
}

async function cargarArbol() {
  try {
    arbol.value = await api.arbol()
  } catch (e) {
    error.value = `No se puede contactar con el backend: ${e.message}`
  }
}

function manejarTeclasGlobales(e) {
  if (
    ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') ||
    (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(e.target.tagName))
  ) {
    e.preventDefault()
    abrirBusqueda()
  }
}

onMounted(() => {
  cargarArbol()
  window.addEventListener('keydown', manejarTeclasGlobales)
})

onUnmounted(() => {
  window.removeEventListener('keydown', manejarTeclasGlobales)
})

function seleccionar(sel) {
  indice.value = []
  setClaveActual('')
  if (sel?.tipo !== 'busqueda') {
    saltarA.value = ''
  }
  seleccion.value = sel
}

function abrirBusqueda(termino = '') {
  if (seleccion.value?.tipo !== 'busqueda') {
    ultimaSeleccion.value = seleccion.value
  }
  if (termino) {
    consultaBusqueda.value = termino
  }
  indice.value = []
  seleccion.value = { tipo: 'busqueda', consulta: consultaBusqueda.value }
}

function cerrarBusqueda() {
  if (ultimaSeleccion.value) {
    seleccion.value = ultimaSeleccion.value
    ultimaSeleccion.value = null
  } else {
    seleccion.value = null
  }
}

function abrirConfiguracion() {
  ultimaSeleccion.value = seleccion.value
  indice.value = []
  setClaveActual('')
  seleccion.value = { tipo: 'configuracion' }
}

function cerrarConfiguracion() {
  seleccion.value = ultimaSeleccion.value
  ultimaSeleccion.value = null
}

function abrirDesdeBusqueda(datos) {
  terminoBusquedaActivo.value = datos.termino || consultaBusqueda.value
  seleccionar({ tipo: datos.tipo, id: datos.id, proyecto: datos.proyecto })
  saltarA.value = datos.saltarA || ''
  setClaveActual(saltarA.value)
}

async function nuevoProyecto() {
  const nombre = prompt('Nombre del proyecto')
  if (!nombre) return
  const p = await api.crearProyecto({ nombre })
  await cargarArbol()
  seleccionar({ tipo: 'proyecto', id: p.id })
}

async function borrarProyecto(p) {
  if (!confirm(`¿Eliminar el proyecto "${p.nombre}" con todos sus documentos?`)) return
  await api.borrarProyecto(p.id)
  seleccion.value = null
  await cargarArbol()
}

async function nuevoDocumento({ proyecto, tipo }) {
  const titulo = prompt(tipo === 'evolutivos' ? 'Título del evolutivo' : 'Título de la incidencia')
  if (!titulo) return
  const doc = await api.crearDocumento(tipo, { proyecto_id: proyecto.id, titulo })
  await cargarArbol()
  seleccionar({ tipo, id: doc.id })
}

async function documentoCambiado(info) {
  await cargarArbol()
  if (info && info.borrado) seleccion.value = null
}
</script>

<template>
  <div class="disposicion" :style="estiloDisposicion">
    <aside class="panel izquierda">
      <ArbolProyectos
        :nodos="arbol"
        :seleccion="seleccion"
        @seleccionar="seleccionar"
        @nuevo-proyecto="nuevoProyecto"
        @nuevo-documento="nuevoDocumento"
        @borrar-proyecto="borrarProyecto"
        @diario="seleccionar(null)"
        @buscar="abrirBusqueda($event || '')"
        @configuracion="abrirConfiguracion"
      />
    </aside>

    <div class="divisor" @mousedown="iniciarRedimension('izquierda')"></div>

    <main class="centro" @focusin="registrarCampoActual">
      <p v-if="error" class="error">{{ error }}</p>

      <!-- Vista de configuración (base de datos) -->
      <ConfiguracionVista
        v-if="seleccion && seleccion.tipo === 'configuracion'"
        @cerrar="cerrarConfiguracion"
      />

      <!-- Zona de búsqueda y resultados -->
      <BusquedaVista
        v-if="seleccion && seleccion.tipo === 'busqueda'"
        :consulta-inicial="seleccion.consulta || consultaBusqueda"
        @abrir="abrirDesdeBusqueda"
        @cerrar="cerrarBusqueda"
        @error="error = $event"
      />

      <!-- Vista de documento (evolutivo o incidencia) -->
      <DocumentoVista
        v-else-if="seleccion && seleccion.tipo !== 'proyecto'"
        :key="seleccion.tipo + seleccion.id"
        :tipo="seleccion.tipo"
        :id="seleccion.id"
        :saltar-a="saltarA"
        :termino-busqueda="terminoBusquedaActivo"
        @indice="indice = $event"
        @cambiado="documentoCambiado"
        @volver-busqueda="abrirBusqueda(terminoBusquedaActivo)"
        @error="error = $event"
      />

      <!-- Vista de proyecto -->
      <ProyectoVista
        v-else-if="proyectoSeleccionado"
        :nodo="proyectoSeleccionado"
        @cambiado="cargarArbol"
        @abrir="seleccionar"
        @nuevo-documento="nuevoDocumento({ proyecto: proyectoSeleccionado, tipo: $event })"
        @error="error = $event"
      />

      <!-- Pantalla de bienvenida -->
      <section v-else class="md bienvenida">
        <h1>OnePage</h1>
        <blockquote>
          Gestión de proyectos personales: evolutivos e incidencias en una única página.
        </blockquote>
        <p>
          Selecciona un proyecto en el árbol de la izquierda, crea uno nuevo con el botón «+»,
          o pulsa el botón 🔍 para buscar en cualquier parte.
        </p>
        <DiarioSeguimiento @abrir="seleccionar" @error="error = $event" />
      </section>
    </main>

    <div class="divisor derecho" @mousedown="iniciarRedimension('derecha')"></div>

    <aside class="panel derecha">
      <template v-if="seleccion?.tipo === 'busqueda'">
        <h2>Búsqueda global</h2>
        <div class="panel-ayuda-busqueda">
          <p><strong>Buscar en cualquier parte:</strong></p>
          <ul>
            <li>Inspecciona títulos, códigos, textos markdown, tablas y checklists.</li>
            <li>Filtra por evolutivos, incidencias o proyectos.</li>
            <li>
              Al hacer clic en un resultado, se abrirá el documento y se desplazará automáticamente a
              la sección correspondiente.
            </li>
          </ul>
        </div>
      </template>
      <template v-else>
        <h2>En esta página</h2>
        <ArbolContenido
          v-if="indice.length"
          :key="seleccion?.tipo + seleccion?.id"
          :nodos="indice"
        />
        <p v-else class="vacio">Sin contenido</p>
      </template>
    </aside>
  </div>
</template>

<style scoped>
.disposicion {
  display: grid;
  grid-template-columns: 290px 6px minmax(0, 1fr) 6px 270px;
  height: 100%;
}

.panel {
  overflow: auto;
  background: var(--bg-soft);
}

.izquierda {
  grid-column: 1;
  border-right: 1px solid var(--border);
}

.divisor {
  grid-column: 2;
  cursor: col-resize;
  background: var(--border-soft);
}

.centro {
  grid-column: 3;
  overflow: auto;
}

.divisor.derecho {
  grid-column: 4;
  cursor: col-resize;
  background: var(--border-soft);
}

.divisor:hover {
  background: var(--accent);
}

.derecha {
  grid-column: 5;
  border-left: 1px solid var(--border);
  padding: 12px;
}

.derecha h2 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--fg-muted);
  margin: 0 0 8px;
}

.panel-ayuda-busqueda {
  font-size: 12px;
  color: var(--fg-muted);
  line-height: 1.5;
}

.panel-ayuda-busqueda ul {
  padding-left: 16px;
  margin: 8px 0 0;
}

.bienvenida {
  padding: 40px;
  max-width: 900px;
}

.error {
  margin: 12px 20px;
  padding: 8px 12px;
  border: 1px solid var(--danger);
  border-radius: 6px;
  color: var(--danger);
  background: #ffebe9;
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
}

@media (max-width: 1100px) {
  .disposicion {
    grid-template-columns: var(--ancho-izq, 240px) 6px minmax(0, 1fr) !important;
  }
  .derecha {
    display: none;
  }
  .divisor.derecho {
    display: none;
  }
}
</style>
