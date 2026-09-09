<script setup>
import { computed, provide, ref, watch } from 'vue'
import { api } from '../api.js'
import { abrirTodo, cerrarTodo } from '../store/acordeon.js'
import { construirIndice, todasLasClaves } from '../toc.js'
import { ESQUEMAS } from '../schema.js'
import Acordeon from './Acordeon.vue'
import EntradaCampo from './EntradaCampo.vue'
import NodoSeccion from './NodoSeccion.vue'

const props = defineProps({
  tipo: { type: String, required: true },
  id: { type: Number, required: true }
})
const emit = defineEmits(['indice', 'cambiado', 'error'])

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
    recargar().then(() => abrirTodo(['doc/cabecera', ...esquema.value.secciones.map((s) => `doc/${s.id}`)]))
  },
  { immediate: true }
)

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
    <div class="barra">
      <h1>{{ doc.titulo || '(sin título)' }}</h1>
      <div class="botones">
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

    <Acordeon clave="doc/cabecera" titulo="Cabecera" :nivel="2">
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
      <Acordeon :clave="`doc/${seccion.id}`" :titulo="seccion.titulo" :nivel="2">
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
</style>
