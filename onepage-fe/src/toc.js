// Construye el arbol de subsecciones del documento actual (indice de navegacion derecho).

function nodoHijo(nodo, datos, claveBase) {
  const clave = `${claveBase}/${nodo.id}`
  if (nodo.tipo === 'entidades') {
    const items = datos?.[nodo.recurso] || []
    return {
      clave,
      titulo: nodo.titulo,
      hijos: items.map((item) => ({
        clave: `${clave}/${item.id}`,
        titulo: nodo.clave ? nodo.clave(item) : `#${item.id}`,
        hijos: (nodo.hijos || []).map((h) => nodoHijo(h, item, `${clave}/${item.id}`))
      }))
    }
  }
  return { clave, titulo: nodo.titulo, hijos: [] }
}

export function construirIndice(esquema, doc) {
  const raiz = [{ clave: 'doc/cabecera', titulo: 'Cabecera', hijos: [] }]
  for (const seccion of esquema.secciones) {
    const clave = `doc/${seccion.id}`
    raiz.push({
      clave,
      titulo: seccion.titulo,
      hijos: seccion.hijos.map((h) => nodoHijo(h, doc, clave))
    })
  }
  return raiz
}

export function todasLasClaves(nodos) {
  const acc = []
  const visita = (ns) =>
    ns.forEach((n) => {
      acc.push(n.clave)
      visita(n.hijos || [])
    })
  visita(nodos)
  return acc
}
