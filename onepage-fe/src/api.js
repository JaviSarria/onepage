const BASE = import.meta.env.VITE_API_URL || '/api'

async function request(method, url, body) {
  const res = await fetch(BASE + url, {
    method,
    headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body)
  })
  if (!res.ok) {
    const detalle = await res.text()
    throw new Error(`${method} ${url} -> ${res.status}: ${detalle}`)
  }
  return res.status === 204 ? null : res.json()
}

export const api = {
  arbol: () => request('GET', '/arbol'),
  diario: () => request('GET', '/diario'),
  buscar: (q, tipo = 'todos', limite = 150) =>
    request(
      'GET',
      `/buscar?q=${encodeURIComponent(q)}&tipo=${encodeURIComponent(tipo)}&limite=${limite}`
    ),

  proyectos: () => request('GET', '/proyectos'),
  crearProyecto: (data) => request('POST', '/proyectos', data),
  actualizarProyecto: (id, data) => request('PUT', `/proyectos/${id}`, data),
  borrarProyecto: (id) => request('DELETE', `/proyectos/${id}`),

  documento: (tipo, id) => request('GET', `/${tipo}/${id}/full`),
  crearDocumento: (tipo, data) => request('POST', `/${tipo}`, data),
  actualizarDocumento: (tipo, id, data) => request('PUT', `/${tipo}/${id}`, data),
  borrarDocumento: (tipo, id) => request('DELETE', `/${tipo}/${id}`),

  crearHijo: (tipo, ruta, parentId, data, rutaPadre = null) =>
    request('POST', `/${tipo}${rutaPadre ? '/' + rutaPadre : ''}/${parentId}/${ruta}`, data),
  actualizarHijo: (tipo, ruta, id, data) => request('PUT', `/${tipo}/${ruta}/item/${id}`, data),
  borrarHijo: (tipo, ruta, id) => request('DELETE', `/${tipo}/${ruta}/item/${id}`),

  async subirImagen(tipo, docId, seccion, fichero) {
    const ext = (
      fichero.name?.includes('.') ? fichero.name.split('.').pop() : fichero.type.split('/').pop()
    ).toLowerCase()
    const params = new URLSearchParams({ tipo, doc_id: docId, seccion, ext })
    const res = await fetch(`${BASE}/assets?${params}`, {
      method: 'POST',
      headers: { 'Content-Type': fichero.type || 'application/octet-stream' },
      body: fichero
    })
    if (!res.ok) throw new Error(`No se pudo subir la imagen: ${await res.text()}`)
    const { nombre } = await res.json()
    return { nombre, url: `${BASE}/assets/${nombre}` }
  }
}
