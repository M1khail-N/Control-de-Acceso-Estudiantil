pipeline {
    agent any

    environment {
        PROJECT_NAME   = "cael"
        DOCKER_IMAGE   = "cael-app"
        DOCKER_TAG     = "latest"
        SONARQUBE_ENV  = "SonarQubeServer"
        SONAR_TOKEN = credentials('sonarqube-token')
    }

    stages {

        /* =====================
           CHECKOUT
        ====================== */
        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/M1khail-N/Control-de-Acceso-Estudiantil.git',
                    branch: 'feature'
                )
            }
        }

        /* =====================
           BUILD DOCKER IMAGE
        ====================== */
        stage('Levantar imagen en Docker') {
            steps {
                powershell """
                docker build -t ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} .
                """
            }
        }

        /* =====================
           RUN TEST CONTAINER
        ====================== */
        stage('Ejecutar contenedor para testeo') {
            steps {
                powershell """
                docker network create cael-net 2>\$null

                docker run -d --name ${env.PROJECT_NAME}-test `
                    --network=cael-net `
                    -p 8000:8000 `
                    ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}

                Start-Sleep -Seconds 12
                """
            }
        }

        /* =====================
           UNIT TESTS
        ====================== */
        stage('Pruebas unitarias') {
            steps {
                powershell """
                docker exec ${env.PROJECT_NAME}-test `
                    python manage.py test micsv --settings=core.settings_test
                """
            }
        }

        /* =====================
           INTEGRATION TESTS
        ====================== */
        stage('Pruebas de integración') {
            steps {
                powershell """
                docker exec ${env.PROJECT_NAME}-test `
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

        /* =====================
           SONARQUBE ANALYSIS
        ====================== */
        stage('Analisis con SonarQube') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    powershell """
                    sonar-scanner \
                        -Dsonar.projectKey=django-project \
                        -Dsonar.sources=core,micsv,frontend \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_TOKEN}
                    """
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 3, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        /* =====================
           JMETER
        ====================== */
        stage('Prueba de rendimiento con JMeter') {
            steps {
                powershell """
                docker run --rm `
                    -v "${WORKSPACE}:/jmeter" `
                    justb4/jmeter `
                    -n -t /jmeter/test-plan.jmx `
                    -l /jmeter/results.jtl
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'results.jtl', allowEmptyArchive: true
                }
            }
        }

        /* =====================
           OWASP ZAP
        ====================== */
        stage('Escaneo con OWASP ZAP') {
            steps {
                powershell """
                docker run --rm `
                    --network="cael-net" `
                    -v "${WORKSPACE}/zap-reports:/zap/reports" `
                    owasp/zap2docker-stable zap-baseline.py `
                        -t http://cael-test:8000 `
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
            docker rm -f ${env.PROJECT_NAME}-test 2>\$null
            docker-compose -f docker-compose.selenium.yml down 2>\$null
            """
        }
    }
}
