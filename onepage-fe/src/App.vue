<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from './api.js'
import ArbolContenido from './components/ArbolContenido.vue'
import ArbolProyectos from './components/ArbolProyectos.vue'
import DocumentoVista from './components/DocumentoVista.vue'
import ProyectoVista from './components/ProyectoVista.vue'

const arbol = ref([])
const seleccion = ref(null)
const indice = ref([])
const error = ref('')

const proyectoSeleccionado = computed(() =>
  seleccion.value?.tipo === 'proyecto'
    ? arbol.value.find((p) => p.id === seleccion.value.id)
    : null
)

async function cargarArbol() {
  try {
    arbol.value = await api.arbol()
  } catch (e) {
    error.value = `No se puede contactar con el backend: ${e.message}`
  }
}

onMounted(cargarArbol)

function seleccionar(sel) {
  indice.value = []
  seleccion.value = sel
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
  <div class="disposicion">
    <aside class="panel izquierda">
      <ArbolProyectos
        :nodos="arbol"
        :seleccion="seleccion"
        @seleccionar="seleccionar"
        @nuevo-proyecto="nuevoProyecto"
        @nuevo-documento="nuevoDocumento"
        @borrar-proyecto="borrarProyecto"
      />
    </aside>

    <main class="centro">
      <p v-if="error" class="error">{{ error }}</p>
      <DocumentoVista
        v-if="seleccion && seleccion.tipo !== 'proyecto'"
        :key="seleccion.tipo + seleccion.id"
        :tipo="seleccion.tipo"
        :id="seleccion.id"
        @indice="indice = $event"
        @cambiado="documentoCambiado"
        @error="error = $event"
      />
      <ProyectoVista
        v-else-if="proyectoSeleccionado"
        :nodo="proyectoSeleccionado"
        @cambiado="cargarArbol"
        @abrir="seleccionar"
        @nuevo-documento="nuevoDocumento({ proyecto: proyectoSeleccionado, tipo: $event })"
        @error="error = $event"
      />
      <section v-else class="md bienvenida">
        <h1>OnePage</h1>
        <blockquote>
          Gestión de proyectos personales: evolutivos e incidencias en una única página.
        </blockquote>
        <p>Selecciona un proyecto en el árbol de la izquierda o crea uno nuevo con el botón «+».</p>
      </section>
    </main>

    <aside class="panel derecha">
      <h2>En esta página</h2>
      <ArbolContenido v-if="indice.length" :nodos="indice" />
      <p v-else class="vacio">Sin contenido</p>
    </aside>
  </div>
</template>

<style scoped>
.disposicion {
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr) 270px;
  height: 100%;
}

.panel {
  overflow: auto;
  background: var(--bg-soft);
}

.izquierda {
  border-right: 1px solid var(--border);
}

.derecha {
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

.centro {
  overflow: auto;
}

.bienvenida {
  padding: 40px;
  max-width: 700px;
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
    grid-template-columns: 240px minmax(0, 1fr);
  }
  .derecha {
    display: none;
  }
}
</style>
