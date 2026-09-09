<script setup>
import { ref } from 'vue'

const props = defineProps({
  nodos: { type: Array, default: () => [] },
  seleccion: { type: Object, default: null }
})
const emit = defineEmits(['seleccionar', 'nuevo-proyecto', 'nuevo-documento', 'borrar-proyecto'])

const abiertos = ref(new Set())
const filtro = ref('')

function alternar(id) {
  const s = new Set(abiertos.value)
  s.has(id) ? s.delete(id) : s.add(id)
  abiertos.value = s
}

function coincide(texto) {
  return !filtro.value || (texto || '').toLowerCase().includes(filtro.value.toLowerCase())
}

function docsVisibles(proyecto, clase) {
  return proyecto[clase].filter((d) => coincide(d.titulo) || coincide(d.codigo))
}

function proyectosVisibles() {
  if (!filtro.value) return props.nodos
  return props.nodos.filter(
    (p) =>
      coincide(p.nombre) ||
      docsVisibles(p, 'evolutivos').length ||
      docsVisibles(p, 'incidencias').length
  )
}

function activo(tipo, id) {
  return props.seleccion && props.seleccion.tipo === tipo && props.seleccion.id === id
}
</script>

<template>
  <nav class="arbol" aria-label="Proyectos">
    <header>
      <h2>Proyectos</h2>
      <button type="button" class="primario" @click="emit('nuevo-proyecto')">+</button>
    </header>
    <input v-model="filtro" type="search" placeholder="Filtrar..." class="filtro" />

    <ul role="tree">
      <li v-for="p in proyectosVisibles()" :key="p.id" role="treeitem" :aria-expanded="abiertos.has(p.id)">
        <div class="nodo nivel-1" :class="{ activo: activo('proyecto', p.id) }">
          <button class="giro" type="button" @click="alternar(p.id)">
            <span :class="{ abierto: abiertos.has(p.id) }">▸</span>
          </button>
          <button class="titulo" type="button" @click="emit('seleccionar', { tipo: 'proyecto', id: p.id })">
            📁 {{ p.nombre }}
          </button>
          <button class="peligro mini" type="button" title="Eliminar proyecto" @click="emit('borrar-proyecto', p)">
            ✕
          </button>
        </div>

        <ul v-show="abiertos.has(p.id)" role="group">
          <li v-for="clase in ['evolutivos', 'incidencias']" :key="clase" role="treeitem">
            <div class="nodo nivel-2">
              <span class="icono">{{ clase === 'evolutivos' ? '🧩' : '🐞' }}</span>
              <span class="titulo estatico">{{ clase === 'evolutivos' ? 'Evolutivos' : 'Incidencias' }}</span>
              <button
                class="mini"
                type="button"
                title="Nuevo"
                @click="emit('nuevo-documento', { proyecto: p, tipo: clase })"
              >
                +
              </button>
            </div>
            <ul role="group">
              <li v-for="d in docsVisibles(p, clase)" :key="d.id" role="treeitem">
                <div class="nodo nivel-3" :class="{ activo: activo(clase, d.id) }">
                  <button
                    class="titulo"
                    type="button"
                    @click="emit('seleccionar', { tipo: clase, id: d.id, proyecto: p.id })"
                  >
                    <span class="codigo">{{ d.codigo || '—' }}</span> {{ d.titulo }}
                  </button>
                </div>
              </li>
              <li v-if="!docsVisibles(p, clase).length" class="vacio">sin elementos</li>
            </ul>
          </li>
        </ul>
      </li>
      <li v-if="!proyectosVisibles().length" class="vacio">No hay proyectos</li>
    </ul>
  </nav>
</template>

<style scoped>
.arbol {
  padding: 12px;
  font-size: 13px;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

h2 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--fg-muted);
  margin: 0;
}

.filtro {
  margin-bottom: 10px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0 0 0 10px;
}

ul[role='tree'] {
  padding-left: 0;
}

.nodo {
  display: flex;
  align-items: center;
  gap: 4px;
  border-radius: 6px;
  padding: 1px 2px;
}

.nodo:hover {
  background: var(--bg-soft);
}

.nodo.activo {
  background: var(--accent-soft);
}

.titulo {
  flex: 1;
  min-width: 0;
  text-align: left;
  border: 0;
  background: none;
  padding: 2px 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.titulo.estatico {
  color: var(--fg-muted);
  font-weight: 600;
}

.giro,
.mini {
  border: 0;
  background: none;
  padding: 0 4px;
  color: var(--fg-muted);
}

.giro span {
  display: inline-block;
  transition: transform 0.15s ease;
}

.giro span.abierto {
  transform: rotate(90deg);
}

.codigo {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--fg-muted);
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
  padding: 2px 8px;
}
</style>
