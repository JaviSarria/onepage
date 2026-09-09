<script setup>
import EntradaCampo from './EntradaCampo.vue'

defineProps({
  columnas: { type: Array, required: true },
  items: { type: Array, default: () => [] },
  crearHabilitado: { type: Boolean, default: true },
  mensajeCrear: { type: String, default: '' }
})
const emit = defineEmits(['crear', 'actualizar', 'borrar'])
</script>

<template>
  <div class="tabla-envoltorio md">
    <table>
      <thead>
        <tr>
          <th
            v-for="c in columnas"
            :key="c.campo"
            :class="c.ancho ? `columna-${c.ancho}` : ''"
          >
            {{ c.etiqueta }}
          </th>
          <th class="acciones-col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td
            v-for="c in columnas"
            :key="c.campo"
            :class="c.ancho ? `columna-${c.ancho}` : ''"
          >
            <EntradaCampo
              :valor="item[c.campo]"
              :control="c.control"
              :opciones="c.opciones || []"
              @cambiar="emit('actualizar', item.id, { [c.campo]: $event })"
            />
          </td>
          <td class="acciones-col">
            <button class="peligro" type="button" title="Eliminar" @click="emit('borrar', item.id)">
              ✕
            </button>
          </td>
        </tr>
        <tr v-if="!items.length">
          <td :colspan="columnas.length + 1" class="vacio">Sin registros</td>
        </tr>
      </tbody>
    </table>
    <button
      type="button"
      class="anadir"
      :disabled="!crearHabilitado"
      :title="mensajeCrear"
      @click="emit('crear')"
    >
      + Añadir fila
    </button>
  </div>
</template>

<style scoped>
.tabla-envoltorio {
  overflow-x: auto;
  margin-bottom: 8px;
}

td :deep(input),
td :deep(select),
td :deep(textarea) {
  border-color: transparent;
  background: transparent;
  padding: 2px 4px;
}

td :deep(input:focus),
td :deep(select:focus),
td :deep(textarea:focus) {
  border-color: var(--accent);
  background: var(--bg);
}

.acciones-col {
  width: 34px;
  text-align: center;
}

.columna-codigo {
  width: 92px;
  max-width: 92px;
}

.columna-codigo :deep(input) {
  width: 78px;
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
}

.anadir {
  margin-top: 6px;
}
</style>
