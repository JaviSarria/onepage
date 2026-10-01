<script setup>
import { computed } from 'vue'
import { alternar, domId, estaAbierto } from '../store/acordeon.js'

const props = defineProps({
  clave: { type: String, required: true },
  titulo: { type: String, required: true },
  nivel: { type: Number, default: 2 },
  insignia: { type: String, default: '' },
  color: { type: Object, default: null }
})

const abierto = computed(() => estaAbierto(props.clave))
const etiqueta = computed(() => 'h' + Math.min(props.nivel, 4))
const estiloColor = computed(() =>
  props.color ? { '--sec-fondo': props.color.fondo, '--sec-borde': props.color.borde } : null
)
</script>

<template>
  <section
    class="acordeon"
    :class="{ coloreado: color }"
    :style="estiloColor"
    :id="domId(clave)"
    :data-nivel="nivel"
  >
    <component :is="etiqueta" class="cabecera">
      <button
        class="disparador"
        type="button"
        :aria-expanded="abierto"
        :aria-controls="domId(clave) + '-panel'"
        @click="alternar(clave)"
      >
        <span class="chevron" :class="{ abierto }" aria-hidden="true">▸</span>
        <span class="texto">{{ titulo }}</span>
        <span v-if="insignia" class="etiqueta-estado">{{ insignia }}</span>
      </button>
      <span class="acciones"><slot name="acciones" /></span>
    </component>
    <div v-show="abierto" class="panel" :id="domId(clave) + '-panel'">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.acordeon {
  margin: 0 0 14px;
  scroll-margin-top: 12px;
}

.cabecera {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 8px;
}

.disparador {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 0;
  background: none;
  padding: 2px 0;
  font: inherit;
  color: inherit;
  text-align: left;
  flex: 1;
  min-width: 0;
}

.disparador:hover {
  background: none;
  color: var(--accent);
}

.chevron {
  transition: transform 0.15s ease;
  color: var(--fg-muted);
  font-size: 12px;
}

.chevron.abierto {
  transform: rotate(90deg);
}

.texto {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.acordeon[data-nivel='2'] > .cabecera,
.acordeon[data-nivel='1'] > .cabecera {
  border-bottom: 1px solid var(--border-soft);
  padding-bottom: 4px;
}

.panel {
  padding-left: 18px;
  border-left: 1px solid var(--border-soft);
  margin-left: 5px;
  animation: desplegar 0.15s ease;
}

.acordeon.coloreado > .cabecera {
  background: var(--sec-fondo);
  border-bottom: 0;
  border-left: 4px solid var(--sec-borde);
  border-radius: 6px;
  padding: 4px 8px;
}

.acordeon.coloreado > .panel {
  border-left: 2px solid var(--sec-borde);
}

@keyframes desplegar {
  from {
    opacity: 0;
    transform: translateY(-3px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
</style>
