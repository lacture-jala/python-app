pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
        SONARQUBE = 'SonarQubeServer'
        scannerHome = tool 'SonarQubeScanner'
        IMAGE_NAME = 'ashish142/your-app-name'
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
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // 1. Trivy Filesystem Scan (source & dependencies)
        stage('Trivy Filesystem Scan') {
            steps {
                script {
                    sh '''
                        mkdir -p trivy-reports

                        docker run --rm \
                            -v $(pwd):/project \
                            -v trivy-cache:/root/.cache/ \
                            aquasec/trivy:latest \
                            fs /project \
                            --exit-code 1 \
                            --severity HIGH,CRITICAL \
                            --format table \
                            --output /project/trivy-reports/fs-scan.txt
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-reports/fs-scan.txt', fingerprint: true
                }
            }
        }

        // 2. Build Docker image (tagged with git short SHA)
                stage('Docker Build') {
            steps {
                script {
                    env.IMAGE_TAG = "${IMAGE_NAME}:${BUILD_NUMBER}"
                    echo "Building Docker image: ${env.IMAGE_TAG}"
                    sh "docker build -t ${env.IMAGE_TAG} ."
                }
            }
        }

        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    sh 'mkdir -p trivy-reports'

                    def trivyStatus = sh(
                        script: """
                            docker run --rm \
                                -v ${env.WORKSPACE}:/workspace \
                                -v /var/run/docker.sock:/var/run/docker.sock \
                                -v trivy-cache:/root/.cache/ \
                                aquasec/trivy:latest image ${env.IMAGE_TAG} \
                                --exit-code 1 \
                                --severity HIGH,CRITICAL \
                                --format table \
                                --output /workspace/trivy-reports/image-scan.txt
                        """,
                        returnStatus: true
                    )

                    if (trivyStatus != 0) {
                        error "Trivy found HIGH or CRITICAL vulnerabilities in the Docker image."
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-reports/image-scan.txt', fingerprint: true
                }
            }
        }

        stage('Approval Before Push') {
            when {
                expression {
                    return true // Always run unless explicitly failed
                }
            }
            steps {
                input message: "Trivy scan passed. Do you want to proceed with Docker push?"
                echo "Approved by user to push the Docker image"
                // Add docker push or other logic here
            }
        }

        // Optional deploy stage
        stage('Deploy') {
            steps {
                echo "Deploying image ${env.IMAGE_TAG}..."
                // Add your deployment commands here
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
