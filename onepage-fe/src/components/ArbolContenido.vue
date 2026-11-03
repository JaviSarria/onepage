<script setup>
import { computed, reactive } from 'vue'
import { claveActual, estaAbierto, irA } from '../store/acordeon.js'

const props = defineProps({
  nodos: { type: Array, default: () => [] },
  nivel: { type: Number, default: 1 },
  expandidos: { type: Set, default: null },
  contraidos: { type: Set, default: null }
})

const expandidosLocales = reactive(new Set())
const contraidosLocales = reactive(new Set())
const expandidos = computed(() => props.expandidos || expandidosLocales)
const contraidos = computed(() => props.contraidos || contraidosLocales)
const actual = computed(() => claveActual())

function debeExpandir(nodo) {
  if (contraidos.value.has(nodo.clave)) return false
  return expandidos.value.has(nodo.clave) ||
    (Boolean(actual.value) && actual.value.startsWith(nodo.clave + '/'))
}

function alternarExpandido(clave) {
  if (debeExpandir({ clave })) {
    expandidos.value.delete(clave)
    contraidos.value.add(clave)
  } else {
    contraidos.value.delete(clave)
    expandidos.value.add(clave)
  }
}
</script>

<template>
  <ul :role="nivel === 1 ? 'tree' : 'group'" class="indice">
    <li v-for="n in nodos" :key="n.clave" role="treeitem">
      <div class="fila">
        <button
          v-if="n.hijos && n.hijos.length"
          type="button"
          class="alternar"
          :aria-expanded="debeExpandir(n)"
          :aria-label="`${debeExpandir(n) ? 'Contraer' : 'Expandir'} ${n.titulo}`"
          @click="alternarExpandido(n.clave)"
        >{{ debeExpandir(n) ? '−' : '+' }}</button>
        <span v-else class="alternar vacio" aria-hidden="true"></span>
        <button
        type="button"
        class="enlace"
        :class="{ activo: estaAbierto(n.clave), raiz: nivel === 1 }"
        @click="irA(n.clave)"
      >
        {{ n.titulo }}
        </button>
      </div>
      <ArbolContenido
        v-if="n.hijos && n.hijos.length && debeExpandir(n)"
        :nodos="n.hijos"
        :nivel="nivel + 1"
        :expandidos="expandidos"
        :contraidos="contraidos"
      />
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

.fila {
  display: flex;
  align-items: center;
}

.alternar {
  flex: 0 0 18px;
  width: 18px;
  height: 22px;
  padding: 0;
  border: 0;
  background: none;
  color: var(--fg-muted);
  cursor: pointer;
  font-size: 15px;
  line-height: 1;
}

.alternar:hover {
  color: var(--accent);
}

.alternar.vacio {
  display: inline-block;
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
