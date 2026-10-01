<script setup>
import { computed, onMounted, ref } from 'vue'
import { marked } from 'marked'
import { api } from '../api.js'
import { COLORES_SECCION } from '../schema.js'
import { abrirTodo } from '../store/acordeon.js'
import Acordeon from './Acordeon.vue'

const emit = defineEmits(['abrir', 'error'])
const partes = ref([])
const cargando = ref(false)
const colorSeguimiento = COLORES_SECCION.seguimiento

const markdown = (texto) => marked.parse(texto || '', { breaks: true })
const claveDia = (dia) => 'diario/' + dia.clave.replace(/\//g, '-')
const claveTarea = (dia, parte, tarea) =>
  `${claveDia(dia)}/${parte.documento.tipo}-${parte.id}/${tarea.id}`
const hechas = (lista) => lista.filter((x) => x.completada).length + '/' + lista.length

// Normaliza fechas libres (YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY) a ISO para ordenar y agrupar.
function fechaIso(fecha) {
  const texto = (fecha || '').trim()
  let m = texto.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})/)
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`
  m = texto.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{4})/)
  if (m) return `${m[3]}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}`
  return ''
}

function tituloDia(iso, original) {
  if (!iso) return original || 'Sin fecha'
  const [a, mes, d] = iso.split('-').map(Number)
  const texto = new Date(a, mes - 1, d).toLocaleDateString('es-ES', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
  return texto.charAt(0).toUpperCase() + texto.slice(1)
}

const dias = computed(() => {
  const grupos = new Map()
  for (const parte of partes.value) {
    const iso = fechaIso(parte.fecha)
    const clave = iso || parte.fecha || ''
    if (!grupos.has(clave)) grupos.set(clave, { clave, iso, titulo: tituloDia(iso, parte.fecha), partes: [] })
    grupos.get(clave).partes.push(parte)
  }
  return [...grupos.values()]
    .map((g) => ({ ...g, horas: g.partes.reduce((total, p) => total + (Number(p.tiempo) || 0), 0) }))
    .sort((x, y) => {
      if (x.iso && y.iso) return y.iso.localeCompare(x.iso)
      if (x.iso || y.iso) return x.iso ? -1 : 1
      return x.clave.localeCompare(y.clave)
    })
})

async function cargar() {
  cargando.value = true
  try {
    partes.value = await api.diario()
    if (dias.value.length) abrirTodo([claveDia(dias.value[0])])
  } catch (e) {
    emit('error', e.message)
  } finally {
    cargando.value = false
  }
}

onMounted(cargar)
</script>

<template>
  <section class="diario">
    <h2>Diario de seguimiento</h2>
    <p v-if="cargando" class="vacio">Cargando…</p>
    <p v-else-if="!dias.length" class="vacio">
      No hay partes de seguimiento registrados en evolutivos ni incidencias.
    </p>
    <Acordeon
      v-for="dia in dias"
      :key="dia.clave"
      :clave="claveDia(dia)"
      :titulo="dia.titulo"
      :nivel="3"
      :color="colorSeguimiento"
      :insignia="dia.horas ? `${dia.horas} h` : ''"
    >
      <article
        v-for="parte in dia.partes"
        :key="parte.documento.tipo + parte.id"
        class="parte"
      >
        <header>
          <a href="#" @click.prevent="emit('abrir', { tipo: parte.documento.tipo, id: parte.documento.id })">
            <span class="etiqueta-estado">
              {{ parte.documento.tipo === 'evolutivos' ? 'Evolutivo' : 'Incidencia' }}
            </span>
            <strong v-if="parte.documento.codigo">{{ parte.documento.codigo }}</strong>
            {{ parte.documento.titulo }}
          </a>
          <span class="proyecto">{{ parte.documento.proyecto }}</span>
          <span v-if="parte.tiempo" class="tiempo">{{ parte.tiempo }} h</span>
        </header>
        <Acordeon
          v-for="tarea in parte.tareas"
          :key="tarea.id"
          :clave="claveTarea(dia, parte, tarea)"
          :titulo="(tarea.completada ? '☑ ' : '☐ ') + tarea.nombre"
          :nivel="4"
          :insignia="tarea.actividades.length ? hechas(tarea.actividades) : ''"
          :class="{ hecha: tarea.completada }"
        >
          <div v-if="tarea.descripcion" class="descripcion md" v-html="markdown(tarea.descripcion)"></div>
          <p v-else class="vacio">Sin descripción</p>
          <Acordeon
            v-if="tarea.actividades.length"
            :clave="claveTarea(dia, parte, tarea) + '/actividades'"
            titulo="Actividades"
            :nivel="4"
            :insignia="hechas(tarea.actividades)"
          >
            <ul class="actividades">
              <li v-for="a in tarea.actividades" :key="a.id" :class="{ hecha: a.completada }">
                <span class="marca">{{ a.completada ? '☑' : '☐' }}</span>
                {{ a.descripcion }}
              </li>
            </ul>
          </Acordeon>
        </Acordeon>
        <p v-if="!parte.tareas.length" class="vacio">Sin tareas registradas</p>
        <div v-if="parte.notas" class="notas md" v-html="markdown(parte.notas)"></div>
      </article>
    </Acordeon>
  </section>
</template>

<style scoped>
.diario {
  margin-top: 24px;
}

.parte {
  margin: 0 0 10px;
}

.parte header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 6px;
}

.parte header a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.proyecto,
.tiempo {
  color: var(--fg-muted);
  font-size: 13px;
}

.tiempo {
  margin-left: auto;
}

.actividades {
  list-style: none;
  margin: 0;
  padding-left: 0;
  font-size: 13px;
}

.marca {
  margin-right: 6px;
  color: var(--fg-muted);
}

.hecha > :deep(.cabecera .texto),
.actividades .hecha {
  color: var(--fg-muted);
  text-decoration: line-through;
}

.descripcion {
  margin: 0 0 8px;
  font-size: 14px;
}

.notas {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--fg-muted);
  font-style: italic;
}

.vacio {
  color: var(--fg-muted);
  font-style: italic;
}
</style>
