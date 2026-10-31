<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { api } from '../api.js'

const props = defineProps({
  consultaInicial: { type: String, default: '' },
  tipoInicial: { type: String, default: 'todos' }
})

const emit = defineEmits(['abrir', 'cerrar', 'error'])

const texto = ref(props.consultaInicial || '')
const tipoSeleccionado = ref(props.tipoInicial || 'todos')
const cargando = ref(false)
const haBuscado = ref(false)
const resultados = ref([])
const terminoEjecutado = ref('')
const agruparPorDoc = ref(true)

const inputRef = ref(null)

function escaparHtml(str) {
  return (str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function fragmentoResaltado(fragmento, query) {
  if (!fragmento) return ''
  const seguro = escaparHtml(fragmento)
  const q = (query || '').trim()
  if (!q) return seguro

  const palabras = q.split(/\s+/).filter(Boolean)
  if (!palabras.length) return seguro

  const patron = palabras
    .map((p) => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
    .join('|')
  const regex = new RegExp(`(${patron})`, 'gi')
  return seguro.replace(regex, '<mark class="resaltado">$1</mark>')
}

async function ejecutarBusqueda() {
  const q = texto.value.trim()
  if (!q) {
    resultados.value = []
    haBuscado.value = false
    terminoEjecutado.value = ''
    return
  }

  cargando.value = true
  haBuscado.value = true
  terminoEjecutado.value = q
  try {
    const data = await api.buscar(q, tipoSeleccionado.value)
    resultados.value = data || []
  } catch (e) {
    emit('error', `Error al buscar: ${e.message}`)
    resultados.value = []
  } finally {
    cargando.value = false
  }
}

function limpiar() {
  texto.value = ''
  resultados.value = []
  haBuscado.value = false
  terminoEjecutado.value = ''
  if (inputRef.value) inputRef.value.focus()
}

function cambiarFiltroTipo(nuevoTipo) {
  tipoSeleccionado.value = nuevoTipo
  if (texto.value.trim()) {
    ejecutarBusqueda()
  }
}

const conteosPorTipo = computed(() => {
  const c = { todos: resultados.value.length, evolutivos: 0, incidencias: 0, proyectos: 0 }
  for (const r of resultados.value) {
    if (c[r.tipo] !== undefined) c[r.tipo]++
  }
  return c
})

const resultadosFiltrados = computed(() => {
  if (tipoSeleccionado.value === 'todos') return resultados.value
  return resultados.value.filter((r) => r.tipo === tipoSeleccionado.value)
})

// Agrupación de resultados por documento o proyecto
const resultadosAgrupados = computed(() => {
  const grupos = []
  const mapa = new Map()

  for (const r of resultadosFiltrados.value) {
    const claveGrupo =
      r.tipo === 'proyectos'
        ? `proyecto-${r.proyecto_id}`
        : `${r.tipo}-${r.documento_id}`

    if (!mapa.has(claveGrupo)) {
      const grupo = {
        clave: claveGrupo,
        tipo: r.tipo,
        proyectoId: r.proyecto_id,
        proyectoNombre: r.proyecto_nombre,
        documentoId: r.documento_id,
        documentoCodigo: r.documento_codigo,
        documentoTitulo: r.documento_titulo,
        items: []
      }
      mapa.set(claveGrupo, grupo)
      grupos.push(grupo)
    }
    mapa.get(claveGrupo).items.push(r)
  }

  return grupos
})

const totalDocumentos = computed(() => resultadosAgrupados.value.length)

function irAResultado(r) {
  if (r.tipo === 'proyectos') {
    emit('abrir', { tipo: 'proyecto', id: r.proyecto_id, termino: terminoEjecutado.value })
  } else {
    emit('abrir', {
      tipo: r.tipo,
      id: r.documento_id,
      proyecto: r.proyecto_id,
      saltarA: r.clave_acordeon,
      termino: terminoEjecutado.value
    })
  }
}

function iconoTipo(tipo) {
  if (tipo === 'proyectos') return '📁'
  if (tipo === 'evolutivos') return '🧩'
  if (tipo === 'incidencias') return '🐞'
  return '📄'
}

function etiquetaTipo(tipo) {
  if (tipo === 'proyectos') return 'Proyecto'
  if (tipo === 'evolutivos') return 'Evolutivo'
  if (tipo === 'incidencias') return 'Incidencia'
  return tipo
}

watch(
  () => props.consultaInicial,
  (nueva) => {
    if (nueva && nueva !== texto.value) {
      texto.value = nueva
      ejecutarBusqueda()
    }
  }
)

onMounted(() => {
  if (inputRef.value) inputRef.value.focus()
  if (texto.value.trim()) {
    ejecutarBusqueda()
  }
})
</script>

<template>
  <div class="vista-busqueda md">
    <!-- Zona de Búsqueda -->
    <header class="zona-busqueda">
      <div class="barra-titulo">
        <h1>Búsqueda global</h1>
        <button
          v-if="haBuscado"
          type="button"
          class="boton-cerrar"
          title="Cerrar búsqueda y volver"
          @click="emit('cerrar')"
        >
          ✕ Cerrar
        </button>
      </div>

      <p class="descripcion-zona">
        Busca texto en toda la aplicación: proyectos, evolutivos, incidencias, tareas, requisitos,
        criterios, notas de reuniones y partes diarios.
      </p>

      <form class="formulario-busqueda" @submit.prevent="ejecutarBusqueda">
        <div class="campo-con-icono">
          <span class="icono-lupa" aria-hidden="true">🔍</span>
          <input
            ref="inputRef"
            v-model="texto"
            type="search"
            class="entrada-busqueda"
            placeholder="Escribe el texto a buscar... (ej: autenticación, Stripe, TAR-01, LDAP)"
            autocomplete="off"
            @keydown.esc="limpiar"
          />
          <button
            v-if="texto"
            type="button"
            class="boton-limpiar"
            title="Borrar texto"
            aria-label="Borrar texto"
            @click="limpiar"
          >
            ✕
          </button>
        </div>
        <button type="submit" class="primario boton-buscar" :disabled="cargando || !texto.trim()">
          {{ cargando ? 'Buscando...' : 'Buscar' }}
        </button>
      </form>

      <!-- Filtros por tipo -->
      <div class="filtros-tipo">
        <span class="etiqueta-filtros">Filtrar por ámbito:</span>
        <div class="botones-pildoras" role="tablist">
          <button
            type="button"
            class="pildora"
            :class="{ activa: tipoSeleccionado === 'todos' }"
            @click="cambiarFiltroTipo('todos')"
          >
            Todos
            <span v-if="haBuscado" class="contador-pildora">{{ conteosPorTipo.todos }}</span>
          </button>
          <button
            type="button"
            class="pildora"
            :class="{ activa: tipoSeleccionado === 'evolutivos' }"
            @click="cambiarFiltroTipo('evolutivos')"
          >
            🧩 Evolutivos
            <span v-if="haBuscado" class="contador-pildora">{{ conteosPorTipo.evolutivos }}</span>
          </button>
          <button
            type="button"
            class="pildora"
            :class="{ activa: tipoSeleccionado === 'incidencias' }"
            @click="cambiarFiltroTipo('incidencias')"
          >
            🐞 Incidencias
            <span v-if="haBuscado" class="contador-pildora">{{ conteosPorTipo.incidencias }}</span>
          </button>
          <button
            type="button"
            class="pildora"
            :class="{ activa: tipoSeleccionado === 'proyectos' }"
            @click="cambiarFiltroTipo('proyectos')"
          >
            📁 Proyectos
            <span v-if="haBuscado" class="contador-pildora">{{ conteosPorTipo.proyectos }}</span>
          </button>
        </div>
      </div>
    </header>

    <hr class="separador" />

    <!-- Zona de Resultados -->
    <section class="zona-resultados" aria-label="Resultados de la búsqueda">
      <!-- Indicador de carga -->
      <div v-if="cargando" class="estado-cargando">
        <span class="animacion-giro">⏳</span> Buscando coincidencias en todos los documentos...
      </div>

      <!-- Estado inicial sin buscar -->
      <div v-else-if="!haBuscado" class="estado-inicial">
        <div class="icono-estado">🔍</div>
        <h3>Encuentra cualquier término al instante</h3>
        <p>
          Introduce una palabra clave en el campo superior. La búsqueda inspecciona todos los
          campos narrativos, tablas, checklists y subsecciones de tus proyectos.
        </p>
        <div class="sugerencias">
          <strong>Ejemplos útiles:</strong>
          <ul>
            <li>Códigos de tareas o requisitos: <code>REQ-01</code>, <code>TAR-03</code>, <code>CA-02</code></li>
            <li>Tecnologías o herramientas: <code>Docker</code>, <code>JWT</code>, <code>PostgreSQL</code></li>
            <li>Estados o entornos: <code>Bloqueada</code>, <code>PROD</code>, <code>Crítica</code></li>
            <li>Personas responsables o fechas</li>
          </ul>
        </div>
      </div>

      <!-- Estado sin resultados -->
      <div v-else-if="resultadosFiltrados.length === 0" class="estado-sin-resultados">
        <div class="icono-estado">📋</div>
        <h3>No se encontraron coincidencias para «{{ terminoEjecutado }}»</h3>
        <p>
          Comprueba la ortografía del término o selecciona otro filtro de ámbito arriba.
        </p>
      </div>

      <!-- Listado de resultados -->
      <div v-else class="listado-resultados">
        <div class="barra-resumen">
          <span class="conteo-total">
            Se encontraron <strong>{{ resultadosFiltrados.length }}</strong> coincidencias en
            <strong>{{ totalDocumentos }}</strong> documento{{ totalDocumentos === 1 ? '' : 's' }}.
          </span>
          <label class="opcion-agrupar">
            <input v-model="agruparPorDoc" type="checkbox" />
            Agrupar por documento
          </label>
        </div>

        <!-- Vista agrupada por documento -->
        <div v-if="agruparPorDoc" class="grupos-documentos">
          <article
            v-for="grupo in resultadosAgrupados"
            :key="grupo.clave"
            class="tarjeta-documento"
          >
            <header class="cabecera-grupo">
              <span class="icono-doc">{{ iconoTipo(grupo.tipo) }}</span>
              <div class="titulos-grupo">
                <span class="miga-proyecto">
                  📁 {{ grupo.proyectoNombre || 'Proyecto' }}
                </span>
                <h3 class="titulo-doc">
                  <span v-if="grupo.documentoCodigo" class="codigo-doc">
                    {{ grupo.documentoCodigo }}
                  </span>
                  {{ grupo.documentoTitulo }}
                </h3>
              </div>
              <span class="insignia-conteo">
                {{ grupo.items.length }} coincidencia{{ grupo.items.length === 1 ? '' : 's' }}
              </span>
            </header>

            <ul class="items-coincidencia">
              <li
                v-for="item in grupo.items"
                :key="item.id"
                class="item-resultado"
                tabindex="0"
                @click="irAResultado(item)"
                @keydown.enter="irAResultado(item)"
              >
                <div class="metadatos-item">
                  <span class="etiqueta-seccion">{{ item.seccion }}</span>
                  <span class="etiqueta-campo">Campo: {{ item.campo }}</span>
                  <span v-if="item.coincidencias > 1" class="insignia-repeticiones">
                    {{ item.coincidencias }} veces
                  </span>
                </div>
                <div
                  class="fragmento-texto"
                  v-html="fragmentoResaltado(item.fragmento, terminoEjecutado)"
                ></div>
                <div class="accion-ir">
                  <button type="button" class="enlace-ir" @click.stop="irAResultado(item)">
                    Ver en el documento →
                  </button>
                </div>
              </li>
            </ul>
          </article>
        </div>

        <!-- Vista plana (lista continua) -->
        <div v-else class="lista-plana">
          <article
            v-for="item in resultadosFiltrados"
            :key="item.id"
            class="item-resultado plano"
            tabindex="0"
            @click="irAResultado(item)"
            @keydown.enter="irAResultado(item)"
          >
            <div class="encabezado-plano">
              <span class="icono-tipo">{{ iconoTipo(item.tipo) }}</span>
              <span class="miga-plana">
                📁 {{ item.proyecto_nombre || 'Proyecto' }} ›
                <strong v-if="item.documento_codigo">{{ item.documento_codigo }}</strong>
                {{ item.documento_titulo }}
              </span>
            </div>
            <div class="metadatos-item">
              <span class="etiqueta-seccion">{{ item.seccion }}</span>
              <span class="etiqueta-campo">Campo: {{ item.campo }}</span>
            </div>
            <div
              class="fragmento-texto"
              v-html="fragmentoResaltado(item.fragmento, terminoEjecutado)"
            ></div>
            <div class="accion-ir">
              <button type="button" class="enlace-ir" @click.stop="irAResultado(item)">
                Ver en el documento →
              </button>
            </div>
          </article>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.vista-busqueda {
  padding: 24px 32px 60px;
  max-width: 980px;
  margin: 0 auto;
}

.zona-busqueda {
  margin-bottom: 16px;
}

.barra-titulo {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.barra-titulo h1 {
  font-size: 24px;
  margin: 0;
}

.boton-cerrar {
  font-size: 13px;
  color: var(--fg-muted);
}

.descripcion-zona {
  color: var(--fg-muted);
  font-size: 14px;
  margin: 0 0 16px;
}

.formulario-busqueda {
  display: flex;
  gap: 10px;
  align-items: center;
}

.campo-con-icono {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}

.icono-lupa {
  position: absolute;
  left: 12px;
  pointer-events: none;
  font-size: 16px;
  color: var(--fg-muted);
}

.entrada-busqueda {
  padding: 9px 36px 9px 38px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid var(--border);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.entrada-busqueda:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-soft);
}

.boton-limpiar {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  color: var(--fg-muted);
  padding: 4px;
  font-size: 14px;
}

.boton-limpiar:hover {
  background: transparent;
  color: var(--fg);
}

.boton-buscar {
  padding: 9px 20px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 8px;
  white-space: nowrap;
}

.filtros-tipo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 14px;
  flex-wrap: wrap;
}

.etiqueta-filtros {
  font-size: 13px;
  font-weight: 500;
  color: var(--fg-muted);
}

.botones-pildoras {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pildora {
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 13px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.15s ease;
}

.pildora.activa {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

.contador-pildora {
  font-size: 11px;
  background: rgba(0, 0, 0, 0.08);
  padding: 1px 6px;
  border-radius: 10px;
}

.pildora.activa .contador-pildora {
  background: rgba(255, 255, 255, 0.25);
  color: #fff;
}

.zona-resultados {
  margin-top: 20px;
}

.estado-cargando,
.estado-inicial,
.estado-sin-resultados {
  text-align: center;
  padding: 40px 20px;
  background: var(--bg-soft);
  border: 1px dashed var(--border);
  border-radius: 8px;
  color: var(--fg-muted);
}

.icono-estado {
  font-size: 36px;
  margin-bottom: 12px;
}

.estado-inicial h3,
.estado-sin-resultados h3 {
  color: var(--fg);
  margin-bottom: 8px;
}

.sugerencias {
  margin-top: 20px;
  text-align: left;
  display: inline-block;
  background: var(--bg);
  padding: 14px 20px;
  border-radius: 6px;
  border: 1px solid var(--border-soft);
  font-size: 13px;
}

.sugerencias ul {
  margin: 6px 0 0 20px;
  padding: 0;
}

.barra-resumen {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 14px;
}

.opcion-agrupar {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--fg-muted);
  cursor: pointer;
}

.opcion-agrupar input {
  width: auto;
  cursor: pointer;
}

.grupos-documentos {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tarjeta-documento {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.cabecera-grupo {
  background: var(--bg-soft);
  border-bottom: 1px solid var(--border);
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.icono-doc {
  font-size: 20px;
}

.titulos-grupo {
  flex: 1;
}

.miga-proyecto {
  font-size: 12px;
  color: var(--fg-muted);
  display: block;
}

.titulo-doc {
  font-size: 15px;
  margin: 0;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.codigo-doc {
  font-family: var(--mono);
  font-size: 12px;
  padding: 1px 6px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 4px;
}

.insignia-conteo {
  font-size: 12px;
  color: var(--fg-muted);
  background: var(--bg);
  padding: 2px 8px;
  border-radius: 12px;
  border: 1px solid var(--border-soft);
}

.items-coincidencia {
  list-style: none;
  margin: 0;
  padding: 0;
}

.item-resultado {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-soft);
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.item-resultado:last-child {
  border-bottom: none;
}

.item-resultado:hover,
.item-resultado:focus {
  background-color: #f3f7fa;
  outline: none;
}

.item-resultado.plano {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 12px;
}

.encabezado-plano {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  margin-bottom: 6px;
}

.miga-plana {
  color: var(--fg-muted);
}

.metadatos-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 12px;
}

.etiqueta-seccion {
  background: var(--accent-soft);
  color: var(--accent);
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.etiqueta-campo {
  color: var(--fg-muted);
  background: var(--bg-soft);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--border-soft);
}

.insignia-repeticiones {
  font-size: 11px;
  color: var(--warn);
  font-weight: 600;
}

.fragmento-texto {
  font-family: var(--mono);
  font-size: 13px;
  line-height: 1.5;
  color: var(--fg);
  background: var(--bg-soft);
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid var(--border-soft);
  word-break: break-word;
}

.accion-ir {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}

.enlace-ir {
  background: transparent;
  border: none;
  color: var(--accent);
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  cursor: pointer;
}

.enlace-ir:hover {
  text-decoration: underline;
  background: transparent;
}
</style>
