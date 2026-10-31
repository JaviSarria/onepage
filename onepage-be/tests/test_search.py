"""Pruebas unitarias para el motor de busqueda global."""

import unittest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from onepage_be.database import EvolutivosBase, IncidenciasBase
from onepage_be.models import evolutivo as me, incidencia as mi
from onepage_be.routers.search import buscar, extraer_fragmento


class TestSearchEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine_e = create_engine("sqlite:///:memory:")
        cls.engine_i = create_engine("sqlite:///:memory:")
        EvolutivosBase.metadata.create_all(cls.engine_e)
        IncidenciasBase.metadata.create_all(cls.engine_i)

        cls.SessionE = sessionmaker(bind=cls.engine_e)
        cls.SessionI = sessionmaker(bind=cls.engine_i)

    def setUp(self):
        self.db_e = self.SessionE()
        self.db_i = self.SessionI()

    def tearDown(self):
        self.db_e.close()
        self.db_i.close()

    def test_extraer_fragmento(self):
        texto = "Este es un texto largo para comprobar que la extraccion de fragmentos funciona correctamente alrededor de la palabra clave."
        frag = extraer_fragmento(texto, "extraccion", radio=20)
        self.assertIn("extraccion", frag)
        self.assertTrue(frag.startswith("..."))
        self.assertTrue(frag.endswith("..."))

    def test_busqueda_vacia(self):
        res = buscar(q="   ", tipo="todos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertEqual(res, [])

    def test_busqueda_proyectos(self):
        pid = str(uuid.uuid4())
        p = me.Proyecto(id=pid, nombre="Proyecto Apolo", descripcion="Gestion espacial confidencial")
        self.db_e.add(p)
        self.db_e.commit()

        # Buscar por nombre
        res = buscar(q="Apolo", tipo="proyectos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertTrue(any(r.proyecto_id == pid and r.campo == "Nombre" for r in res))

        # Buscar por descripcion
        res_desc = buscar(q="confidencial", tipo="todos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertTrue(any(r.proyecto_id == pid and r.campo == "Descripción" for r in res_desc))

    def test_busqueda_evolutivos_y_tareas(self):
        pid = str(uuid.uuid4())
        p = me.Proyecto(id=pid, nombre="Proyecto Orion", descripcion="")
        self.db_e.add(p)
        self.db_e.flush()

        evo = me.Evolutivo(
            proyecto_id=pid,
            codigo="EVO-99",
            titulo="Integracion con microservicio de pagos",
            resumen="Pasarela Stripe y PayPal",
        )
        self.db_e.add(evo)
        self.db_e.flush()

        tarea = me.Tarea(
            evolutivo_id=evo.id,
            codigo="TAR-01",
            nombre="Configurar webhook de Stripe",
            descripcion="Validar firma criptografica del webhook",
        )
        self.db_e.add(tarea)
        self.db_e.flush()

        recurso = me.RecursoTarea(
            tarea_id=tarea.id,
            tipo="servicio",
            nombre="API Stripe",
            detalle="Token secreto para endpoints seguros",
        )
        self.db_e.add(recurso)
        self.db_e.commit()

        # Buscar en cabecera / resumen
        res_evo = buscar(q="Stripe", tipo="evolutivos", limite=20, db_e=self.db_e, db_i=self.db_i)
        self.assertTrue(len(res_evo) >= 2)
        # Verificar que una coincidencia apunte al acordeon de la tarea
        tarea_matches = [r for r in res_evo if r.clave_acordeon == f"doc/analisis/tareas/{tarea.id}"]
        self.assertTrue(len(tarea_matches) >= 1)

    def test_busqueda_incidencias(self):
        pid = str(uuid.uuid4())
        p = mi.Proyecto(id=pid, nombre="Proyecto Vulcano", descripcion="")
        self.db_i.add(p)
        self.db_i.flush()

        inc = mi.Incidencia(
            proyecto_id=pid,
            codigo="INC-42",
            titulo="Fallo critico en login",
            descripcion_problema="Timeout intermitente al contactar con LDAP",
            causa_raiz="Pool de conexiones agotado",
        )
        self.db_i.add(inc)
        self.db_i.commit()

        res_inc = buscar(q="LDAP", tipo="incidencias", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertEqual(len(res_inc), 1)
        self.assertEqual(res_inc[0].documento_codigo, "INC-42")
        self.assertEqual(res_inc[0].seccion, "Problema")
        self.assertEqual(res_inc[0].clave_acordeon, "doc/problema")

    def test_busqueda_reuniones_y_seguimientos(self):
        pid = str(uuid.uuid4())
        p = me.Proyecto(id=pid, nombre="Proyecto Jupiter", descripcion="")
        self.db_e.add(p)
        self.db_e.flush()

        evo = me.Evolutivo(
            proyecto_id=pid,
            codigo="EVO-55",
            titulo="Evolutivo con actas y diario",
        )
        self.db_e.add(evo)
        self.db_e.flush()

        reu = me.Reunion(
            evolutivo_id=evo.id,
            objetivo="Revision de arquitectura de microservicios",
            decisiones="Adoptar Kafka para eventos",
        )
        self.db_e.add(reu)
        self.db_e.flush()

        accion = me.AccionReunion(
            reunion_id=reu.id,
            descripcion="Desplegar cluster de Kafka en Kubernetes",
            responsable="Arquitecto Cloud",
        )
        self.db_e.add(accion)

        seg = me.Seguimiento(
            evolutivo_id=evo.id,
            notas="Jornada dedicada a dockerizar la aplicacion",
        )
        self.db_e.add(seg)
        self.db_e.flush()

        ts = me.TareaSeguimiento(
            seguimiento_id=seg.id,
            nombre="Optimizar imagen Docker con multi-stage build",
        )
        self.db_e.add(ts)
        self.db_e.commit()

        # Buscar por Kafka
        res_kafka = buscar(q="Kafka", tipo="evolutivos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertEqual(len(res_kafka), 2)
        self.assertTrue(any("Reuniones" in r.seccion for r in res_kafka))

        # Buscar por multi-stage
        res_docker = buscar(q="multi-stage", tipo="evolutivos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertEqual(len(res_docker), 1)
        self.assertEqual(res_docker[0].seccion, "Seguimiento › Tareas")
        self.assertEqual(res_docker[0].clave_acordeon, f"doc/seguimiento/seguimientos/{seg.id}")

    def test_caracteres_especiales(self):
        # Asegurar que caracteres comodin como % y _ no rompen ni causan errores de sintaxis
        res = buscar(q="100%", tipo="todos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertIsInstance(res, list)
        res2 = buscar(q="test_user", tipo="todos", limite=10, db_e=self.db_e, db_i=self.db_i)
        self.assertIsInstance(res2, list)


if __name__ == "__main__":
    unittest.main()
