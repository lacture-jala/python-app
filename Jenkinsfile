pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        SONARQUBE = 'SonarQubeServer'  // Jenkins SonarQube server name from Jenkins config
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
                sh './venv/bin/coverage run -m pytest'
                sh './venv/bin/coverage xml'  // generate XML for SonarQube
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh './venv/bin/sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            junit '**/reports/*.xml'  // if you generate junit reports
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
