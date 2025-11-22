pipeline {
    agent any

    environment {
        PROJECT_NAME   = "cael"
        DOCKER_IMAGE   = "cael-app"
        SONARQUBE_ENV  = "SonarQubeServer"
        HOST_URL       = "http://host.docker.internal:8000"
    }

    stages {
        // CHECKOUT
        stage('Checkout') {
            steps {
                echo "Clonando repo..."
                git(
                    url: 'https://github.com/M1khail-N/Control-de-Acceso-Estudiantil.git',
                    branch: 'feature'
                )
            }
        }

        // BUILD DOCKER IMAGE
        stage('Levantar imagen en Docker') {
            steps {
                powershell """
                echo "Levantando imagen ${env.DOCKER_IMAGE}..."
                docker build -t ${env.DOCKER_IMAGE}:latest .
                """
            }
        }

        // EJECUTAR ENTORNO DE PRUEBAS
        stage('Levantar contenedor de testeo') {
            steps {
                powershell """
                echo "Levantando servicios web y BD..."
                docker-compose down 2>\$null
                docker-compose up -d
                echo "Esperando 20 segundos para que inicie la BD y el servidor..."
                Start-Sleep -Seconds 20
                """
            }
        }

        // UNIT TESTS
        stage('Pruebas unitarias') {
            steps {
                powershell """
                echo "Ejecutando pruebas unitarias de los microservicios..."
                docker exec -t cael_django `
                    python manage.py test micsv --settings=core.settings_test
                """
            }
        }

        // INTEGRATION TESTS
        stage('Pruebas de integración') {
            steps {
                powershell """
                echo "Ejecutando prueba de integración..."
                docker exec -t cael_django `
                    python manage.py test --settings=core.settings_test
                """
            }
        }

        /* 
        stage('Levantar Selenium Grid') {
            steps {
                powershell """
                docker-compose -f docker-compose.selenium.yml up -d
                Start-Sleep -Seconds 8
                """
            }
        }

        stage('Pruebas funcionales (Selenium)') {
            steps {
                powershell """
                docker exec ${env.PROJECT_NAME}-test `
                    pytest tests_selenium -q
                """
            }
        }

        */

        // SONARQUBE ANALYSIS
        stage('Analisis con SonarQube') {
            steps {
                withSonarQubeEnv("${env.SONARQUBE_ENV}") {
                    powershell """
                    echo "Ejecutando SonarScanner..."
                    sonar-scanner
                """
                }
            }
        }

        stage("Quality Gate") {
            steps {
                echo "Esperando resultado de SonarQube..."
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // JMETER
        stage('Prueba de rendimiento con JMeter') {
            steps {
                powershell """
                echo "Ejecutando pruebas de rendimiento con JMeter..."
                docker run --rm `
                    -v "${WORKSPACE}:/jmeter" `
                    justb4/jmeter `
                    -n -t /jmeter/test-plan.jmx `
                    -l /jmeter/results.jtl
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'jmeter/results.jtl', allowEmptyArchive: true
                }
            }
        }

        // OWASP ZAP
        stage('Escaneo con OWASP ZAP') {
            steps {
                powershell """
                docker run --rm `
                    --network=${env.PROJECT_NAME}_default `
                    -v "${WORKSPACE}/zap-reports:/zap/reports" `
                    owasp/zap2docker-stable zap-baseline.py `
                        -t http://cael_django:8000 `
                        -r zap_report.htm
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'zap-reports/**', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            powershell """
            echo "Limpiando el entorno Docker..."
            docker-compose down 2>\$null
            """
        }
    }
}
