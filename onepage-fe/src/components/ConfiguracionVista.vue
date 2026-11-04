<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api.js'

const emit = defineEmits(['cerrar'])

const bases = ref([])
const cargando = ref(false)
const error = ref('')
const archivo = ref(null)
const baseSeleccionada = ref('')

async function cargar() {
  cargando.value = true
  error.value = ''
  try {
    bases.value = await api.sistemaBases()
    baseSeleccionada.value = bases.value[0]?.nombre || ''
  } catch (e) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

async function exportar() {
  for (const base of bases.value) {
    await api.sistemaDescargar(base.nombre)
  }
}

async function restaurar() {
  const base = bases.value.find((b) => b.nombre === baseSeleccionada.value) || bases.value[0]
  if (!base || !archivo.value) return
  await api.sistemaImportar(base.nombre, archivo.value)
  archivo.value = null
}

onMounted(cargar)
</script>

<template>
  <section class="config">
    <header class="cabecera-config">
      <h2>Configuración</h2>
      <button type="button" class="boton" @click="emit('cerrar')">← Volver</button>
    </header>

    <h3>Base de datos</h3>
    <p v-if="error" class="error">{{ error }}</p>
    <ul v-else-if="!cargando" class="lista-bases">
      <li v-for="base in bases" :key="base.nombre">{{ base.nombre }}</li>
    </ul>

    <div class="acciones">
      <button type="button" :disabled="cargando" @click="exportar">Exportar bases de datos</button>
    </div>

    <div v-if="bases.length" class="acciones">
      <select v-model="baseSeleccionada">
        <option v-for="base in bases" :key="base.nombre" :value="base.nombre">{{ base.nombre }}</option>
      </select>
      <input type="file" accept=".sqlite3,application/octet-stream" @change="archivo = $event.target.files?.[0]" />
      <button type="button" :disabled="!archivo" @click="restaurar">Restaurar / importar</button>
    </div>
  </section>
</template>

<style scoped>
.config {
  max-width: 720px;
  padding: 20px 28px 120px;
}

.cabecera-config {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.cabecera-config h2 {
  margin: 0;
  font-size: 20px;
}

.acciones {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.lista-bases {
  padding-left: 18px;
}

.error {
  color: var(--danger);
}
</style>
