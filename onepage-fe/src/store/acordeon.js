import { reactive, ref } from 'vue'

// Estado global de apertura/cierre de las secciones (efecto acordeon).
const abiertos = reactive(new Set())
// Profundidad maxima visible en el indice derecho: 1 = solo secciones de
// primer nivel (# Cabecera, # Requerimiento, # Analisis, ...); 2 o 3 anaden
// subapartados; valores >= 99 devuelven a "todo".
const profundidad = ref(1)
// Tema activo ('light' | 'dark'), sincronizado con document.documentElement.
const tema = ref('light')

export function domId(clave) {
  return 'sec-' + clave.replace(/[^a-zA-Z0-9_-]+/g, '-')
}

export function estaAbierto(clave) {
  return abiertos.has(clave)
}

export function alternar(clave) {
  if (abiertos.has(clave)) abiertos.delete(clave)
  else abiertos.add(clave)
}

export function abrir(clave) {
  const partes = clave.split('/')
  for (let i = 1; i <= partes.length; i++) abiertos.add(partes.slice(0, i).join('/'))
}

export function abrirTodo(claves) {
  claves.forEach((c) => abiertos.add(c))
}

export function cerrarTodo() {
  abiertos.clear()
}

export function irA(clave) {
  abrir(clave)
  requestAnimationFrame(() => {
    const el = document.getElementById(domId(clave))
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
      el.classList.remove('destacado-temporal')
      void el.offsetWidth
      el.classList.add('destacado-temporal')
      setTimeout(() => el.classList.remove('destacado-temporal'), 2600)
    }
  })
}

// Clave (ruta) de la seccion o campo en foco: la mas profunda abierta hoy.
export function claveActual() {
  let maxima = ''
  let maximaProfundidad = 0
  for (const clave of abiertos) {
    const prof = clave ? clave.split('/').length : 0
    const esMasProfunda = prof > maximaProfundidad || (prof === maximaProfundidad && clave.length > maxima.length)
    if (esMasProfunda) {
      maxima = clave
      maximaProfundidad = prof
    }
  }
  return maxima
}

export function getProfundidad() {
  return profundidad.value
}

export function setProfundidad(valor) {
  profundidad.value = valor
}

export function getTema() {
  return tema.value
}

export function setTema(valor) {
  tema.value = valor
}
