<script setup>
import { computed, ref, watch } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  valor: { type: String, default: '' },
  placeholder: { type: String, default: '' }
})
const emit = defineEmits(['cambiar'])
const vista = ref(false)
const local = ref(props.valor)

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
</script>

<template>
  <div class="markdown-field">
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
      v-model="local"
      :placeholder="placeholder"
      rows="4"
      @blur="guardar"
    ></textarea>
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
</style>
