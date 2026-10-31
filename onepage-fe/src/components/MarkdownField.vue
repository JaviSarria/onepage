<script setup>
import { computed, inject, ref, watch } from 'vue'
import { marked } from 'marked'
import { api } from '../api.js'

const props = defineProps({
  valor: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  // Id de la sección del documento; si se indica, se permiten imágenes (pegar/arrastrar).
  seccion: { type: String, default: '' }
})
const emit = defineEmits(['cambiar'])
const ctx = inject('ctx', null)
const vista = ref(false)
const local = ref(props.valor)
const area = ref(null)
const arrastrando = ref(false)
const subiendo = ref(false)
const error = ref('')
const admiteImagenes = computed(() => Boolean(props.seccion && ctx?.tipo && ctx?.id))

watch(
  () => props.valor,
  (valor) => {
    local.value = valor || ''
  }
)

const html = computed(() => marked.parse(local.value || '', { breaks: true }))

function guardar() {
  if (local.value !== props.valor) emit('cambiar', local.value)
}

function imagenesDe(lista) {
  return [...(lista || [])].filter((f) => f.type.startsWith('image/'))
}

async function adjuntar(ficheros) {
  if (!ficheros.length) return
  subiendo.value = true
  error.value = ''
  try {
    const enlaces = []
    for (const fichero of ficheros) {
      const { nombre, url } = await api.subirImagen(ctx.tipo, ctx.id, props.seccion, fichero)
      enlaces.push(`![${nombre}](${url})`)
    }
    const texto = enlaces.join('\n')
    const el = area.value
    const inicio = !vista.value && el ? el.selectionStart : local.value.length
    const fin = !vista.value && el ? el.selectionEnd : local.value.length
    local.value = local.value.slice(0, inicio) + texto + local.value.slice(fin)
    guardar()
  } catch (e) {
    error.value = e.message
  } finally {
    subiendo.value = false
  }
}

function alPegar(evento) {
  if (!admiteImagenes.value) return
  const ficheros = imagenesDe(evento.clipboardData?.files)
  if (!ficheros.length) return
  evento.preventDefault()
  adjuntar(ficheros)
}

function alArrastrar(evento) {
  if (!admiteImagenes.value || !evento.dataTransfer?.types.includes('Files')) return
  evento.preventDefault()
  arrastrando.value = true
}

function alSoltar(evento) {
  arrastrando.value = false
  if (!admiteImagenes.value) return
  const ficheros = imagenesDe(evento.dataTransfer?.files)
  if (!ficheros.length) return
  evento.preventDefault()
  adjuntar(ficheros)
}
</script>

<template>
  <div
    class="markdown-field"
    :class="{ arrastrando }"
    @paste="alPegar"
    @dragover="alArrastrar"
    @dragleave="arrastrando = false"
    @drop="alSoltar"
  >
    <button
      class="markdown-toggle"
      type="button"
      :aria-pressed="vista"
      :title="vista ? 'Editar Markdown' : 'Previsualizar Markdown'"
      @click="vista = !vista"
    >
      {{ vista ? '✎' : 'M↓' }}
    </button>
    <div v-if="vista" class="markdown-preview md" v-html="html"></div>
    <textarea
      v-else
      ref="area"
      class="markdown-textarea"
      v-model="local"
      :placeholder="placeholder || (admiteImagenes ? 'Puedes pegar (Ctrl+V) o arrastrar imágenes aquí' : '')"
      rows="4"
      @blur="guardar"
    ></textarea>
    <div v-if="!vista" class="markdown-preview-print md" v-html="html"></div>
    <p v-if="subiendo" class="aviso">Subiendo imagen…</p>
    <p v-if="error" class="aviso error">{{ error }}</p>
  </div>
</template>

<style scoped>
.markdown-field {
  position: relative;
}

.markdown-toggle {
  position: absolute;
  z-index: 1;
  top: 5px;
  right: 5px;
  min-width: 28px;
  padding: 1px 5px;
  color: var(--fg-muted);
  background: var(--bg-soft);
  font-family: var(--mono);
  font-size: 11px;
}

.markdown-preview {
  min-height: 76px;
  padding: 8px 36px 8px 9px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--bg);
}

.markdown-preview :deep(p:first-child) {
  margin-top: 0;
}

.markdown-preview :deep(p:last-child) {
  margin-bottom: 0;
}

.markdown-preview :deep(pre) {
  overflow-x: auto;
  padding: 8px;
  background: var(--bg-soft);
}

.markdown-preview :deep(img) {
  max-width: 100%;
}

.arrastrando textarea,
.arrastrando .markdown-preview {
  outline: 2px dashed var(--accent);
  outline-offset: 2px;
}

.aviso {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--fg-muted);
}

.aviso.error {
  color: var(--danger);
}
.markdown-preview-print {
  display: none;
}

@media print {
  .markdown-toggle,
  .markdown-textarea,
  .aviso {
    display: none !important;
  }

  .markdown-preview,
  .markdown-preview-print {
    display: block !important;
    border: none !important;
    padding: 0 !important;
    min-height: 0 !important;
    background: transparent !important;
  }
}
</style>
