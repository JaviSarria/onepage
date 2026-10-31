"""Router de busqueda global en cualquier parte de la aplicacion."""

from __future__ import annotations

import re
from typing import Any
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_evolutivos_db, get_incidencias_db
from ..models import evolutivo as me
from ..models import incidencia as mi

router = APIRouter(prefix="/api", tags=["busqueda"])


class ResultadoBusqueda(BaseModel):
    id: str
    tipo: str  # "proyectos", "evolutivos", "incidencias"
    proyecto_id: str
    proyecto_nombre: str
    documento_id: int | None = None
    documento_codigo: str = ""
    documento_titulo: str = ""
    seccion: str
    campo: str
    clave_acordeon: str = ""
    fragmento: str
    coincidencias: int = 1


def extraer_fragmento(texto: str, query: str, radio: int = 60) -> str:
    """Extrae un fragmento legible con contexto alrededor de la coincidencia."""
    if not texto:
        return ""
    texto_una_linea = re.sub(r"\s+", " ", texto).strip()
    idx = texto_una_linea.lower().find(query.lower())
    if idx == -1:
        if len(texto_una_linea) > radio * 2:
            return texto_una_linea[: radio * 2].rstrip() + "..."
        return texto_una_linea

    inicio = max(0, idx - radio)
    fin = min(len(texto_una_linea), idx + len(query) + radio)

    # Ajuste suave a palabras
    if inicio > 0:
        espacio = texto_una_linea.find(" ", inicio)
        if espacio != -1 and espacio < idx:
            inicio = espacio + 1
    if fin < len(texto_una_linea):
        espacio = texto_una_linea.rfind(" ", idx + len(query), fin)
        if espacio != -1:
            fin = espacio

    frag = texto_una_linea[inicio:fin].strip()
    if inicio > 0:
        frag = "..." + frag
    if fin < len(texto_una_linea):
        frag = frag + "..."
    return frag


def _escapar_like(query: str) -> str:
    return query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def buscar_en_proyectos(
    db: Session, query: str, limite: int
) -> list[ResultadoBusqueda]:
    patron = f"%{_escapar_like(query)}%"
    campos = [
        ("nombre", "Nombre"),
        ("descripcion", "Descripción"),
        ("responsable", "Responsable"),
        ("estado", "Estado"),
    ]
    condiciones = [getattr(me.Proyecto, c[0]).ilike(patron, escape="\\") for c in campos]
    proyectos = db.query(me.Proyecto).filter(or_(*condiciones)).limit(limite).all()

    resultados: list[ResultadoBusqueda] = []
    q_baja = query.lower()
    for p in proyectos:
        for attr, etiqueta in campos:
            val = getattr(p, attr) or ""
            if q_baja in val.lower():
                resultados.append(
                    ResultadoBusqueda(
                        id=f"proj-{p.id}-{attr}",
                        tipo="proyectos",
                        proyecto_id=p.id,
                        proyecto_nombre=p.nombre,
                        documento_id=None,
                        documento_codigo="",
                        documento_titulo=p.nombre,
                        seccion="Ficha del proyecto",
                        campo=etiqueta,
                        clave_acordeon="",
                        fragmento=extraer_fragmento(val, query),
                        coincidencias=val.lower().count(q_baja),
                    )
                )
    return resultados


