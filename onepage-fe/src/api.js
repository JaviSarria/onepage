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
  borrarHijo: (tipo, ruta, id) => request('DELETE', `/${tipo}/${ruta}/item/${id}`)
}
