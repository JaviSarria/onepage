<script setup>
import { computed, inject } from 'vue'
import Acordeon from './Acordeon.vue'
import EntradaCampo from './EntradaCampo.vue'
import ListaChecklist from './ListaChecklist.vue'
import MarkdownField from './MarkdownField.vue'
import TablaEditable from './TablaEditable.vue'
import { tituloTareaDesarrollo } from '../schema.js'

const props = defineProps({
  nodo: { type: Object, required: true },
  datos: { type: Object, required: true },
  claveBase: { type: String, required: true },
  nivel: { type: Number, default: 3 }
})

const ctx = inject('ctx')
const clave = computed(() => `${props.claveBase}/${props.nodo.id}`)
const items = computed(() => props.datos?.[props.nodo.recurso] || [])
const padreId = computed(() => props.datos?.id)
const grupos = computed(() => props.datos?.['grupos-requisito'] || [])
const tareas = computed(() => props.datos?.tareas || [])
const columnas = computed(() => {
  if (!props.nodo.columnas) return []
  return props.nodo.columnas.map((columna) =>
    columna.campo === 'grupo_id' || columna.control === 'select-dinamico-tarea'
      ? {
          ...columna,
          opciones:
            columna.campo === 'grupo_id'
              ? grupos.value.map((grupo) => ({ valor: grupo.id, etiqueta: grupo.nombre }))
              : tareas.value.map((tarea) => ({
                  valor: tarea.id,
                  etiqueta: [tarea.codigo, tarea.nombre].filter(Boolean).join(' — ')
                }))
        }
      : columna
  )
})

function opcionesCampo(campo) {
  if (campo.control === 'select-dinamico-tarea') {
    return tareas.value.map((tarea) => ({
      valor: tarea.id,
      etiqueta: [tarea.codigo, tarea.nombre].filter(Boolean).join(' — ')
    }))
  }
  return campo.opciones || []
}
const puedeCrear = computed(() => {
  if (props.nodo.id === 'requisitos') return grupos.value.length > 0
  if (props.nodo.id === 'tareas-desarrollo') return tareas.value.length > 0
  return true
})

function crear() {
  if (props.nodo.id === 'requisitos' && !grupos.value.length) return
  if (props.nodo.id === 'tareas-desarrollo' && !tareas.value.length) return
  const datos =
    props.nodo.id === 'requisitos'
      ? { grupo_id: grupos.value[0].id }
      : props.nodo.id === 'tareas-desarrollo'
        ? { tarea_id: tareas.value[0].id }
        : {}
  ctx.crearHijo(props.nodo.recurso, props.nodo.rutaPadre || null, padreId.value, datos)
}

function actualizar(id, cambios) {
  ctx.actualizarHijo(props.nodo.recurso, id, cambios)
}

function borrar(id) {
  if (confirm('¿Eliminar el registro seleccionado?')) ctx.borrarHijo(props.nodo.recurso, id)
}

function actualizarEntidad(item, campo, valor) {
  ctx.actualizarHijo(props.nodo.recurso, item.id, { [campo]: valor })
}

function tituloEntidad(item) {
  return props.nodo.id === 'tareas-desarrollo'
    ? tituloTareaDesarrollo(item, tareas.value)
    : props.nodo.clave
      ? props.nodo.clave(item)
      : '#' + item.id
}
</script>

