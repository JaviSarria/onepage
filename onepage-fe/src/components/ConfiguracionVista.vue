<script setup>
import { onMounted, ref } from 'vue'
import { api } from '../api.js'

const emit = defineEmits(['cerrar'])

const bases = ref([])
const cargando = ref(false)
const error = ref('')
const notificacion = ref('')
const archivosAssets = ref([])
const archivoTodo = ref(null)
const modoImport = ref('evolutivos')
const archivo = ref(null)

const MAPA_IMPORT = { evolutivos: 'evolutivos.sqlite3', incidencias: 'incidencias.sqlite3' }

async function cargar() {
  cargando.value = true
  error.value = ''
  notificacion.value = ''
  try {
    bases.value = await api.sistemaBases()
  } catch (e) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

async function exportar() {
  notificacion.value = ''
  const nombre = await api.sistemaExportar()
  notificacion.value = `Exportación completada. Archivo creado: ${nombre}. Contenido: ${bases.value.map((b) => b.nombre).join(', ')}; carpeta assets incluida. Los ficheros se descargaron a la carpeta de descargas del navegador.`
}

async function importarBase() {
  if (!archivo.value) return
  const nombre = MAPA_IMPORT[modoImport.value]
  if (!nombre) return
  notificacion.value = ''
  error.value = ''
  try {
    const r = await api.sistemaImportar(nombre, archivo.value)
    notificacion.value = `Importación de la base ${nombre} completada. OK: ${r?.ok}`
  } catch (e) {
    notificacion.value = `Fallo la importación de la base ${nombre}: ${e.message}`
  }
}

async function importarAssets() {
  notificacion.value = ''
  if (!archivosAssets.value.length) return
  error.value = ''
  const ok = []
  for (const f of archivosAssets.value) {
    try {
      const r = await api.sistemaImportarAsset(f)
      ok.push(r?.destino || f.name)
    } catch (e) {
      error.value = e.message
      notificacion.value = `Fallo la importación de assets: ${e.message}`
      return
    }
  }
  notificacion.value = `Importación de assets completada. Ficheros subidos: ${ok.length}.`
}

async function importarTodo() {
  if (!archivoTodo.value) return
  notificacion.value = ''
  error.value = ''
  try {
    const r = await api.sistemaImportarTodo(archivoTodo.value)
    notificacion.value = `Importación completa completada. OK: ${r?.ok}`
  } catch (e) {
    notificacion.value = `Fallo la importación completa: ${e.message}`
  }
}

onMounted(cargar)
</script>

<template>
  <section class="config">
    <header class="cabecera-config">
      <h2>Configuración</h2>
      <button type="button" class="boton" @click="emit('cerrar')">← Volver</button>
    </header>

    <h3>Datos</h3>
    <p v-if="error" class="error">{{ error }}</p>
    <ul v-else-if="!cargando" class="lista-bases">
      <li v-for="base in bases" :key="base.nombre">{{ base.nombre }}</li>
    </ul>

    <div class="acciones">
      <button type="button" :disabled="cargando" @click="exportar">Exportar datos</button>
    </div>

    <div class="acciones">
      <select v-model="modoImport">
        <option value="evolutivos">evolutivos</option>
        <option value="incidencias">incidencias</option>
        <option value="assets">assets</option>
        <option value="todos">todos</option>
      </select>

      <template v-if="modoImport === 'evolutivos' || modoImport === 'incidencias'">
        <input type="file" accept=".sqlite3" @change="archivo = $event.target.files?.[0]" />
        <button type="button" :disabled="!archivo" @click="importarBase">Importar</button>
      </template>

      <template v-else-if="modoImport === 'assets'">
        <input type="file" multiple @change="archivosAssets = Array.from($event.target.files || [])" />
        <button type="button" :disabled="!archivosAssets.length" @click="importarAssets">Importar assets</button>
      </template>

      <template v-else-if="modoImport === 'todos'">
        <input type="file" accept=".zip" @change="archivoTodo = $event.target.files?.[0]" />
        <button type="button" :disabled="!archivoTodo" @click="importarTodo">Importar todo</button>
      </template>
    </div>

    <div v-if="notificacion" class="notificacion" role="status">{{ notificacion }}</div>
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

.notificacion {
  margin-top: 12px;
  padding: 8px 10px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg-soft);
  color: var(--fg);
  font-size: 12px;
}
</style>
