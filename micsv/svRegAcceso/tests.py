from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from micsv.svGestionRegistros.models import Alumno, Maquina, Asignatura, Profesor
from micsv.svRegAcceso.models import RegistroBase, RegistroLibre, RegistroClase

# REGISTRO BASE
class RegistroBaseViewSetTests(APITestCase):

    def setUp(self):
        self.alumno = Alumno.objects.create(
            codigo_alumno="1111111",
            nombre="Juan",
            apellido="Perez",
            carrera="Ingeniería",
            ciclo=5,
            fecha_nacimiento="2000-01-01"
        )

        self.maquina = Maquina.objects.create(
            id_maquina=1,
            nombre="PC-01"
        )

        self.url_entrada = reverse("registrobase-entrada")
        self.url_salida = reverse("registrobase-salida")

    def test_entradaExitosa(self):
        data = {
            "codigo_alumno": "1111111",
            "maquina_id": 1
        }

        response = self.client.post(self.url_entrada, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(RegistroBase.objects.count(), 1)

    def test_entradaFaltanDatos(self):
        data = {
            "codigo_alumno": "1111111"
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_entradaDatosIncorr(self):
        data = {
            "codigo_alumno": "AAAAAAA"
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_salidaExitosa(self):
        # Crear entrada previa
        RegistroBase.objects.create(
            alumno=self.alumno,
            maquina=self.maquina,
            fecha_hora_entrada="2024-01-01T10:00:00Z"
        )

        data = {
            "codigo_alumno": "1111111"
        }

        response = self.client.post(self.url_salida, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["fecha_hora_salida"])

# REGISTRO LIBRE
class RegistroLibreViewSetTests(APITestCase):

    def setUp(self):
        self.alumno = Alumno.objects.create(
            codigo_alumno="1111111",
            nombre="Juan",
            apellido="Perez",
            carrera="Ingeniería",
            ciclo=5,
            fecha_nacimiento="2000-01-01"
        )

        self.maquina = Maquina.objects.create(
            id_maquina=1,
            nombre="PC-01"
        )

        self.url_entrada = reverse("registrolibre-entrada")

    def test_registroLibreExitoso(self):
        data = {
            "codigo_alumno": "1111111",
            "maquina_id": 1,
            "motivo": "proyecto"
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RegistroLibre.objects.count(), 1)

    def test_registroLibreFaltanDatos(self):
        data = {
            "codigo_alumno": "1111111",
            "maquina_id": 1
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# REGISTRO DE CLASE
class RegistroClaseViewSetTests(APITestCase):

    def setUp(self):
        self.alumno = Alumno.objects.create(
            codigo_alumno="1111111",
            nombre="Juan",
            apellido="Perez",
            carrera="Ingeniería",
            ciclo=5,
            fecha_nacimiento="2000-01-01"
        )

        self.maquina = Maquina.objects.create(
            id_maquina=1,
            nombre="PC-01"
        )

        self.profesor = Profesor.objects.create(
            id_profesor=10,
            nombre="Profesor Lopez"
        )

        self.asignatura = Asignatura.objects.create(
            id_asignatura=5,
            nombre="Algoritmos",
            profesor=self.profesor
        )

        self.url_entrada = reverse("registroclase-entrada")

    def test_registroClaseExitoso(self):
        data = {
            "codigo_alumno": "1111111",
            "maquina_id": 1,
            "asignatura_id": 5,
            "profesor_id": 10
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RegistroClase.objects.count(), 1)

    def test_registroClaseProfNoPert(self):
        profesor2 = Profesor.objects.create(
            id_profesor=99,
            nombre="Otro Profe"
        )

        data = {
            "codigo_alumno": "1111111",
            "maquina_id": 1,
            "asignatura_id": 5,
            "profesor_id": 99
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registroClaseFaltanDatos(self):
        data = {
            "codigo_alumno": "1111111",
            "maquina_id": 1,
            "profesor_id": 10
        }

        response = self.client.post(self.url_entrada, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)