<template>
  <!-- Bloque de texto libre del documento -->
  <Acordeon v-if="nodo.tipo === 'texto'" :clave="clave" :titulo="nodo.titulo" :nivel="nivel">
    <blockquote v-if="nodo.ayuda" class="md">{{ nodo.ayuda }}</blockquote>
    <MarkdownField
      :valor="datos[nodo.campo] || ''"
      @cambiar="ctx.guardarCampo(nodo.campo, $event)"
    />
  </Acordeon>

  <!-- Tabla editable -->
  <Acordeon
    v-else-if="nodo.tipo === 'tabla'"
    :clave="clave"
    :titulo="nodo.titulo"
    :nivel="nivel"
    :insignia="String(items.length)"
  >
    <TablaEditable
      :columnas="columnas"
      :items="items"
      :crear-habilitado="puedeCrear"
      :mensaje-crear="
        nodo.id === 'requisitos' && !puedeCrear
          ? 'Da de alta al menos un grupo de requisitos antes de crear requisitos'
          : nodo.id === 'tareas-desarrollo' && !puedeCrear
            ? 'Da de alta una tarea en Análisis antes de completar su Desarrollo'
            : ''
      "
      @crear="crear"
      @actualizar="actualizar"
      @borrar="borrar"
    />
  </Acordeon>

  <!-- Lista de comprobacion -->
  <Acordeon
    v-else-if="nodo.tipo === 'checklist'"
    :clave="clave"
    :titulo="nodo.titulo"
    :nivel="nivel"
    :insignia="items.filter((i) => i[nodo.check]).length + '/' + items.length"
  >
    <ListaChecklist
      :items="items"
      :campo="nodo.campo"
      :check="nodo.check"
      @crear="crear"
      @actualizar="actualizar"
      @borrar="borrar"
    />
  </Acordeon>

  <!-- Coleccion de entidades con sus propias subsecciones -->
  <Acordeon
    v-else-if="nodo.tipo === 'entidades'"
    :clave="clave"
    :titulo="nodo.titulo"
    :nivel="nivel"
    :insignia="String(items.length)"
  >
    <template #acciones>
      <button type="button" @click="crear">+ {{ nodo.etiqueta }}</button>
    </template>
    <p v-if="!items.length" class="vacio">Sin {{ nodo.titulo.toLowerCase() }}</p>
    <Acordeon
      v-for="item in items"
      :key="item.id"
      :clave="`${clave}/${item.id}`"
      :titulo="tituloEntidad(item)"
      :nivel="Math.min(nivel + 1, 4)"
    >
      <template #acciones>
        <button class="peligro" type="button" @click="borrar(item.id)">Eliminar</button>
      </template>

      <dl v-if="nodo.campos.length" class="ficha">
        <template v-for="c in nodo.campos" :key="c.campo">
          <dt>{{ c.etiqueta }}</dt>
          <dd>
            <EntradaCampo
              :valor="item[c.campo]"
              :control="c.control === 'select-dinamico-tarea' ? 'select' : c.control"
              :opciones="opcionesCampo(c)"
              @cambiar="actualizarEntidad(item, c.campo, $event)"
            />
          </dd>
        </template>
      </dl>

      <div v-for="t in nodo.textos" :key="t.campo" class="bloque-texto">
        <h5>{{ t.titulo }}</h5>
        <MarkdownField
          :valor="item[t.campo] || ''"
          @cambiar="actualizarEntidad(item, t.campo, $event)"
        />
      </div>

      <dl v-if="nodo.camposFinales?.length" class="ficha">
        <template v-for="c in nodo.camposFinales" :key="c.campo">
          <dt>{{ c.etiqueta }}</dt>
          <dd>
            <EntradaCampo
              :valor="item[c.campo]"
              :control="c.control"
              :opciones="c.opciones || []"
              @cambiar="actualizarEntidad(item, c.campo, $event)"
            />
          </dd>
        </template>
      </dl>

      <NodoSeccion
        v-for="hijo in nodo.hijos || []"
        :key="hijo.id"
        :nodo="hijo"
        :datos="item"
        :clave-base="`${clave}/${item.id}`"
        :nivel="4"
      />
    </Acordeon>
  </Acordeon>
</template>

<script>
export default { name: 'NodoSeccion' }
</script>

<style scoped>
.ficha {
  display: grid;
  grid-template-columns: 190px 1fr;
  gap: 4px 10px;
  margin: 0 0 12px;
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

.bloque-texto h5 {
  margin: 10px 0 4px;
  font-size: 13px;
  color: var(--fg-muted);
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
}
</style>
