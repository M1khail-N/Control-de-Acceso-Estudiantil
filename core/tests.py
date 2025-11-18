from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from micsv.svGestionRegistros.models import Profesor, Asignatura, Alumno, Maquina
from micsv.svRegAcceso.models import RegistroBase, RegistroLibre, RegistroClase


class IntegracionSistemaCompletoTests(APITestCase):
    """
    Pruebas de INTEGRACIÓN entre:
    - svGestionRegistros
    - svRegAcceso

    Valida un flujo real de uso del sistema.
    """

    def setUp(self):
        # Crear profesor
        self.profesor = Profesor.objects.create(
            nombre="Luis",
            apellido="Ramirez"
        )

        # Crear asignatura
        self.asignatura = Asignatura.objects.create(
            nombre="Algoritmos",
            profesor=self.profesor
        )

        # Crear maquina
        self.maquina = Maquina.objects.create(nombre="PC-01")

        # Crear alumno
        self.alumno = Alumno.objects.create(
            codigo_alumno="1234567",
            nombre="Ana",
            apellido="Torres",
            carrera="Sistemas",
            ciclo=4,
            fecha_nacimiento="2002-05-05"
        )

        # URLs globales necesarias
        self.url_entrada_base = reverse("registrobase-entrada")
        self.url_salida_base = reverse("registrobase-salida")
        self.url_entrada_libre = reverse("registrolibre-entrada")
        self.url_entrada_clase = reverse("registroclase-entrada")

    # ===========================================================
    # 1. REGISTRO BASE - ENTRADA Y SALIDA
    # ===========================================================
    def test_flujo_registro_base(self):
        """
        Flujo completo: entrada -> salida
        """

        # --- Entrada ---
        data_entrada = {
            "codigo_alumno": "1234567",
            "maquina_id": self.maquina.id_maquina
        }

        r1 = self.client.post(self.url_entrada_base, data_entrada)
        self.assertEqual(r1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RegistroBase.objects.count(), 1)

        # --- Salida ---
        data_salida = {
            "codigo_alumno": "1234567"
        }

        r2 = self.client.post(self.url_salida_base, data_salida)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(r2.data["fecha_hora_salida"])

    # ===========================================================
    # 2. REGISTRO LIBRE
    # ===========================================================
    def test_flujo_registro_libre(self):
        """
        Verifica que un alumno puede registrar un uso libre sin conflictos.
        """

        data = {
            "codigo_alumno": "1234567",
            "maquina_id": self.maquina.id_maquina,
            "motivo": "investigacion"
        }

        r = self.client.post(self.url_entrada_libre, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RegistroLibre.objects.count(), 1)

        # Validar relación correcta con RegistroBase
        base = RegistroBase.objects.first()
        libre = RegistroLibre.objects.get(reg_base=base)
        self.assertEqual(libre.motivo, "investigacion")
        
    # ===========================================================
    # 3. REGISTRO DE CLASE
    # ===========================================================
    def test_flujo_registro_clase(self):
        """
        Verifica que un alumno puede registrar un uso por clase,
        respetando asignatura-profesor.
        """

        data = {
            "codigo_alumno": "1234567",
            "maquina_id": self.maquina.id_maquina,
            "asignatura_id": self.asignatura.id_asignatura,
            "profesor_id": self.profesor.id_profesor
        }

        r = self.client.post(self.url_entrada_clase, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        # Validar creación correcta
        self.assertEqual(RegistroClase.objects.count(), 1)
        reg = RegistroClase.objects.first()

        self.assertEqual(reg.asignatura.id_asignatura, self.asignatura.id_asignatura)
        self.assertEqual(reg.profesor.id_profesor, self.profesor.id_profesor)

    # ===========================================================
    # 4. VALIDACIÓN DE COHERENCIA GLOBAL DEL SISTEMA
    # ===========================================================
    def test_integridad_global(self):
        """
        Prueba que varias operaciones encadenadas mantienen la
        integridad general del sistema.
        """

        # 1. Registrar libre
        self.client.post(self.url_entrada_libre, {
            "codigo_alumno": "1234567",
            "maquina_id": self.maquina.id_maquina,
            "motivo": "proyecto"
        })

        # ❗ Cerrar esa sesión para permitir otro acceso
        self.client.post(self.url_salida_base, {
            "codigo_alumno": "1234567"
        })

        # 2. Registrar clase
        self.client.post(self.url_entrada_clase, {
            "codigo_alumno": "1234567",
            "maquina_id": self.maquina.id_maquina,
            "asignatura_id": self.asignatura.id_asignatura,
            "profesor_id": self.profesor.id_profesor
        })

        # Cerrar también este registro
        self.client.post(self.url_salida_base, {
            "codigo_alumno": "1234567"
        })

        # 3. Entrada base y salida
        self.client.post(self.url_entrada_base, {
            "codigo_alumno": "1234567",
            "maquina_id": self.maquina.id_maquina
        })
        self.client.post(self.url_salida_base, {
            "codigo_alumno": "1234567"
        })

        # --- Validaciones globales ---
        self.assertEqual(Alumno.objects.count(), 1)
        self.assertEqual(Maquina.objects.count(), 1)
        self.assertEqual(Profesor.objects.count(), 1)
        self.assertEqual(Asignatura.objects.count(), 1)

        # Registros generados durante el flujo
        self.assertEqual(RegistroLibre.objects.count(), 1)
        self.assertEqual(RegistroClase.objects.count(), 1)
        self.assertEqual(RegistroBase.objects.count(), 3)