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
                    env.IMAGE_TAG = "${IMAGE_NAME}:${env.BUILD_NUMBER}"

                    echo "Building Docker image: ${env.IMAGE_TAG}"
                    sh "docker build -t ${env.IMAGE_TAG} ."
                }
            }
        }

        // stage('Docker Build') {
        //     steps {
        //         script {
        //             def shortCommit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        //             env.SHORT_COMMIT = shortCommit
        //             env.IMAGE_TAG = "${IMAGE_NAME}:${shortCommit}"

        //             echo "Building Docker image: ${env.IMAGE_TAG}"
        //             sh "docker build -t ${env.IMAGE_TAG} ."
        //         }
        //     }
        // }

        // 3. Trivy Docker Image Scan (scan built image for vulnerabilities)
        stage('Trivy Docker Image Scan') {
            steps {
                script {
                    sh '''
                        mkdir -p trivy-reports

                        docker run --rm \
                            -v $(pwd):/workspace \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            -v trivy-cache:/root/.cache/ \
                            aquasec/trivy:latest \
                            image ${IMAGE_TAG} \
                            --exit-code 1 \
                            --severity HIGH,CRITICAL \
                            --format table \
                            --output /workspace/trivy-reports/image-scan.txt
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-reports/image-scan.txt', fingerprint: true
                }
            }
        }


        // 4. Approval before pushing
        stage('Approval Before Push') {
            steps {
                script {
                    input message: "Vulnerability scans passed. Approve to push Docker image ${env.IMAGE_TAG}?", ok: 'Push'
                }
            }
        }

        // 5. Push Docker image after approval
        stage('Docker Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-pat', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh """
                            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                            docker push ${env.IMAGE_TAG}
                            docker logout
                        """
                    }
                }
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