def _buscar_en_documentos(
    db: Session,
    query: str,
    doc_model: type,
    tipo_doc: str,
    proyectos_map: dict[str, str],
    limite: int,
    especificos_narrativos: list[tuple[str, str, str, str]],
) -> list[ResultadoBusqueda]:
    patron = f"%{_escapar_like(query)}%"
    q_baja = query.lower()

    # Campos comunes de cabecera y narrativos
    campos_cabecera = [
        ("codigo", "Código", "Cabecera", "doc/cabecera"),
        ("titulo", "Título", "Cabecera", "doc/cabecera"),
        ("estado", "Estado", "Cabecera", "doc/cabecera"),
        ("responsable", "Responsable", "Cabecera", "doc/cabecera"),
        ("prioridad", "Prioridad", "Cabecera", "doc/cabecera"),
        ("version", "Versión", "Cabecera", "doc/cabecera"),
        ("fecha_objetivo", "Fecha objetivo", "Cabecera", "doc/cabecera"),
        ("commits", "Commits", "Cabecera", "doc/cabecera"),
        ("despliegues", "Despliegues", "Cabecera", "doc/cabecera"),
        ("incidencias", "Incidencias vinculadas", "Cabecera", "doc/cabecera"),
        ("resumen", "Resumen", "Resumen", "doc/requerimiento" if tipo_doc == "evolutivos" else "doc/problema"),
        ("investigacion_previa", "Investigación previa", "Análisis › Investigación", "doc/analisis"),
        ("fuera_alcance", "Fuera de alcance", "Análisis › Alcance", "doc/analisis"),
        ("supuestos_restricciones", "Supuestos y restricciones", "Análisis › Supuestos", "doc/analisis"),
        ("dependencias", "Dependencias", "Planificación › Dependencias", "doc/planificacion"),
        ("riesgos_mitigacion", "Riesgos y mitigación", "Planificación › Riesgos", "doc/planificacion"),
        ("decisiones_pendientes", "Decisiones pendientes", "Planificación › Decisiones", "doc/planificacion"),
        ("descripcion_solucion", "Descripción de la solución", "Desarrollo › Solución", "doc/desarrollo"),
        ("datos_pruebas", "Datos de pruebas", "Pruebas › Datos", "doc/pruebas"),
        ("modulos_afectados", "Módulos afectados", "Desarrollo › Módulos", "doc/desarrollo"),
        ("migracion_datos", "Migración de datos", "Desarrollo › Migración", "doc/desarrollo"),
    ] + especificos_narrativos

    condiciones = [
        getattr(doc_model, c[0]).ilike(patron, escape="\\")
        for c in campos_cabecera
        if hasattr(doc_model, c[0])
    ]
    docs = db.query(doc_model).filter(or_(*condiciones)).limit(limite).all()

    resultados: list[ResultadoBusqueda] = []
    for d in docs:
        p_nombre = proyectos_map.get(d.proyecto_id, "")
        for attr, etiqueta, seccion, clave in campos_cabecera:
            if not hasattr(d, attr):
                continue
            val = getattr(d, attr) or ""
            if q_baja in val.lower():
                resultados.append(
                    ResultadoBusqueda(
                        id=f"{tipo_doc}-{d.id}-{attr}",
                        tipo=tipo_doc,
                        proyecto_id=d.proyecto_id,
                        proyecto_nombre=p_nombre,
                        documento_id=d.id,
                        documento_codigo=d.codigo or "",
                        documento_titulo=d.titulo or "(sin título)",
                        seccion=seccion,
                        campo=etiqueta,
                        clave_acordeon=clave,
                        fragmento=extraer_fragmento(val, query),
                        coincidencias=val.lower().count(q_baja),
                    )
                )
    return resultados


