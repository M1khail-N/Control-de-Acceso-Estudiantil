pipeline {
    agent any

    environment {
        PROJECT_NAME   = "cael"
        DOCKER_IMAGE   = "cael-app"
        DOCKER_TAG     = "latest"
        SONARQUBE_ENV  = "SonarQubeServer"
    }

    stages {

        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/M1khail-N/Control-de-Acceso-Estudiantil.git',
                    branch: 'feature',
                    credentialsId: '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'
                )
            }
        }

        stage('Levantar imagen en Docker') {
            steps {
                sh '''
                docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                '''
            }
        }

        stage('Ejecutar contenedor para testeo') {
            steps {
                sh '''
                docker network create cael-net || true

                docker run -d --name ${PROJECT_NAME}-test \
                    --network=cael-net \
                    -p 8000:8000 \
                    ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
                sleep 12
            }
        }

        stage('Pruebas unitarias') {
            steps {
                sh '''
                docker exec ${PROJECT_NAME}-test bash -c \
                    "python manage.py test micsv"
                '''
            }
        }

        stage('Pruebas de integración') {
            steps {
                sh '''
                docker exec ${PROJECT_NAME}-test bash -c \
                    "python manage.py test"
                '''
            }
        }

        stage('Levantar Selenium Grid') {
            steps {
                sh '''
                docker-compose -f docker-compose.selenium.yml up -d
                '''
                sleep 8
            }
        }


        stage('Pruebas funcionales (Selenium)') {
            steps {
                sh '''
                docker exec ${PROJECT_NAME}-test bash -c \
                    "pytest tests_selenium -q"
                '''
            }
        }

        stage('Análisis con SonarQube') {
            environment {
                SONAR_TOKEN = credentials('sonarqube-token')
            }
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                    docker run --rm \
                        -e SONAR_HOST_URL="${SONAR_HOST_URL}" \
                        -e SONAR_TOKEN="${SONAR_TOKEN}" \
                        -v "\$(pwd):/usr/src" \
                        sonarsource/sonar-scanner-cli
                    '''
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

        stage('Prueba de rendimiento con JMeter') {
            steps {
                sh '''
                docker run --rm -v "$PWD":/jmeter \
                    justb4/jmeter \
                    -n -t /jmeter/test-plan.jmx \
                    -l /jmeter/results.jtl
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'results.jtl', allowEmptyArchive: true
                }
            }
        }

        stage('Escaneo con OWASP ZAP') {
            steps {
                sh '''
                docker run --rm \
                    --network="host" \
                    -v $(pwd)/zap-reports:/zap/reports \
                    owasp/zap2docker-stable zap-baseline.py \
                        -t http://localhost:8000 \
                        -r zap_report.htm
                '''
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
            sh "docker rm -f ${PROJECT_NAME}-test || true"
            sh "docker-compose -f docker-compose.selenium.yml down || true"
        }
    }
}