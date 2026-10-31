<script setup>
import { computed, provide, ref, watch } from 'vue'
import { api } from '../api.js'
import { abrirTodo, cerrarTodo } from '../store/acordeon.js'
import { construirIndice, todasLasClaves } from '../toc.js'
import { COLORES_SECCION, ESQUEMAS } from '../schema.js'
import Acordeon from './Acordeon.vue'
import EntradaCampo from './EntradaCampo.vue'
import MarkdownField from './MarkdownField.vue'
import NodoSeccion from './NodoSeccion.vue'

const props = defineProps({
  tipo: { type: String, required: true },
  id: { type: Number, required: true },
  saltarA: { type: String, default: '' },
  terminoBusqueda: { type: String, default: '' }
})
const emit = defineEmits(['indice', 'cambiado', 'error', 'volver-busqueda'])

const doc = ref(null)
const cargando = ref(false)
const esquema = computed(() => ESQUEMAS[props.tipo])
const indice = computed(() => (doc.value ? construirIndice(esquema.value, doc.value) : []))

async function recargar() {
  cargando.value = true
  try {
    doc.value = await api.documento(props.tipo, props.id)
  } catch (e) {
    emit('error', e.message)
  } finally {
    cargando.value = false
  }
}

async function ejecutar(accion, avisarArbol = false) {
  try {
    await accion()
    await recargar()
    if (avisarArbol) emit('cambiado')
  } catch (e) {
    emit('error', e.message)
  }
}

const ctx = {
  get tipo() {
    return props.tipo
  },
  get id() {
    return props.id
  },
  guardarCampo: (campo, valor) =>
    ejecutar(
      () => api.actualizarDocumento(props.tipo, props.id, { [campo]: valor }),
      ['codigo', 'titulo', 'estado', 'severidad', 'prioridad'].includes(campo)
    ),
  crearHijo: (recurso, rutaPadre, padreId, datos) =>
    ejecutar(() => api.crearHijo(props.tipo, recurso, padreId, datos, rutaPadre)),
  actualizarHijo: (recurso, id, datos) =>
    ejecutar(() => api.actualizarHijo(props.tipo, recurso, id, datos)),
  borrarHijo: (recurso, id) => ejecutar(() => api.borrarHijo(props.tipo, recurso, id))
}
provide('ctx', ctx)

watch(indice, (v) => emit('indice', v), { immediate: true })
watch(
  () => [props.tipo, props.id],
  () => {
    recargar().then(() => {
      abrirTodo(['doc/cabecera', ...esquema.value.secciones.map((s) => `doc/${s.id}`)])
      if (props.saltarA) {
        setTimeout(() => irA(props.saltarA), 150)
      }
    })
  },
  { immediate: true }
)

watch(
  () => props.saltarA,
  (nueva) => {
    if (nueva) {
      setTimeout(() => irA(nueva), 150)
    }
  }
)

const fechaImpresion = computed(() =>
  new Date().toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
)

function exportarPdf() {
  expandirTodo()
  const tituloOriginal = document.title
  const prefijo = doc.value?.codigo ? `${doc.value.codigo} - ` : ''
  const tituloDoc = doc.value?.titulo || 'Documento'
  document.title = `${prefijo}${tituloDoc}`

  requestAnimationFrame(() => {
    setTimeout(() => {
      window.print()
      document.title = tituloOriginal
    }, 180)
  })
}

function expandirTodo() {
  abrirTodo(todasLasClaves(indice.value))
}

async function borrarDocumento() {
  if (!confirm('¿Eliminar este documento y todo su contenido?')) return
  try {
    await api.borrarDocumento(props.tipo, props.id)
    emit('cambiado', { borrado: true })
  } catch (e) {
    emit('error', e.message)
  }
}
</script>

<template>
  <article v-if="doc" class="md documento">
    <div class="cabecera-impresion">
      <span class="logo-impresion">OnePage · {{ esquema.etiqueta }}</span>
      <span class="fecha-impresion">Exportado el {{ fechaImpresion }}</span>
    </div>
    <div v-if="terminoBusqueda" class="banner-busqueda">
      <span>
        🔍 Coincidencia para <strong>«{{ terminoBusqueda }}»</strong>
      </span>
      <button type="button" class="enlace-volver" @click="emit('volver-busqueda')">
        ← Volver a resultados de búsqueda
      </button>
    </div>
    <div class="barra">
      <h1>{{ doc.titulo || '(sin título)' }}</h1>
      <div class="botones">
        <button type="button" class="primario" title="Exportar este documento a formato PDF" @click="exportarPdf">
          📄 Exportar a PDF
        </button>
        <button type="button" @click="expandirTodo">Expandir todo</button>
        <button type="button" @click="cerrarTodo()">Contraer todo</button>
        <button type="button" class="peligro" @click="borrarDocumento">Eliminar</button>
      </div>
    </div>
    <p class="meta">
      <span class="etiqueta-estado">{{ esquema.etiqueta }}</span>
      <span class="etiqueta-estado">{{ doc.estado }}</span>
      <span v-if="doc.codigo" class="etiqueta-estado">{{ doc.codigo }}</span>
    </p>
    <hr class="separador" />

    <Acordeon clave="doc/cabecera" titulo="Cabecera" :nivel="2" :color="COLORES_SECCION.cabecera">
      <dl class="ficha">
        <template v-for="c in esquema.cabecera" :key="c.campo">
          <dt>{{ c.etiqueta }}</dt>
          <dd>
            <EntradaCampo
              :valor="doc[c.campo]"
              :control="c.control"
              :opciones="c.opciones || []"
              @cambiar="ctx.guardarCampo(c.campo, $event)"
            />
          </dd>
        </template>
      </dl>
    </Acordeon>

    <template v-for="seccion in esquema.secciones" :key="seccion.id">
      <hr class="separador" />
      <Acordeon
        :clave="`doc/${seccion.id}`"
        :titulo="seccion.titulo"
        :nivel="2"
        :color="COLORES_SECCION[seccion.id]"
      >
        <NodoSeccion
          v-for="hijo in seccion.hijos"
          :key="hijo.id"
          :nodo="hijo"
          :datos="doc"
          :clave-base="`doc/${seccion.id}`"
          :nivel="3"
        />
      </Acordeon>
    </template>
  </article>
  <p v-else-if="cargando" class="estado">Cargando…</p>
</template>

<style scoped>
.documento {
  max-width: 1100px;
  padding: 20px 28px 120px;
}

.barra {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.botones {
  display: flex;
  gap: 6px;
  flex: none;
}

.meta {
  display: flex;
  gap: 6px;
  margin: 8px 0 0;
}

.ficha {
  display: grid;
  grid-template-columns: 210px 1fr;
  gap: 5px 12px;
  margin: 0;
  align-items: center;
}

.ficha dt {
  font-weight: 600;
  color: var(--fg-muted);
  font-size: 13px;
}

.ficha dd {
  margin: 0;
}

.estado {
  padding: 24px;
  color: var(--fg-muted);
}
.banner-busqueda {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--accent-soft);
  border: 1px solid var(--accent);
  border-radius: 6px;
  padding: 8px 14px;
  margin-bottom: 16px;
  font-size: 13px;
}

.enlace-volver {
  background: var(--bg);
  border: 1px solid var(--accent);
  color: var(--accent);
  font-weight: 600;
  cursor: pointer;
  padding: 3px 10px;
  border-radius: 4px;
}

.enlace-volver:hover {
  background: var(--accent);
  color: #fff;
}

.cabecera-impresion {
  display: none;
}
</style>
