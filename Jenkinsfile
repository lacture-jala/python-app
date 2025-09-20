pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        SONARQUBE = 'SonarQubeServer'         // Jenkins-configured SonarQube instance
        scannerHome = tool 'SonarQubeScanner' // MUST be defined in Jenkins Global Tool Config
    }

    stages {
        stage('Setup Python') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'mkdir -p reports'
                sh './venv/bin/pytest --junitxml=reports/test-results.xml'
                sh './venv/bin/coverage xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE}") {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            junit 'reports/test-results.xml'

            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '',
                reportFiles: 'coverage.xml',
                reportName: 'Coverage Report'
            ])
        }
    }
}