def buscar_en_evolutivos(
    db: Session, query: str, proyectos_map: dict[str, str], limite: int
) -> list[ResultadoBusqueda]:
    patron = f"%{_escapar_like(query)}%"
    q_baja = query.lower()

    especificos_evo = [
        ("referencia_normativa", "Referencia normativa", "Cabecera", "doc/cabecera"),
        ("descripcion_requerimiento", "Descripción del requerimiento", "Requerimiento", "doc/requerimiento"),
        ("objetivo", "Objetivo", "Requerimiento", "doc/requerimiento"),
        ("alcance", "Alcance", "Requerimiento", "doc/requerimiento"),
        ("tareas_planificadas", "Tareas planificadas", "Planificación", "doc/planificacion"),
    ]

    resultados = _buscar_en_documentos(
        db, query, me.Evolutivo, "evolutivos", proyectos_map, limite, especificos_evo
    )
    if len(resultados) >= limite:
        return resultados

    # Helper para asociar datos del documento
    docs_cache: dict[int, me.Evolutivo] = {}

    def get_doc(doc_id: int) -> me.Evolutivo | None:
        if doc_id not in docs_cache:
            docs_cache[doc_id] = db.get(me.Evolutivo, doc_id)
        return docs_cache[doc_id]

    # Tablas hijas directas de evolutivos
    hijos_directos = [
        (me.GrupoRequisito, "evolutivo_id", "Requerimiento › Requisitos", "doc/requerimiento/requisitos", [("nombre", "Nombre")]),
        (me.Requisito, "evolutivo_id", "Requerimiento › Requisitos", "doc/requerimiento/requisitos", [("codigo", "Código"), ("detalle", "Detalle")]),
        (me.CriterioAceptacion, "evolutivo_id", "Análisis › Criterios", "doc/analisis/criterios", [("codigo", "Código"), ("criterio", "Criterio"), ("requisito_codigo", "Requisito")]),
        (me.Repositorio, "evolutivo_id", "Análisis › Repositorios", "doc/analisis/repositorios", [("nombre", "Repositorio"), ("subaccount", "Subaccount"), ("space", "Space")]),
        (me.Tarea, "evolutivo_id", "Análisis › Tareas", "doc/analisis/tareas/{id}", [("codigo", "Código"), ("nombre", "Nombre"), ("descripcion", "Descripción"), ("dependencias", "Dependencias"), ("diseno", "Diseño"), ("problemas", "Problemas")]),
        (me.TareaDesarrollada, "evolutivo_id", "Desarrollo › Tareas desarrolladas", "doc/desarrollo/tareas-desarrollo/{id}", [("estado", "Estado")]),
        (me.CasoPlan, "evolutivo_id", "Análisis › Plan de pruebas", "doc/analisis/casos-plan/{id}", [("codigo", "Código"), ("nombre", "Nombre"), ("criterio_codigo", "Criterio"), ("precondiciones", "Precondiciones"), ("pasos", "Pasos"), ("resultado_esperado", "Resultado esperado")]),
        (me.CasoPrueba, "evolutivo_id", "Pruebas › Casos de prueba", "doc/pruebas/casos-prueba/{id}", [("requisito_codigo", "Requisito"), ("datos", "Datos"), ("estado", "Estado"), ("responsable", "Responsable"), ("incidencias", "Incidencias")]),
        (me.DefinitionOfDone, "evolutivo_id", "Definition of Done", "doc/dod/definition-of-done", [("descripcion", "Criterio")]),
        (me.Despliegue, "evolutivo_id", "Despliegues", "doc/despliegue/registros-despliegue", [("version", "Versión"), ("entorno", "Entorno"), ("fecha_hora", "Fecha"), ("responsable", "Responsable"), ("commits", "Commits"), ("url_pipeline", "Pipeline"), ("validacion_post", "Validación"), ("resultado", "Resultado"), ("plan_reversion", "Plan de reversión")]),
        (me.BaseDatosAfectada, "evolutivo_id", "Desarrollo › Bases de datos", "doc/desarrollo/bases-datos", [("repositorio", "Repositorio"), ("nombre", "Base de datos"), ("tabla", "Tabla"), ("campos", "Campos")]),
        (me.Reunion, "evolutivo_id", "Reuniones", "doc/reuniones/reuniones/{id}", [("fecha", "Fecha"), ("participantes", "Participantes"), ("objetivo", "Objetivo"), ("decisiones", "Decisiones"), ("notas", "Notas")]),
        (me.Planificacion, "evolutivo_id", "Planificación", "doc/planificacion/planificacion", [("requisito_codigo", "Requisito"), ("criterio_codigo", "Criterio"), ("tarea_codigo", "Tarea"), ("responsable", "Responsable"), ("bloqueos", "Bloqueos")]),
        (me.Trazabilidad, "evolutivo_id", "Planificación › Trazabilidad", "doc/planificacion/trazabilidad", [("requisito_codigo", "Requisito"), ("criterio_codigo", "Criterio"), ("tarea_codigo", "Tarea"), ("prueba_codigo", "Prueba"), ("cambios", "Cambios"), ("estado_cobertura", "Cobertura")]),
        (me.Seguimiento, "evolutivo_id", "Seguimiento", "doc/seguimiento/seguimientos/{id}", [("fecha", "Fecha"), ("notas", "Notas")]),
    ]

    for model_cls, fk_attr, sec_nom, clave_tpl, campos in hijos_directos:
        if len(resultados) >= limite:
            break
        conds = [getattr(model_cls, c[0]).ilike(patron, escape="\\") for c in campos if hasattr(model_cls, c[0])]
        items = db.query(model_cls).filter(or_(*conds)).limit(limite - len(resultados)).all()
        for item in items:
            doc_id = getattr(item, fk_attr)
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = clave_tpl.format(id=getattr(item, "id", ""))
            for attr, etiqueta in campos:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"evo-{model_cls.__tablename__}-{item.id}-{attr}",
                            tipo="evolutivos",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion=sec_nom,
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Tablas nietas (con join a Tarea)
    nietos_tarea = [
        (me.RecursoTarea, "Análisis › Tareas › Recursos", [("tipo", "Tipo"), ("nombre", "Nombre"), ("detalle", "Detalle")]),
        (me.ActividadTarea, "Análisis › Tareas › Actividades", [("descripcion", "Descripción")]),
        (me.Cambio, "Análisis › Tareas › Cambios", [("nombre", "Objeto"), ("ubicacion", "Ubicación"), ("descripcion", "Descripción"), ("repositorio", "Repositorio"), ("rama", "Rama"), ("commit", "Commit")]),
    ]
    for model_cls, sec_nom, campos in nietos_tarea:
        if len(resultados) >= limite:
            break
        conds = [getattr(model_cls, c[0]).ilike(patron, escape="\\") for c in campos if hasattr(model_cls, c[0])]
        rows = (
            db.query(model_cls, me.Tarea.evolutivo_id, me.Tarea.id)
            .join(me.Tarea, model_cls.tarea_id == me.Tarea.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, tarea_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/analisis/tareas/{tarea_id}"
            for attr, etiqueta in campos:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"evo-{model_cls.__tablename__}-{item.id}-{attr}",
                            tipo="evolutivos",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion=sec_nom,
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Tablas nietas (con join a TareaDesarrollada)
    nietos_td = [
        (me.ActividadDesarrollo, "Desarrollo › Actividades", [("descripcion", "Descripción"), ("fecha_realizacion", "Fecha")]),
        (me.CambioDesarrollo, "Desarrollo › Cambios", [("nombre", "Objeto"), ("ubicacion", "Ubicación"), ("descripcion", "Descripción"), ("repositorio", "Repositorio"), ("rama", "Rama"), ("commit", "Commit")]),
    ]
    for model_cls, sec_nom, campos in nietos_td:
        if len(resultados) >= limite:
            break
        conds = [getattr(model_cls, c[0]).ilike(patron, escape="\\") for c in campos if hasattr(model_cls, c[0])]
        rows = (
            db.query(model_cls, me.TareaDesarrollada.evolutivo_id, me.TareaDesarrollada.id)
            .join(me.TareaDesarrollada, model_cls.tarea_desarrollo_id == me.TareaDesarrollada.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, td_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/desarrollo/tareas-desarrollo/{td_id}"
            for attr, etiqueta in campos:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"evo-{model_cls.__tablename__}-{item.id}-{attr}",
                            tipo="evolutivos",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion=sec_nom,
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Ejecuciones de prueba
    if len(resultados) < limite:
        campos_ej = [("fecha", "Fecha"), ("version", "Versión"), ("entorno", "Entorno"), ("responsable", "Responsable"), ("resultado", "Resultado"), ("incidencia", "Incidencia"), ("evidencias", "Evidencias")]
        conds = [getattr(me.EjecucionPrueba, c[0]).ilike(patron, escape="\\") for c in campos_ej]
        rows = (
            db.query(me.EjecucionPrueba, me.CasoPrueba.evolutivo_id, me.CasoPrueba.id)
            .join(me.CasoPrueba, me.EjecucionPrueba.caso_id == me.CasoPrueba.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, cp_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/pruebas/casos-prueba/{cp_id}"
            for attr, etiqueta in campos_ej:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"evo-ejecuciones_prueba-{item.id}-{attr}",
                            tipo="evolutivos",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion="Pruebas › Ejecuciones",
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Acciones de reunion
    if len(resultados) < limite:
        campos_ar = [("descripcion", "Acción"), ("responsable", "Responsable"), ("fecha_objetivo", "Fecha")]
        conds = [getattr(me.AccionReunion, c[0]).ilike(patron, escape="\\") for c in campos_ar]
        rows = (
            db.query(me.AccionReunion, me.Reunion.evolutivo_id, me.Reunion.id)
            .join(me.Reunion, me.AccionReunion.reunion_id == me.Reunion.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, r_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/reuniones/reuniones/{r_id}"
            for attr, etiqueta in campos_ar:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"evo-acciones_reunion-{item.id}-{attr}",
                            tipo="evolutivos",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion="Reuniones › Acciones",
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Tareas y actividades de seguimiento
    if len(resultados) < limite:
        campos_ts = [("tarea_codigo", "Código de tarea"), ("nombre", "Nombre"), ("descripcion", "Descripción")]
        conds = [getattr(me.TareaSeguimiento, c[0]).ilike(patron, escape="\\") for c in campos_ts]
        rows = (
            db.query(me.TareaSeguimiento, me.Seguimiento.evolutivo_id, me.Seguimiento.id)
            .join(me.Seguimiento, me.TareaSeguimiento.seguimiento_id == me.Seguimiento.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, seg_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/seguimiento/seguimientos/{seg_id}"
            for attr, etiqueta in campos_ts:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"evo-tareas_seguimiento-{item.id}-{attr}",
                            tipo="evolutivos",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion="Seguimiento › Tareas",
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    if len(resultados) < limite:
        conds = [me.ActividadSeguimiento.descripcion.ilike(patron, escape="\\")]
        rows = (
            db.query(me.ActividadSeguimiento, me.Seguimiento.evolutivo_id, me.Seguimiento.id)
            .join(me.TareaSeguimiento, me.ActividadSeguimiento.tarea_seguimiento_id == me.TareaSeguimiento.id)
            .join(me.Seguimiento, me.TareaSeguimiento.seguimiento_id == me.Seguimiento.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, seg_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/seguimiento/seguimientos/{seg_id}"
            val = item.descripcion or ""
            if q_baja in val.lower():
                resultados.append(
                    ResultadoBusqueda(
                        id=f"evo-actividades_seguimiento-{item.id}-descripcion",
                        tipo="evolutivos",
                        proyecto_id=doc.proyecto_id,
                        proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                        documento_id=doc.id,
                        documento_codigo=doc.codigo or "",
                        documento_titulo=doc.titulo or "(sin título)",
                        seccion="Seguimiento › Actividades",
                        campo="Descripción",
                        clave_acordeon=clave,
                        fragmento=extraer_fragmento(val, query),
                        coincidencias=val.lower().count(q_baja),
                    )
                )

    return resultados


def buscar_en_incidencias(
    db: Session, query: str, proyectos_map: dict[str, str], limite: int
) -> list[ResultadoBusqueda]:
    patron = f"%{_escapar_like(query)}%"
    q_baja = query.lower()

    especificos_inc = [
        ("severidad", "Severidad", "Cabecera", "doc/cabecera"),
        ("version_afectada", "Versión afectada", "Cabecera", "doc/cabecera"),
        ("entorno_deteccion", "Entorno detección", "Cabecera", "doc/cabecera"),
        ("fecha_deteccion", "Fecha detección", "Cabecera", "doc/cabecera"),
        ("incidencia_jira", "Incidencia Jira", "Cabecera", "doc/cabecera"),
        ("descripcion_problema", "Descripción del problema", "Problema", "doc/problema"),
        ("impacto", "Impacto", "Problema", "doc/problema"),
        ("pasos_reproducir", "Pasos para reproducir", "Problema", "doc/problema"),
        ("comportamiento_actual", "Comportamiento actual", "Problema", "doc/problema"),
        ("comportamiento_esperado", "Comportamiento esperado", "Problema", "doc/problema"),
        ("alcance_correccion", "Alcance de corrección", "Análisis › Alcance", "doc/analisis"),
        ("evidencias_iniciales", "Evidencias iniciales", "Problema › Evidencias", "doc/problema"),
        ("causa_raiz", "Causa raíz", "Análisis › Causa raíz", "doc/analisis"),
        ("verificacion_no_regresion", "Verificación de no regresión", "Pruebas › No regresión", "doc/pruebas"),
    ]

    resultados = _buscar_en_documentos(
        db, query, mi.Incidencia, "incidencias", proyectos_map, limite, especificos_inc
    )
    if len(resultados) >= limite:
        return resultados

    docs_cache: dict[int, mi.Incidencia] = {}

    def get_doc(doc_id: int) -> mi.Incidencia | None:
        if doc_id not in docs_cache:
            docs_cache[doc_id] = db.get(mi.Incidencia, doc_id)
        return docs_cache[doc_id]

    hijos_directos = [
        (mi.CriterioAceptacion, "incidencia_id", "Análisis › Criterios", "doc/analisis/criterios", [("codigo", "Código"), ("criterio", "Criterio")]),
        (mi.Repositorio, "incidencia_id", "Análisis › Repositorios", "doc/analisis/repositorios", [("nombre", "Repositorio"), ("subaccount", "Subaccount"), ("space", "Space")]),
        (mi.Tarea, "incidencia_id", "Análisis › Tareas", "doc/analisis/tareas/{id}", [("criterio_codigo", "Criterio"), ("codigo", "Código"), ("nombre", "Nombre"), ("descripcion", "Descripción"), ("dependencias", "Dependencias"), ("diseno", "Diseño"), ("problemas", "Problemas")]),
        (mi.TareaDesarrollada, "incidencia_id", "Desarrollo › Tareas desarrolladas", "doc/desarrollo/tareas-desarrollo/{id}", [("estado", "Estado")]),
        (mi.CasoPlan, "incidencia_id", "Análisis › Plan de pruebas", "doc/analisis/casos-plan/{id}", [("codigo", "Código"), ("nombre", "Nombre"), ("criterio_codigo", "Criterio"), ("precondiciones", "Precondiciones"), ("pasos", "Pasos"), ("resultado_esperado", "Resultado esperado")]),
        (mi.CasoPrueba, "incidencia_id", "Pruebas › Casos de prueba", "doc/pruebas/casos-prueba/{id}", [("datos_usados", "Datos usados"), ("pasos_dados", "Pasos dados"), ("datos", "Datos"), ("estado", "Estado"), ("responsable", "Responsable"), ("incidencias", "Incidencias")]),
        (mi.DefinitionOfDone, "incidencia_id", "Definition of Done", "doc/dod/definition-of-done", [("descripcion", "Criterio")]),
        (mi.Despliegue, "incidencia_id", "Despliegues", "doc/despliegue/registros-despliegue", [("version", "Versión"), ("entorno", "Entorno"), ("fecha_hora", "Fecha"), ("responsable", "Responsable"), ("commits", "Commits"), ("url_pipeline", "Pipeline"), ("validacion_post", "Validación"), ("resultado", "Resultado"), ("plan_reversion", "Plan de reversión")]),
        (mi.BaseDatosAfectada, "incidencia_id", "Desarrollo › Bases de datos", "doc/desarrollo/bases-datos", [("repositorio", "Repositorio"), ("nombre", "Base de datos"), ("tabla", "Tabla"), ("campos", "Campos")]),
        (mi.Reunion, "incidencia_id", "Reuniones", "doc/reuniones/reuniones/{id}", [("fecha", "Fecha"), ("participantes", "Participantes"), ("objetivo", "Objetivo"), ("decisiones", "Decisiones"), ("notas", "Notas")]),
        (mi.Planificacion, "incidencia_id", "Planificación", "doc/planificacion/planificacion", [("criterio_codigo", "Criterio"), ("tarea_codigo", "Tarea"), ("responsable", "Responsable"), ("bloqueos", "Bloqueos")]),
        (mi.Trazabilidad, "incidencia_id", "Planificación › Trazabilidad", "doc/planificacion/trazabilidad", [("criterio_codigo", "Criterio"), ("tarea_codigo", "Tarea"), ("prueba_codigo", "Prueba"), ("cambios", "Cambios"), ("estado_cobertura", "Cobertura")]),
        (mi.Seguimiento, "incidencia_id", "Seguimiento", "doc/seguimiento/seguimientos/{id}", [("fecha", "Fecha"), ("notas", "Notas")]),
    ]

    for model_cls, fk_attr, sec_nom, clave_tpl, campos in hijos_directos:
        if len(resultados) >= limite:
            break
        conds = [getattr(model_cls, c[0]).ilike(patron, escape="\\") for c in campos if hasattr(model_cls, c[0])]
        items = db.query(model_cls).filter(or_(*conds)).limit(limite - len(resultados)).all()
        for item in items:
            doc_id = getattr(item, fk_attr)
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = clave_tpl.format(id=getattr(item, "id", ""))
            for attr, etiqueta in campos:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"inc-{model_cls.__tablename__}-{item.id}-{attr}",
                            tipo="incidencias",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion=sec_nom,
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Nietos tarea
    nietos_tarea = [
        (mi.RecursoTarea, "Análisis › Tareas › Recursos", [("tipo", "Tipo"), ("nombre", "Nombre"), ("detalle", "Detalle")]),
        (mi.ActividadTarea, "Análisis › Tareas › Actividades", [("descripcion", "Descripción")]),
        (mi.Cambio, "Análisis › Tareas › Cambios", [("nombre", "Objeto"), ("ubicacion", "Ubicación"), ("descripcion", "Descripción"), ("repositorio", "Repositorio"), ("rama", "Rama"), ("commit", "Commit")]),
    ]
    for model_cls, sec_nom, campos in nietos_tarea:
        if len(resultados) >= limite:
            break
        conds = [getattr(model_cls, c[0]).ilike(patron, escape="\\") for c in campos if hasattr(model_cls, c[0])]
        rows = (
            db.query(model_cls, mi.Tarea.incidencia_id, mi.Tarea.id)
            .join(mi.Tarea, model_cls.tarea_id == mi.Tarea.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, tarea_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/analisis/tareas/{tarea_id}"
            for attr, etiqueta in campos:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"inc-{model_cls.__tablename__}-{item.id}-{attr}",
                            tipo="incidencias",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion=sec_nom,
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Nietos tarea desarrollada
    nietos_td = [
        (mi.ActividadDesarrollo, "Desarrollo › Actividades", [("descripcion", "Descripción"), ("fecha_realizacion", "Fecha")]),
        (mi.CambioDesarrollo, "Desarrollo › Cambios", [("nombre", "Objeto"), ("ubicacion", "Ubicación"), ("descripcion", "Descripción"), ("repositorio", "Repositorio"), ("rama", "Rama"), ("commit", "Commit")]),
    ]
    for model_cls, sec_nom, campos in nietos_td:
        if len(resultados) >= limite:
            break
        conds = [getattr(model_cls, c[0]).ilike(patron, escape="\\") for c in campos if hasattr(model_cls, c[0])]
        rows = (
            db.query(model_cls, mi.TareaDesarrollada.incidencia_id, mi.TareaDesarrollada.id)
            .join(mi.TareaDesarrollada, model_cls.tarea_desarrollo_id == mi.TareaDesarrollada.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, td_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/desarrollo/tareas-desarrollo/{td_id}"
            for attr, etiqueta in campos:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"inc-{model_cls.__tablename__}-{item.id}-{attr}",
                            tipo="incidencias",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion=sec_nom,
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Ejecuciones de prueba
    if len(resultados) < limite:
        campos_ej = [("fecha", "Fecha"), ("version", "Versión"), ("entorno", "Entorno"), ("responsable", "Responsable"), ("resultado", "Resultado"), ("incidencia", "Incidencia"), ("evidencias", "Evidencias")]
        conds = [getattr(mi.EjecucionPrueba, c[0]).ilike(patron, escape="\\") for c in campos_ej]
        rows = (
            db.query(mi.EjecucionPrueba, mi.CasoPrueba.incidencia_id, mi.CasoPrueba.id)
            .join(mi.CasoPrueba, mi.EjecucionPrueba.caso_id == mi.CasoPrueba.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, cp_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/pruebas/casos-prueba/{cp_id}"
            for attr, etiqueta in campos_ej:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"inc-ejecuciones_prueba-{item.id}-{attr}",
                            tipo="incidencias",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion="Pruebas › Ejecuciones",
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Acciones de reunion
    if len(resultados) < limite:
        campos_ar = [("descripcion", "Acción"), ("responsable", "Responsable"), ("fecha_objetivo", "Fecha")]
        conds = [getattr(mi.AccionReunion, c[0]).ilike(patron, escape="\\") for c in campos_ar]
        rows = (
            db.query(mi.AccionReunion, mi.Reunion.incidencia_id, mi.Reunion.id)
            .join(mi.Reunion, mi.AccionReunion.reunion_id == mi.Reunion.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, r_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/reuniones/reuniones/{r_id}"
            for attr, etiqueta in campos_ar:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"inc-acciones_reunion-{item.id}-{attr}",
                            tipo="incidencias",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion="Reuniones › Acciones",
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    # Tareas y actividades de seguimiento
    if len(resultados) < limite:
        campos_ts = [("tarea_codigo", "Código de tarea"), ("nombre", "Nombre"), ("descripcion", "Descripción")]
        conds = [getattr(mi.TareaSeguimiento, c[0]).ilike(patron, escape="\\") for c in campos_ts]
        rows = (
            db.query(mi.TareaSeguimiento, mi.Seguimiento.incidencia_id, mi.Seguimiento.id)
            .join(mi.Seguimiento, mi.TareaSeguimiento.seguimiento_id == mi.Seguimiento.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, seg_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/seguimiento/seguimientos/{seg_id}"
            for attr, etiqueta in campos_ts:
                val = getattr(item, attr) or ""
                if q_baja in val.lower():
                    resultados.append(
                        ResultadoBusqueda(
                            id=f"inc-tareas_seguimiento-{item.id}-{attr}",
                            tipo="incidencias",
                            proyecto_id=doc.proyecto_id,
                            proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                            documento_id=doc.id,
                            documento_codigo=doc.codigo or "",
                            documento_titulo=doc.titulo or "(sin título)",
                            seccion="Seguimiento › Tareas",
                            campo=etiqueta,
                            clave_acordeon=clave,
                            fragmento=extraer_fragmento(val, query),
                            coincidencias=val.lower().count(q_baja),
                        )
                    )

    if len(resultados) < limite:
        conds = [mi.ActividadSeguimiento.descripcion.ilike(patron, escape="\\")]
        rows = (
            db.query(mi.ActividadSeguimiento, mi.Seguimiento.incidencia_id, mi.Seguimiento.id)
            .join(mi.TareaSeguimiento, mi.ActividadSeguimiento.tarea_seguimiento_id == mi.TareaSeguimiento.id)
            .join(mi.Seguimiento, mi.TareaSeguimiento.seguimiento_id == mi.Seguimiento.id)
            .filter(or_(*conds))
            .limit(limite - len(resultados))
            .all()
        )
        for item, doc_id, seg_id in rows:
            doc = get_doc(doc_id)
            if not doc:
                continue
            clave = f"doc/seguimiento/seguimientos/{seg_id}"
            val = item.descripcion or ""
            if q_baja in val.lower():
                resultados.append(
                    ResultadoBusqueda(
                        id=f"inc-actividades_seguimiento-{item.id}-descripcion",
                        tipo="incidencias",
                        proyecto_id=doc.proyecto_id,
                        proyecto_nombre=proyectos_map.get(doc.proyecto_id, ""),
                        documento_id=doc.id,
                        documento_codigo=doc.codigo or "",
                        documento_titulo=doc.titulo or "(sin título)",
                        seccion="Seguimiento › Actividades",
                        campo="Descripción",
                        clave_acordeon=clave,
                        fragmento=extraer_fragmento(val, query),
                        coincidencias=val.lower().count(q_baja),
                    )
                )

    return resultados


@router.get("/buscar", response_model=list[ResultadoBusqueda])
def buscar(
    q: str = Query(..., min_length=1, description="Texto a buscar en cualquier campo"),
    tipo: str = Query("todos", description="Filtro opcional: todos, proyectos, evolutivos, incidencias"),
    limite: int = Query(150, ge=1, le=500, description="Número máximo de coincidencias"),
    db_e: Session = Depends(get_evolutivos_db),
    db_i: Session = Depends(get_incidencias_db),
) -> list[ResultadoBusqueda]:
    termino = q.strip()
    if not termino:
        return []

    # Mapa de proyectos para enriquecer los resultados
    proyectos_e = db_e.query(me.Proyecto).all()
    proyectos_map = {p.id: p.nombre for p in proyectos_e}

    resultados: list[ResultadoBusqueda] = []

    tipo_norm = tipo.lower().strip()

    # 1. Proyectos
    if tipo_norm in ("todos", "proyectos"):
        res_proy = buscar_en_proyectos(db_e, termino, limite)
        resultados.extend(res_proy)

    # 2. Evolutivos
    if tipo_norm in ("todos", "evolutivos") and len(resultados) < limite:
        res_evo = buscar_en_evolutivos(db_e, termino, proyectos_map, limite - len(resultados))
        resultados.extend(res_evo)

    # 3. Incidencias
    if tipo_norm in ("todos", "incidencias") and len(resultados) < limite:
        res_inc = buscar_en_incidencias(db_i, termino, proyectos_map, limite - len(resultados))
        resultados.extend(res_inc)

    return resultados
