<script setup>
import EntradaCampo from './EntradaCampo.vue'

defineProps({
  items: { type: Array, default: () => [] },
  campo: { type: String, default: 'descripcion' },
  check: { type: String, default: 'completado' }
})
const emit = defineEmits(['crear', 'actualizar', 'borrar'])
</script>

<template>
  <div class="checklist">
    <div v-for="item in items" :key="item.id" class="fila">
      <input
        type="checkbox"
        :checked="!!item[check]"
        @change="emit('actualizar', item.id, { [check]: $event.target.checked })"
      />
      <EntradaCampo
        :valor="item[campo]"
        @cambiar="emit('actualizar', item.id, { [campo]: $event })"
      />
      <button class="peligro" type="button" @click="emit('borrar', item.id)">✕</button>
    </div>
    <p v-if="!items.length" class="vacio">Sin elementos</p>
    <button type="button" @click="emit('crear')">+ Añadir elemento</button>
  </div>
</template>

<style scoped>
.fila {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.fila input[type='checkbox'] {
  width: auto;
  flex: none;
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
  margin: 0 0 6px;
}
</style>
