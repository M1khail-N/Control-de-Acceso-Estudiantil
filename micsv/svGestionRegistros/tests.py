from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from micsv.svGestionRegistros.models import Profesor, Asignatura, Maquina, Alumno

# TEST PROFESOR
class ProfesorViewSetTests(APITestCase):

    def setUp(self):
        self.profesor = Profesor.objects.create(
            nombre="Juan",
            apellido="Lopez"
        )
        self.url_list = reverse("profesor-list")
        self.url_detail = reverse("profesor-detail", args=[self.profesor.id_profesor])

    def test_crearProfesor(self):
        data = {
            "nombre": "Ana",
            "apellido": "Torres"
        }
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profesor.objects.count(), 2)

    def test_listarProfesores(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtenerProfesor(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# TEST ASIGNATURA
class AsignaturaViewSetTests(APITestCase):

    def setUp(self):
        self.profesor = Profesor.objects.create(
            nombre="Luis",
            apellido="Ramirez"
        )
        self.asignatura = Asignatura.objects.create(
            nombre="Matemática",
            profesor=self.profesor
        )

        self.url_list = reverse("asignatura-list")
        self.url_detail = reverse("asignatura-detail", args=[self.asignatura.id_asignatura])
        self.url_profesor = reverse("asignatura-profesor", args=[self.asignatura.id_asignatura])

    def test_crearAsignatura(self):
        data = {
            "nombre": "Algoritmos",
            "profesor": self.profesor.id_profesor
        }
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Asignatura.objects.count(), 2)

    def test_obtenerAsignatura(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtenerProfesorAsignatura(self):
        response = self.client.get(self.url_profesor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nombre"], "Luis")

# TEST MAQUINA
class MaquinaViewSetTests(APITestCase):

    def setUp(self):
        self.maquina = Maquina.objects.create(nombre="PC-01")
        self.url_list = reverse("maquina-list")
        self.url_detail = reverse("maquina-detail", args=[self.maquina.id_maquina])

    def test_crearMaquina(self):
        data = {"nombre": "PC-02"}
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Maquina.objects.count(), 2)

    def test_listarMaquinas(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_obtenerMaquina(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# TEST ALUMNO
class AlumnoViewSetTests(APITestCase):

    def setUp(self):
        self.alumno = Alumno.objects.create(
            codigo_alumno=9999999,
            nombre="Carlos",
            apellido="Diaz",
            carrera="Ingeniería",
            ciclo=3,
            fecha_nacimiento="2000-01-01"
        )

        self.url_list = reverse("alumno-list")
        self.url_detail = reverse("alumno-detail", args=[self.alumno.id_alumno])

    def test_crearAlumno(self):
        data = {
            "codigo_alumno": 7777777,
            "nombre": "Juan",
            "apellido": "Perez",
            "carrera": "Sistemas",
            "ciclo": 5,
            "fecha_nacimiento": "2001-05-05"
        }
        
        response = self.client.post(self.url_list, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Alumno.objects.count(), 2)

    def test_listarAlumnos(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtenerAlumno(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
