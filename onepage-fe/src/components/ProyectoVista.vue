<script setup>
import { computed, ref } from 'vue'
import { api } from '../api.js'
import EntradaCampo from './EntradaCampo.vue'

const props = defineProps({
  nodo: { type: Object, required: true }
})
const emit = defineEmits(['cambiado', 'abrir', 'nuevo-documento', 'error'])

const guardando = ref(false)

const resumen = computed(() => {
  const cuenta = (lista, campo) =>
    lista.reduce((acc, d) => ({ ...acc, [d[campo]]: (acc[d[campo]] || 0) + 1 }), {})
  return {
    evolutivos: cuenta(props.nodo.evolutivos, 'estado'),
    incidencias: cuenta(props.nodo.incidencias, 'estado')
  }
})

async function guardar(campo, valor) {
  guardando.value = true
  try {
    await api.actualizarProyecto(props.nodo.id, { [campo]: valor })
    emit('cambiado')
  } catch (e) {
    emit('error', e.message)
  } finally {
    guardando.value = false
  }
}
</script>

<template>
  <article class="md documento">
    <h1>{{ nodo.nombre }}</h1>
    <p class="meta"><span class="etiqueta-estado">Proyecto</span></p>
    <hr class="separador" />

    <h2>Ficha</h2>
    <dl class="ficha">
      <dt>Nombre</dt>
      <dd><EntradaCampo :valor="nodo.nombre" @cambiar="guardar('nombre', $event)" /></dd>
      <dt>Estado</dt>
      <dd>
        <EntradaCampo
          :valor="nodo.estado"
          control="select"
          :opciones="['Activo', 'En pausa', 'Cerrado']"
          @cambiar="guardar('estado', $event)"
        />
      </dd>
    </dl>

    <hr class="separador" />
    <h2>Evolutivos ({{ nodo.evolutivos.length }})</h2>
    <button type="button" @click="emit('nuevo-documento', 'evolutivos')">+ Nuevo evolutivo</button>
    <table>
      <thead>
        <tr><th>Código</th><th>Título</th><th>Estado</th><th>Prioridad</th></tr>
      </thead>
      <tbody>
        <tr v-for="e in nodo.evolutivos" :key="e.id">
          <td><code>{{ e.codigo || '—' }}</code></td>
          <td>
            <button class="enlace" type="button" @click="emit('abrir', { tipo: 'evolutivos', id: e.id })">
              {{ e.titulo }}
            </button>
          </td>
          <td>{{ e.estado }}</td>
          <td>{{ e.prioridad }}</td>
        </tr>
        <tr v-if="!nodo.evolutivos.length"><td colspan="4" class="vacio">Sin evolutivos</td></tr>
      </tbody>
    </table>

    <hr class="separador" />
    <h2>Incidencias ({{ nodo.incidencias.length }})</h2>
    <button type="button" @click="emit('nuevo-documento', 'incidencias')">+ Nueva incidencia</button>
    <table>
      <thead>
        <tr><th>Código</th><th>Título</th><th>Estado</th><th>Severidad</th></tr>
      </thead>
      <tbody>
        <tr v-for="i in nodo.incidencias" :key="i.id">
          <td><code>{{ i.codigo || '—' }}</code></td>
          <td>
            <button class="enlace" type="button" @click="emit('abrir', { tipo: 'incidencias', id: i.id })">
              {{ i.titulo }}
            </button>
          </td>
          <td>{{ i.estado }}</td>
          <td>{{ i.severidad }}</td>
        </tr>
        <tr v-if="!nodo.incidencias.length"><td colspan="4" class="vacio">Sin incidencias</td></tr>
      </tbody>
    </table>

    <hr class="separador" />
    <h2>Resumen por estado</h2>
    <p>
      <span v-for="(n, estado) in resumen.evolutivos" :key="'e' + estado" class="etiqueta-estado">
        EVO {{ estado }}: {{ n }}
      </span>
      <span v-for="(n, estado) in resumen.incidencias" :key="'i' + estado" class="etiqueta-estado">
        INC {{ estado }}: {{ n }}
      </span>
    </p>
  </article>
</template>

<style scoped>
.documento {
  max-width: 1100px;
  padding: 20px 28px 120px;
}

.meta {
  margin: 8px 0 0;
}

.ficha {
  display: grid;
  grid-template-columns: 210px 1fr;
  gap: 5px 12px;
  align-items: center;
  margin: 0;
}

.ficha dt {
  font-weight: 600;
  color: var(--fg-muted);
  font-size: 13px;
}

.ficha dd {
  margin: 0;
}

table {
  margin-top: 10px;
}

.enlace {
  border: 0;
  background: none;
  padding: 0;
  color: var(--accent);
  text-align: left;
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
}

.etiqueta-estado {
  margin-right: 6px;
}
</style>
