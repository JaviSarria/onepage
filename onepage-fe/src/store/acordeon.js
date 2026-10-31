import { reactive } from 'vue'

// Estado global de apertura/cierre de las secciones (efecto acordeon).
const abiertos = reactive(new Set())

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
