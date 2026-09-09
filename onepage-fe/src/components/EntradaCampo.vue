<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  valor: { type: [String, Number, Boolean], default: '' },
  control: { type: String, default: 'texto' },
  opciones: { type: Array, default: () => [] }
})
const emit = defineEmits(['cambiar'])

const local = ref(props.valor)
watch(
  () => props.valor,
  (v) => (local.value = v)
)

function confirmar() {
  if (local.value !== props.valor) emit('cambiar', local.value)
}

function cambiarInmediato(v) {
  local.value = v
  emit('cambiar', v)
}
</script>

<template>
  <select
    v-if="control === 'select' || control === 'select-dinamico'"
    :value="local"
    @change="cambiarInmediato($event.target.value)"
  >
    <option v-for="o in opciones" :key="typeof o === 'object' ? o.valor : o" :value="typeof o === 'object' ? o.valor : o">
      {{ typeof o === 'object' ? o.etiqueta : o }}
    </option>
  </select>
  <input
    v-else-if="control === 'check'"
    type="checkbox"
    class="check"
    :checked="!!local"
    @change="cambiarInmediato($event.target.checked)"
  />
  <input
    v-else-if="control === 'numero'"
    type="number"
    step="0.25"
    v-model="local"
    @blur="emit('cambiar', Number(local) || 0)"
  />
  <textarea v-else-if="control === 'area'" v-model="local" rows="4" @blur="confirmar" />
  <input v-else type="text" v-model="local" @blur="confirmar" @keyup.enter="confirmar" />
</template>

<style scoped>
.check {
  width: auto;
}
</style>
