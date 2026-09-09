<script setup>
import { estaAbierto, irA } from '../store/acordeon.js'

defineProps({
  nodos: { type: Array, default: () => [] },
  nivel: { type: Number, default: 1 }
})
</script>

<template>
  <ul :role="nivel === 1 ? 'tree' : 'group'" class="indice">
    <li v-for="n in nodos" :key="n.clave" role="treeitem" :aria-expanded="estaAbierto(n.clave)">
      <button
        type="button"
        class="enlace"
        :class="{ activo: estaAbierto(n.clave), raiz: nivel === 1 }"
        @click="irA(n.clave)"
      >
        {{ n.titulo }}
      </button>
      <ArbolContenido v-if="n.hijos && n.hijos.length" :nodos="n.hijos" :nivel="nivel + 1" />
    </li>
  </ul>
</template>

<script>
export default { name: 'ArbolContenido' }
</script>

<style scoped>
.indice {
  list-style: none;
  margin: 0;
  padding-left: 10px;
}

.enlace {
  display: block;
  width: 100%;
  text-align: left;
  border: 0;
  border-left: 2px solid transparent;
  background: none;
  padding: 2px 6px;
  font-size: 12.5px;
  color: var(--fg-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.enlace.raiz {
  font-weight: 600;
  color: var(--fg);
}

.enlace:hover {
  color: var(--accent);
  background: none;
}

.enlace.activo {
  border-left-color: var(--accent);
  color: var(--fg);
}
</style>
