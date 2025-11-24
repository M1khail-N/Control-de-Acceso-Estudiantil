# CAEL: Control de Acceso Estudiantil para el Laboratorio

Este repositorio contiene el código fuente del proyecto CAEL, una aplicación web simple para gestionar los accesos de estudiantes al laboratorio de computación.
La arquitectura de este sistema es el siguiente: 
- Frontend: HTML, CSS y JS
- Backend: Framework Django (Python)
- Base de datos: MySQL
- Contenerizado de App y BD en Docker

Esta aplicación esta pensada para integrarse en un entorno de desarrollo siguiendo el marco de trabajo DevSecOps, contando con un archivo Jenkinsfile configurado para realizar el despliegue tras la ejecución automatizada de pruebas y análisis de seguridad DAST y SAST con SonarQube y OWASP ZAP.

## 1. Estructura del Proyecto
A continuación, se tiene esta estructura en el directorio:

    CAEL                            # Esta es la carpeta raiz del proyecto
    ├── core/                       # Directorio principal de configuración de Django (Contiene settings.py, entre otros)
    ├── frontend/                   # Directorio del frontend básico (HTML, CSS y JS)
    │   ├── static/
    │   ├── templates/
    │   └── base.html
    ├── micsv/                      # Aplicaciones de Django (Microservicios)
    │   ├── svEstadisticas/         # Microservicio de estadisticas y métricas
    │   ├── svGestionRegistros/     # Microservicio de gestion de registros (Alumnos, Asignaturas, Profesores y Máquinas)
    │   ├── svRegAcceso/            # Microservicio de registro de accesos (Libres o en clase)
    ├── jmeter/
    │   └── test_plan.jmx           # Plan de pruebas de rendimiento con Apache JMeter
    ├── tests_selenium/
    │   └── ...                     # Pruebas funcionales con Selenium exportados en Python
    ├── docker-compose.selenium.yml # Ejecutor de servicio para levantamiento de entorno de prueba Selenium
    ├── docker-compose.yml          # Ejecutor de servicio para levantamiento de entorno MySQL
    ├── Dockerfile                  # Dockerfile para construir la imagen del backend
    ├── entrypoint.sh               # Script de Shell para ejecutar migración de datos entre la imagen backend e imagen MySQL
    ├── Jenkinsfile                 # Script del Pipeline de Jenkins
    ├── manage.py                   # Script de gestión del proyecto Django
    ├── requirements.txt            # Dependencias de Python para el proyecto
    ├── sonar-project.properties    # Configuración para la ejecucion del análisis con SonarQube
    └── README.md                   # El documento que esta leyendo ahora mismo

## 2. Guía de Instalación Local y Ejecución

Para ejecutar el proyecto en sí localmente, solo se debe contar con un daemon Docker, el cual puede brindarse por medio de un SO Linux con Docker instalado o por medio de Docker Desktop para Windows, de forma que este disponible WSL2.
Por otro lado, para la ejecución de pruebas, es importante considerar si estas se hacen manualmente o automáticamente por medio del propio Pipeline Jenkins, que esta configurado actualmente para realizar pruebas unitarias, de integración, SAST, DAST y de estrés.

### 2.1. Instalación Local

- Asegurarse de tener Docker instalado y el daemon ejecutándose en la computadora
- Desde el directorio raiz del proyecto, ejecutar el comando `docker-compose up --build`, y verificar con `docker ps`
- Una vez levantada la imagen de la aplicación, esta se encontrará disponible en `localhost:8000`

### 2.2. Ejecución de Pruebas

- IMPORTANTE: Para realizar estas pruebas, se debe detener el contenedor docker de la aplicación por si esta levantado. Puede usar `Ctrl + C` desde la terminal donde ejecutó `docker-compose up --build` o ejecutar `docker stop cael`, y verificar que no esté su imagen ejecutándose con `docker ps`
- Para realizar pruebas unitarias ejecute en el directorio principal: `docker exec -it cael_django python manage.py test micsv`
- Para realizar pruebas de integración ejecute en el directorio principal: `docker exec -it cael_django python manage.py test`
- Para las pruebas funcionales con Selenium ejecute en el directorio principal: `pytest tests_selenium`
- Para las pruebas de estrés, debe tener instalado Apache JMeter en su computadora, de forma que pueda abrir el archivo `test_plan.jmx` en `jmeter/`
- Para las pruebas SAST con SonarQube inicie una imagen con: `docker run -d --name sonarqube -p 9000:9000 -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true sonarqube:community` y posteriormente el propio análisis con `docker run --rm -e SONAR_HOST_URL="http://host.docker.internal:9000" -e SONAR_TOKEN="<TOKEN_SONARQUBE>" -v "${PWD}:/usr/src" sonarsource/sonar-scanner-cli` donde `<TOKEN_SONARQUBE>` debe ser reemplazado por su propio token para el análisis.
- Las pruebas de seguridad DAST con OWASP ZAP son automatizadas en el pipeline Jenkins.

Ahora, para la ejecucion del pipeline, considere:

- Tener instalado Jenkins localmente en su computadora, al igual que el plugin SonarQube.

### 3. Notas importantes

El stage Quality Gate de Jenkins no logra obtener el reporte realizado con SonarQube por razones de baja memoria. En caso de no contar con este problema, puede descomentar dicho stage en el Jenkinsfile para que pueda ejecutarse correctamente. Asimismo, el stage de pruebas con Selenium cuenta con serios problemas de compatibilidad, por lo que es omitido en el pipeline, sin embargo, puede ejecutarse manualmente sin dificultades.
